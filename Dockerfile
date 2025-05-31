FROM python:3.11-slim

# Declarar argumentos do build
ARG OPENAI_API_KEY
ARG SUPABASE_URL
ARG SUPABASE_KEY
ARG PGHOST
ARG PGPORT
ARG PGDATABASE
ARG PGUSER
ARG PGPASSWORD

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt && \
    pip cache purge

COPY src/ ./src/

# Definir variáveis de ambiente
ENV PYTHONPATH=/app
ENV OPENAI_API_KEY=$OPENAI_API_KEY
ENV SUPABASE_URL=$SUPABASE_URL
ENV SUPABASE_KEY=$SUPABASE_KEY
ENV PGHOST=$PGHOST
ENV PGPORT=$PGPORT
ENV PGDATABASE=$PGDATABASE
ENV PGUSER=$PGUSER
ENV PGPASSWORD=$PGPASSWORD

EXPOSE 8501

CMD ["streamlit", "run", "src/app/chat_rag.py", "--server.port=8501", "--server.address=0.0.0.0"]