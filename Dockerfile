FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 7860

CMD ["python", "-m", "uvicorn", "rag.api:app", "--host", "0.0.0.0", "--port", "7860"]
