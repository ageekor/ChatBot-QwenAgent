from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import uvicorn
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
import json

app = FastAPI(title="RAG知识库服务")

class SearchRequest(BaseModel):
    query: str
    k: Optional[int] = 3

class AddDocumentRequest(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None

class SearchResponse(BaseModel):
    results: List[Dict[str, Any]]

class AddDocumentResponse(BaseModel):
    status: str
    message: str

class RAGService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(
            model_name="shibing624/text2vec-base-chinese",
            model_kwargs={'device': 'cpu'}
        )
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        self.vector_store = None
        self._load_vector_store()

    def _load_vector_store(self):
        if os.path.exists("knowledge_base"):
            self.vector_store = FAISS.load_local("knowledge_base", self.embeddings, allow_dangerous_deserialization=True)
        else:
            self.vector_store = FAISS.from_texts([""], self.embeddings)

    def search(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        docs = self.vector_store.similarity_search(query, k=k)
        results = []
        for doc in docs:
            results.append({
                'content': doc.page_content,
                'metadata': doc.metadata
            })
        return results

    def add_document(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        texts = self.text_splitter.split_text(content)
        metadata = metadata or {}
        
        self.vector_store.add_texts(texts, metadatas=[metadata] * len(texts))
        self.vector_store.save_local("knowledge_base")
        
        return f"成功添加 {len(texts)} 个文本块到知识库"

rag_service = RAGService()

@app.post("/search", response_model=SearchResponse)
async def search(request: SearchRequest):
    try:
        results = rag_service.search(request.query, request.k)
        return SearchResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/add_document", response_model=AddDocumentResponse)
async def add_document(request: AddDocumentRequest):
    try:
        message = rag_service.add_document(request.content, request.metadata)
        return AddDocumentResponse(status="success", message=message)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 