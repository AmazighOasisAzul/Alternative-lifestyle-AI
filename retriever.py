#!/usr/bin/env python3
"""
Alternative Lifestyle AI - Dual-Mode Retriever with Last Resort Handling
"""

from typing import List, Dict, Tuple, Optional
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import os
from config import VECTOR_DB_PATH, CHUNK_SIZE, CHUNK_OVERLAP


class DualModeRetriever:
    def __init__(self, vector_db_path: str = VECTOR_DB_PATH, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.vector_db_path = vector_db_path
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self.embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.vector_store = None
        self.last_resort_sources = {"incels_is", "schaduw"}
    
    def load_vector_store(self):
        if not os.path.exists(self.vector_db_path):
            os.makedirs(self.vector_db_path, exist_ok=True)
        self.vector_store = Chroma(
            persist_directory=self.vector_db_path,
            embedding_function=self.embedding_model
        )
    
    def index_documents(self, documents: List[Dict]):
        if self.vector_store is None:
            self.load_vector_store()
        texts = []
        metadatas = []
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
                    'is_last_resort': doc.get('source') in self.last_resort_sources or doc.get('last_resort_only', False)
                }
                texts.append(chunk.page_content)
                metadatas.append(metadata)
        if texts:
            self.vector_store.add_texts(texts=texts, metadatas=metadatas)
    
    def fast_retrieve(self, query: str, k: int = 8, filter_source: Optional[str] = None, use_last_resort: bool = False):
        if self.vector_store is None:
            self.load_vector_store()
        filter_dict = {}
        if filter_source:
            filter_dict['category'] = filter_source
        if not use_last_resort:
            filter_dict['is_last_resort'] = False
        try:
            results = self.vector_store.similarity_search(query, k=k, filter=filter_dict if filter_dict else None)
            return [self._format_result(r) for r in results], "fast"
        except Exception as e:
            print(f"Retrieval error: {e}")
            return [], "fast"
    
    def deep_retrieve(self, query: str, max_results: int = 8):
        print("Deep retrieval requires web_search module - using fast retrieval instead")
        return self.fast_retrieve(query, k=max_results, use_last_resort=True)
    
    def youtube_retrieve(self, query: str, max_results: int = 8, download: bool = False):
        print("YouTube retrieval requires youtube_search module - using fast retrieval instead")
        return self.fast_retrieve(query, k=max_results, use_last_resort=True)
    
    def _format_result(self, result: Document) -> Dict:
        metadata = result.metadata if hasattr(result, 'metadata') else {}
        return {
            'content': result.page_content if hasattr(result, 'page_content') else str(result),
            'metadata': metadata,
            'category': metadata.get('category', 'general'),
            'is_last_resort': metadata.get('is_last_resort', False)
        }
    
    def retrieve_with_fallback(self, query: str, k: int = 8, filter_source: Optional[str] = None):
        context, mode = self.fast_retrieve(query, k=k, filter_source=filter_source, use_last_resort=False)
        if len(context) >= k:
            return context, mode, False
        context, mode = self.fast_retrieve(query, k=k, filter_source=filter_source, use_last_resort=True)
        return context, mode, True


if __name__ == "__main__":
    retriever = DualModeRetriever()
    retriever.load_vector_store()
    print("Retriever loaded")