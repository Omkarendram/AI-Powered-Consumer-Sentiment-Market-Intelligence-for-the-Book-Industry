"""
RAG natural language Q&A and semantic search routes.
"""

from fastapi import APIRouter, HTTPException
from book_market_intelligence.api.schemas import RAGQueryRequest, RAGQueryResponse
from book_market_intelligence.rag.engine import rag_engine

router = APIRouter(prefix="/api/v1/rag", tags=["RAG"])


@router.post("/query", response_model=RAGQueryResponse)
def ask_market_intelligence(request: RAGQueryRequest) -> RAGQueryResponse:
    """
    Submits a natural language business question to the RAG engine
    retrieving consumer evidence and generating structured insights.
    """
    try:
        result = rag_engine.query(user_query=request.query, top_k=request.top_k)
        return RAGQueryResponse(
            query=result.query,
            answer=result.answer,
            query_type=result.query_type,
            retrieved_documents=result.retrieved_documents
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG query execution failed: {str(e)}")
