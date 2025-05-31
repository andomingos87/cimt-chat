FROM python:3.11

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "src/app/chat_rag.py"]
