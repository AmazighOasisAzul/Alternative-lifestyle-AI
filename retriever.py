#!/usr/bin/env python3
"""
Alternative Lifestyle AI - Enhanced Retriever with Hybrid Search
Implements: Hybrid (dense + BM25), Recency Weighting, Metadata Filters
"""

from typing import List, Dict, Tuple, Optional
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from rank_bm25 import BM25Okapi
import os
import numpy as np
from datetime import datetime, timedelta
from config import VECTOR_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP, RAG_CONFIG


class HybridRetriever:
    """
    Implements hybrid search (dense embeddings + BM25) with recency weighting
    and metadata filtering capabilities.
    """
    
    def __init__(self, vector_db_path: str = VECTOR_DB_PATH, 
                 chunk_size: int = CHUNK_SIZE, 
                 chunk_overlap: int = CHUNK_OVERLAP):
        self.vector_db_path = vector_db_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.vector_store = None
        self.bm25_index = None
        self.documents = []
        self.last_resort_sources = {"incels_is", "schaduw"}
        self.config = RAG_CONFIG
        
        # Recency weighting parameters
        self.recency_weight = 0.2  # 20% weight to recency
        self.half_life_days = 365  # Documents lose half their recency weight in 1 year
    
    def load_vector_store(self):
        """Load vector database and build BM25 index."""
        if not os.path.exists(self.vector_db_path):
            os.makedirs(self.vector_db_path, exist_ok=True)
        
        self.vector_store = Chroma(
            persist_directory=self.vector_db_path,
            embedding_function=self.embedding_model
        )
        
        # Build BM25 index from vector store
        self._build_bm25_index()
    
    def _build_bm25_index(self):
        """Build BM25 index from vector store documents."""
        if self.vector_store is None:
            return
        
        try:
            # Get all documents from vector store
            all_docs = self.vector_store.get()
            texts = [doc.page_content for doc in all_docs['documents']]
            metadatas = all_docs['metadatas']
            
            # Tokenize for BM25
            tokenized_corpus = [doc.split() for doc in texts]
            self.bm25_index = BM25Okapi(tokenized_corpus)
            self.documents = list(zip(texts, metadatas))
        except Exception as e:
            print(f"Error building BM25 index: {e}")
            self.bm25_index = None
    
    def index_documents(self, documents: List[Dict]):
        """Index documents into vector store and update BM25."""
        if self.vector_store is None:
            self.load_vector_store()
        
        texts = []
        metadatas = []
        bm25_texts = []
        
        for doc in documents:
            content = doc.get('content', '')
            if not content:
                continue
            
            chunks = self.text_splitter.create_documents([content])
            for chunk in chunks:
                metadata = {
                    'source': doc.get('source', 'unknown'),
                    'category': doc.get('category', 'general'),
                    'title': doc.get('title', 'No title'),
                    'url': doc.get('url', ''),
                    'date': doc.get('date'),
                    'is_last_resort': doc.get('source') in self.last_resort_sources or doc.get('last_resort_only', False),
                    'subreddit': doc.get('subreddit', '')
                }
                texts.append(chunk.page_content)
                metadatas.append(metadata)
                bm25_texts.append(chunk.page_content)
        
        if texts:
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)
            
            # Update BM25 index
            if self.bm25_index is not None:
                for text in bm25_texts:
                    self.bm25_index.add_document(text.split())
    
    def _calculate_recency_score(self, metadata: Dict) -> float:
        """Calculate recency score (0-1, where 1 is most recent)."""
        date_str = metadata.get('date')
        if not date_str:
            return 0.5  # Neutral score for no date
        
        try:
            # Try to parse date
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        except:
            try:
                date_obj = datetime.strptime(date_str, '%B %d, %Y')
            except:
                return 0.5
        
        age_days = (datetime.now() - date_obj).days
        recency_score = np.exp(-np.log(2) * age_days / self.half_life_days)
        return float(recency_score)
    
    def _apply_metadata_filter(self, metadata: Dict, filters: Dict) -> bool:
        """Apply metadata filters to a document."""
        if not filters:
            return True
        
        for key, value in filters.items():
            if key == 'source' and metadata.get('source') != value:
                return False
            if key == 'category' and metadata.get('category') != value:
                return False
            if key == 'subreddit' and metadata.get('subreddit') != value:
                return False
            # Date range filtering
            if key == 'date_after':
                doc_date = metadata.get('date')
                if doc_date:
                    try:
                        doc_date_obj = datetime.strptime(doc_date, '%Y-%m-%d')
                        filter_date = datetime.strptime(value, '%Y-%m-%d')
                        if doc_date_obj < filter_date:
                            return False
                    except:
                        pass
        
        return True
    
    def hybrid_search(self, query: str, k: int = 8, filters: Dict = None, 
                      use_last_resort: bool = False) -> List[Tuple[Document, float]]:
        """
        Perform hybrid search combining dense embeddings and BM25.
        Returns documents with combined scores.
        """
        if self.vector_store is None:
            self.load_vector_store()
        
        # Dense search
        dense_results = self.vector_store.similarity_search_with_score(query, k=k*2)
        
        # BM25 search
        bm25_scores = []
        if self.bm25_index is not None:
            tokenized_query = query.split()
            bm25_scores = self.bm25_index.get_scores(tokenized_query)
        
        # Combine scores
        combined_results = []
        for i, (doc, dense_score) in enumerate(dense_results):
            if i >= len(bm25_scores):
                break
            
            metadata = doc.metadata if hasattr(doc, 'metadata') else {}
            
            # Apply filters
            if not self._apply_metadata_filter(metadata, filters):
                continue
            
            # Skip last resort if not requested
            if not use_last_resort and metadata.get('is_last_resort', False):
                continue
            
            # Calculate combined score
            bm25_score = bm25_scores[i]
            recency_score = self._calculate_recency_score(metadata)
            
            # Hybrid score: dense + BM25 + recency
            hybrid_score = (dense_score * 0.7 + 
                          bm25_score * 0.2 + 
                          recency_score * self.recency_weight)
            
            combined_results.append((doc, hybrid_score, metadata))
        
        # Sort by combined score
        combined_results.sort(key=lambda x: x[1], reverse=True)
        
        return [(doc, score) for doc, score, _ in combined_results[:k]]
    
    def fast_retrieve(self, query: str, k: int = 8, filter_source: Optional[str] = None, 
                      use_last_resort: bool = False) -> Tuple[List[Dict], str]:
        """Retrieve documents using hybrid search."""
        filters = {}
        if filter_source:
            filters['category'] = filter_source
        if not use_last_resort:
            filters['exclude_last_resort'] = True
        
        try:
            results = self.hybrid_search(query, k=k, filters=filters, use_last_resort=use_last_resort)
            return [self._format_result(r[0], r[1]) for r in results], "fast"
        except Exception as e:
            print(f"Retrieval error: {e}")
            return [], "fast"
    
    def _format_result(self, result: Document, score: float = None) -> Dict:
        metadata = result.metadata if hasattr(result, 'metadata') else {}
        formatted = {
            'content': result.page_content if hasattr(result, 'page_content') else str(result),
            'metadata': metadata,
            'category': metadata.get('category', 'general'),
            'is_last_resort': metadata.get('is_last_resort', False),
            'score': score
        }
        return formatted
    
    def retrieve_with_fallback(self, query: str, k: int = 8, filter_source: Optional[str] = None) -> Tuple[List[Dict], str, bool]:
        """Retrieve with fallback to last resort sources."""
        context, mode = self.fast_retrieve(query, k=k, filter_source=filter_source, use_last_resort=False)
        
        if len(context) >= k:
            return context, mode, False
        
        context, mode = self.fast_retrieve(query, k=k, filter_source=filter_source, use_last_resort=True)
        return context, mode, True
    
    def deep_retrieve(self, query: str, max_results: int = 8) -> Tuple[List[Dict], str]:
        print("Deep retrieval requires web_search module - using fast retrieval")
        return self.fast_retrieve(query, k=max_results, use_last_resort=True)
    
    def youtube_retrieve(self, query: str, max_results: int = 8, download: bool = False) -> Tuple[List[Dict], str]:
        print("YouTube retrieval requires youtube_search module - using fast retrieval")
        return self.fast_retrieve(query, k=max_results, use_last_resort=True)
    
    def get_statistics(self) -> Dict:
        """Get retrieval statistics."""
        return {
            'hybrid_search_enabled': self.config.get('hybrid_search', False),
            'recency_weighting_enabled': self.config.get('recency_weighting', False),
            'metadata_filters_enabled': self.config.get('metadata_filters', False)
        }


# For backward compatibility
DualModeRetriever = HybridRetriever


if __name__ == "__main__":
    retriever = HybridRetriever()
    retriever.load_vector_store()
    print("Hybrid retriever loaded with BM25 and recency weighting")