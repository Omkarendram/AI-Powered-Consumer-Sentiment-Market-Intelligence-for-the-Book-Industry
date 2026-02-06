import os
import pandas as pd
from dotenv import load_dotenv

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from groq import Groq

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")

client = Groq(api_key=GROQ_API_KEY)

# Path to your sentiment results
DATA_PATH = "data/processed/sentiment_analysis_results_batch.csv"


def load_documents():
    df = pd.read_csv(DATA_PATH)
    docs = []

    for _, row in df.iterrows():
        text = f"""
Customer Comment:
{row.get('clean_text', '')}

Sentiment: {row.get('sentiment', '')}
Confidence: {row.get('confidence', '')}
"""
        docs.append(Document(page_content=text.strip()))

    return docs


def build_vector_store(documents):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(documents)

    vectordb = Chroma.from_documents(chunks, embedding=embeddings)
    return vectordb


def ask_llm(question, context_docs):
    context_blocks = []
    for i, doc in enumerate(context_docs, start=1):
        context_blocks.append(f"""
[Feedback {i}]
{doc.page_content}
""")

    context = "\n".join(context_blocks)

    prompt = f"""
You are a senior market analyst for an online book platform.

Use ONLY the feedback excerpts below to answer the question.
If the context does not contain enough information, say "Insufficient data in current dataset."

Feedback Data:
{context}

Question:
{question}

Respond in 3–4 concise bullet points with actionable insights.
Do NOT invent numbers, percentages, or new examples.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.1,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()


def main():
    print("🔹 Loading documents...")
    docs = load_documents()

    print("🔹 Building vector store...")
    vectordb = build_vector_store(docs)

    print("\n✅ RAG system ready!")
    print("Ask questions (type 'exit' to quit)\n")

    while True:
        query = input("Ask: ")
        if query.lower() == "exit":
            break

        # retrieval method 
        retrieved_docs = vectordb.similarity_search(query, k=4)
        answer = ask_llm(query, retrieved_docs)

        print("\n🤖 Answer:\n", answer)
        print("-" * 60)


if __name__ == "__main__":
    main()
