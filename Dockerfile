# Use uma imagem mais leve
FROM python:3.11-slim

# Instale apenas dependências essenciais do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copie apenas o requirements.txt primeiro (para cache)
COPY requirements.txt ./

# Instale dependências Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

# Copie apenas os arquivos necessários
COPY src/ ./src/
COPY .env ./

ENV PYTHONPATH=/app

EXPOSE 8501

CMD ["streamlit", "run", "src/app/chat_rag.py", "--server.port=8501", "--server.address=0.0.0.0"]