from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from rag.rag_app import answer_query

app = FastAPI(title="RAG Backend API")

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


class QueryRequest(BaseModel):
	question: str


class QueryResponse(BaseModel):
	answer: str


@app.get("/")
def health():
	return {"status": "ok"}


@app.post("/ask", response_model=QueryResponse)
def ask(req: QueryRequest):
	try:
		ans = answer_query(req.question)
		if not ans:
			return {"answer": "⚠️ No answer generated (empty response)."}
		return {"answer": ans}
	except Exception as e:
		# don't expose raw trace to client, but provide a helpful message
		import traceback
		traceback.print_exc()
		return {"answer": f"⚠️ Backend error: {str(e)}"}

