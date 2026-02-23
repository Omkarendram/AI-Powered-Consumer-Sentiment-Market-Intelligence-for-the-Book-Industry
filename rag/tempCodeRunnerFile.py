from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.middleware.cors import CORSMiddleware

# from rag.rag_app import answer_query

# import os
# import uvicorn

# app = FastAPI(title="RAG Backend API")

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class QueryRequest(BaseModel):
#     question: str

# class QueryResponse(BaseModel):
#     answer: str

# @app.get("/")
# def health():
#     return {"status": "ok"}

# @app.post("/ask", response_model=QueryResponse)
# def ask(req: QueryRequest):
#     return {"answer": answer_query(req.question)}

# # ✅ THIS PART FIXES RENDER
# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", 8000))
#     uvicorn.run("rag.api:app", host="0.0.0.0", port=port)
