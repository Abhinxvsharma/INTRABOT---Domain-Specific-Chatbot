from typing import List, Dict, Any
from langchain_ollama import OllamaLLM
from langchain_core.prompts import PromptTemplate
from app.services.vector_store import VectorStoreService
from app.utils.cache_utils import CacheUtils
from app.utils.config import (
    LLM_MODEL, OLLAMA_BASE_URL, TEMPERATURE, MAX_TOKENS,
    RETRIEVAL_TOP_K, RERANK_TOP_K, SIMILARITY_THRESHOLD
)

class RAGService:
    def __init__(self, vector_store_service: VectorStoreService = None):
        self.llm = OllamaLLM(
            model=LLM_MODEL,
            base_url=OLLAMA_BASE_URL,
            temperature=TEMPERATURE,
            num_predict=MAX_TOKENS
        )
        self.vector_store_service = vector_store_service or VectorStoreService()

    def _get_prompt_template(self) -> PromptTemplate:
        template = """
        You are IntraBot, a local HR assistant. Use only the following pieces of context to answer the user's question. 
        If you don't know the answer or the information is not in the context, say EXACTLY "Information not found in documents".
        Do NOT use external knowledge. Do NOT hallucinate.

        Also check for context in each uploaded document and give answer from that document.
        Context:
        {context}

        Question: {question}

        Answer:"""
        return PromptTemplate(template=template, input_variables=["context", "question"])

    def query(self, user_query: str, doc_name: str = None) -> Dict[str, Any]:
        """Performs RAG query with caching, re-ranking and grounding."""
        # Normalize doc_name (if "All Documents" or None, treat as None)
        if doc_name == "All Documents":
            doc_name = None

        # Check cache first
        cached_res = CacheUtils.get_from_cache(user_query, doc_name)
        if cached_res:
            return cached_res

        retriever = self.vector_store_service.get_retriever(search_kwargs={"k": RERANK_TOP_K})
        if not retriever:
            return {"answer": "Knowledge base is empty. Please upload documents first.", "sources": []}

        # Retrieve candidates for re-ranking
        try:
            vectorstore = self.vector_store_service.get_vectorstore()
            if not vectorstore:
                return {"answer": "Knowledge base is empty. Please upload documents first.", "sources": []}
                
            # Apply filter if doc_name is provided
            search_kwargs = {"k": RERANK_TOP_K}
            if doc_name:
                search_kwargs["filter"] = {"source": doc_name}
                print(f"\033[94m[SEARCH]\033[0m Filtering by document: '{doc_name}'")

            docs_with_scores = vectorstore.similarity_search_with_score(user_query, **search_kwargs)
            
            if not docs_with_scores and doc_name:
                print(f"\033[93m[WARNING]\033[0m No chunks found for filter: {{'source': '{doc_name}'}}")
                # Diagnostic: Print a few available sources in the index
                all_ids = list(vectorstore.docstore._dict.keys())
                available_sources = set([vectorstore.docstore.search(sid).metadata.get('source') for sid in all_ids[:20]])
                print(f"\033[94m[DEBUG]\033[0m Sample sources available in index: {available_sources}")

            print(f"\033[94m[SEARCH]\033[0m Found {len(docs_with_scores)} candidates.")
            for i, (doc, score) in enumerate(docs_with_scores):
                print(f"  {i+1}. Score: {score:.4f} | Source: {doc.metadata.get('source')} | Snippet: {doc.page_content[:50]}...")

            relevant_docs = [doc for doc, score in docs_with_scores[:RETRIEVAL_TOP_K]]
            
        except Exception as e:
            print(f"\033[91m[ERROR]\033[0m Retrieval failed: {str(e)}")
            return {"answer": f"Error during retrieval: {str(e)}", "sources": []}
        
        if not relevant_docs:
            print("\033[93m[SEARCH]\033[0m No relevant documents found.")
            return {"answer": "Information not found in documents", "sources": []}

        context = "\n\n".join([doc.page_content for doc in relevant_docs])
        prompt = self._get_prompt_template().format(context=context, question=user_query)
        
        answer = self.llm.invoke(prompt)
        
        result = {
            "answer": answer,
            "sources": list(set([doc.metadata.get("source", "Unknown") for doc in relevant_docs]))
        }
        
        # Save to cache
        CacheUtils.save_to_cache(user_query, result, doc_name)
        
        return result
