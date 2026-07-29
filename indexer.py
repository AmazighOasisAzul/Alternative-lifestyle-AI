#!/usr/bin/env python3
"""
Alternative Lifestyle AI - Indexer
"""

import os
import json
import glob
from retriever import DualModeRetriever
from config import VECTOR_DB_PATH


def index_all_documents(data_dir: str = "data", vector_db_path: str = VECTOR_DB_PATH):
    retriever = DualModeRetriever(vector_db_path=vector_db_path)
    all_documents = []
    json_files = glob.glob(os.path.join(data_dir, "*.json"))
    for json_file in json_files:
        print(f"Loading {json_file}...")
        try:
            with open(json_file, 'r') as f:
                documents = json.load(f)
            all_documents.extend(documents)
            print(f"  Loaded {len(documents)} documents")
        except Exception as e:
            print(f"  Error: {e}")
    if all_documents:
        print(f"Indexing {len(all_documents)} documents...")
        retriever.index_documents(all_documents)
        print("Indexing complete!")
    return len(all_documents)


def index_from_sources(vector_db_path: str = VECTOR_DB_PATH, max_pages: int = 500):
    from crawler import crawl_all_sources
    print("Crawling all sources...")
    documents = crawl_all_sources(max_pages=max_pages)
    print(f"Indexing {len(documents)} documents...")
    retriever = DualModeRetriever(vector_db_path=vector_db_path)
    retriever.index_documents(documents)
    print("Indexing complete!")
    return len(documents)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Index documents")
    parser.add_argument("--data-dir", type=str, default="data")
    parser.add_argument("--vector-db", type=str, default=VECTOR_DB_PATH)
    parser.add_argument("--from-sources", action="store_true")
    parser.add_argument("--max-pages", type=int, default=500)
    args = parser.parse_args()
    if args.from_sources:
        count = index_from_sources(vector_db_path=args.vector_db, max_pages=args.max_pages)
    else:
        count = index_all_documents(data_dir=args.data_dir, vector_db_path=args.vector_db)
    print(f"Indexed {count} documents")