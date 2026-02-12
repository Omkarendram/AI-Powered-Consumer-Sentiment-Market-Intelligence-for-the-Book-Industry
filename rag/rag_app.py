import os
import pandas as pd
from dotenv import load_dotenv
import streamlit as st
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import FakeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from groq import Groq

# -----------------------
# Setup
# -----------------------

load_dotenv()
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

if not GROQ_API_KEY:
    print("⚠️ WARNING: GROQ_API_KEY not set")

def get_groq_client():
    from groq import Groq
    return Groq(api_key=GROQ_API_KEY)


DATA_PATH = "sentiment_analysis/book_market_sentiment_topics.csv"

# Global vector DB (loaded once for UI/API)
_vectordb = None


# -----------------------
# Data Loading
# -----------------------

def load_documents():
    """
    Load cleaned feedback and attach useful metadata.
    We embed only the user feedback text for better semantic retrieval.
    """
    df = pd.read_csv(DATA_PATH)
    docs = []

    for _, row in df.iterrows():
        clean_text = str(row.get("clean_text", "")).strip()
        sentiment = str(row.get("sentiment", "")).strip()
        confidence = str(row.get("confidence", "")).strip()

        if not clean_text:
            continue

        docs.append(
            Document(
                page_content=clean_text,
                metadata={
                    "sentiment": sentiment,
                    "confidence": confidence
                }
            )
        )

    return docs


def build_vector_store(documents):
    embeddings = FakeEmbeddings(size=384)

    splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
    chunks = splitter.split_documents(documents)

    vectordb = Chroma.from_documents(chunks, embedding=embeddings)
    return vectordb


def get_vector_store():
    """
    Lazy-load vector DB so UI/API can reuse it without rebuilding every query.
    """
    global _vectordb
    if _vectordb is None:
        print("🔹 Loading documents...")
        docs = load_documents()

        print("🔹 Building vector store...")
        _vectordb = build_vector_store(docs)

        print("✅ Vector store ready.")
    return _vectordb


# -----------------------
# Query Handling
# -----------------------

def classify_query(query: str):
    q = query.lower()
    if any(word in q for word in ["complaint", "problem", "issue", "bad", "negative"]):
        return "negative"
    if any(word in q for word in ["like", "love", "good", "positive", "happy"]):
        return "positive"
    return "general"


def ask_llm(question, context_docs):
    context_blocks = []

    for i, doc in enumerate(context_docs, start=1):
        sentiment = doc.metadata.get("sentiment", "unknown")
        context_blocks.append(
            f"""
[Feedback {i}]
Text: {doc.page_content}
Sentiment: {sentiment}
"""
        )

    context = "\n".join(context_blocks)

    prompt = f"""
You are a senior market intelligence analyst for an online book platform.

Use ONLY the feedback excerpts below to answer the question.
If the context does not contain enough information, say:
"Insufficient data in current dataset."

Structure your response as:
1) Key issue or trend
2) Evidence from feedback
3) Business implication
4) Suggested action

Feedback Data:
{context}

Question:
{question}

Respond concisely in 3–4 bullet points.
Do NOT invent statistics or new examples.
"""
    client = get_groq_client()
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=350
    )

    return response.choices[0].message.content.strip()


def answer_query(query: str) -> str:
    """
    Main function to be called by UI / API.
    """
    vectordb = get_vector_store()
    query_type = classify_query(query)

    if query_type == "negative":
        retrieved_docs = vectordb.similarity_search(query, k=6, filter={"sentiment": "negative"})
    elif query_type == "positive":
        retrieved_docs = vectordb.similarity_search(query, k=6, filter={"sentiment": "positive"})
    else:
        retrieved_docs = vectordb.similarity_search(query, k=6)

    return ask_llm(query, retrieved_docs)


# -----------------------
# Optional CLI for local testing
# -----------------------

def main():
    print("\n✅ RAG system ready! (CLI mode)")
    print("Ask questions (type 'exit' to quit)\n")

    while True:
        query = input("Ask: ")
        if query.lower() == "exit":
            break

        answer = answer_query(query)
        print("\n🤖 Answer:\n", answer)
        print("-" * 60)


if __name__ == "__main__":
    main()
