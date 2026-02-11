from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from rag.rag_app import answer_query, get_vector_store

# -----------------------------
# Create app FIRST
# -----------------------------

app = FastAPI(title="RAG Backend API")

# -----------------------------
# CORS (allow Streamlit frontend)
# -----------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Startup preload
# -----------------------------

@app.on_event("startup")
def preload():
    print("🔥 Preloading RAG system...")
    get_vector_store()
    print("✅ RAG ready")

# -----------------------------
# Request models
# -----------------------------

class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str

# -----------------------------
# API endpoint
# -----------------------------

@app.post("/ask", response_model=QueryResponse)
def ask(req: QueryRequest):
    answer = answer_query(req.question)
    return {"answer": answer}
