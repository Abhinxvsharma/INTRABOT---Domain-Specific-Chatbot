import os
from typing import List
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader, TextLoader, CSVLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from app.utils.config import CHUNK_SIZE, CHUNK_OVERLAP, MIN_CHUNK_SIZE

class IngestionService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
            length_function=len,
            separators=["\n\n", "\n", ".", " ", ""]
        )

    def load_document(self, file_path: str) -> List[Document]:
        """Loads a document based on its extension."""
        ext = os.path.splitext(file_path)[-1].lower()
        if ext == ".pdf":
            loader = PyPDFLoader(file_path)
        elif ext in [".docx", ".doc"]:
            loader = Docx2txtLoader(file_path)
        elif ext in [".txt", ".md"]:
            loader = TextLoader(file_path)
        elif ext == ".csv":
            loader = CSVLoader(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
        return loader.load()

    def process_documents(self, file_paths: List[str]) -> List[Document]:
        """Loads, chunks, and filters documents."""
        all_docs = []
        # Deduplicate paths just in case
        unique_paths = list(set(file_paths))
        print(f"\n\033[94m[INGEST]\033[0m Starting processing for {len(unique_paths)} unique files...")
        
        for path in unique_paths:
            try:
                if not os.path.exists(path):
                    print(f"  - \033[91m[ERROR]\033[0m File not found: {path}")
                    continue
                    
                docs = self.load_document(path)
                print(f"  - Loaded '{os.path.basename(path)}': {len(docs)} pages/parts")
                all_docs.extend(docs)
            except Exception as e:
                print(f"  - \033[91m[ERROR]\033[0m Failed to load '{os.path.basename(path)}': {str(e)}")
        
        if not all_docs:
            print("\033[93m[WARNING]\033[0m No documents were loaded successfully.")
            return []

        # Chunking
        chunks = self.text_splitter.split_documents(all_docs)
        print(f"\033[94m[INGEST]\033[0m Split into {len(chunks)} raw chunks.")
        
        # Normalize source metadata to filename only
        for chunk in chunks:
            if "source" in chunk.metadata:
                chunk.metadata["source"] = os.path.basename(chunk.metadata["source"])
        
        # Filtering
        filtered_chunks = [
            chunk for chunk in chunks 
            if len(chunk.page_content.split()) >= MIN_CHUNK_SIZE
        ]
        
        print(f"\033[92m[INGEST]\033[0m Final result: {len(filtered_chunks)} chunks survived (Min Size: {MIN_CHUNK_SIZE} words).")
        return filtered_chunks
