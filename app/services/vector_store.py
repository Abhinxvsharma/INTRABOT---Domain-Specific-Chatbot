import os
from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from app.utils.config import VECTORSTORE_DIR
from app.utils.embeddings import get_embeddings

class VectorStoreService:
    def __init__(self):
        self.embeddings = get_embeddings()
        os.makedirs(VECTORSTORE_DIR, exist_ok=True)
        self.index_path = os.path.normpath(os.path.join(VECTORSTORE_DIR, "faiss_index"))
        print(f"\033[94m[INDEX]\033[0m Database path: {self.index_path}")

    def get_vectorstore(self):
        """Returns the raw vectorstore object."""
        if not os.path.exists(self.index_path):
            print("\033[93m[INDEX]\033[0m No index found on disk yet.")
            return None
        return FAISS.load_local(
            self.index_path, 
            self.embeddings,
            allow_dangerous_deserialization=True
        )

    def create_or_update_index(self, documents: List[Document]):
        """Updates the FAISS index with new documents."""
        vectorstore = self.get_vectorstore()
        if vectorstore:
            vectorstore.add_documents(documents)
        else:
            vectorstore = FAISS.from_documents(documents, self.embeddings)
        
        vectorstore.save_local(self.index_path)
        print(f"\033[92m[INDEX]\033[0m Successfully updated index with {len(documents)} new chunks.")
        return vectorstore

    def recreate_index(self, documents: List[Document]):
        """Clears and recreates the FAISS index from scratch."""
        if not documents:
            return None
            
        vectorstore = FAISS.from_documents(documents, self.embeddings)
        vectorstore.save_local(self.index_path)
        print(f"\033[92m[INDEX]\033[0m Index RECREATED with {len(documents)} total chunks.")
        return vectorstore

    def get_retriever(self, search_kwargs=None):
        """Loads and returns the retriever."""
        vectorstore = self.get_vectorstore()
        if not vectorstore:
            return None
        return vectorstore.as_retriever(search_kwargs=search_kwargs or {"k": 3})
