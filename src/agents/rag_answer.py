import os
import openai
from supabase import create_client
from db.pg_connection import conectar_postgres

openai.api_key = os.getenv("OPENAI_API_KEY")
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))
EMBEDDING_MODEL = "text-embedding-3-small"
GPT_MODEL = "gpt-3.5-turbo"  # ou "gpt-3.5-turbo" para reduzir custo

def gerar_embedding_pergunta(pergunta: str):
    resposta = openai.Embedding.create(
        model=EMBEDDING_MODEL,
        input=pergunta
    )
    return resposta["data"][0]["embedding"]

def buscar_documentos_similares(vetor, k=5):
    conn = conectar_postgres()
    cur = conn.cursor()

    vetor_str = ",".join([str(x) for x in vetor])
    query = f"""
        SELECT assunto, timestamp, texto_chunk
        FROM document_chunks
        ORDER BY embedding <-> '[{vetor_str}]'::vector
        LIMIT {k};
    """

    cur.execute(query)
    resultados = cur.fetchall()
    cur.close()
    conn.close()

    docs = []
    for assunto, timestamp, texto_chunk in resultados:
        docs.append({
            "assunto": assunto,
            "timestamp": timestamp,
            "texto_chunk": texto_chunk
        })
    return docs

def montar_prompt(pergunta, documentos):
    contexto = "\n---\n".join(
        f"[{doc['assunto']} | {doc['timestamp']}]: {doc['texto_chunk']}" for doc in documentos
    )
    return f"""Você é um assistente especializado nos conteúdos do curso CIMT.

Baseando-se nos trechos abaixo, responda com linguagem clara, prática e objetiva. Se não souber, diga "não sei com base nos dados fornecidos".

Contexto:
{contexto}

Pergunta: {pergunta}
"""

def responder_pergunta(pergunta: str) -> str:
    vetor = gerar_embedding_pergunta(pergunta)
    docs = buscar_documentos_similares(vetor)
    prompt = montar_prompt(pergunta, docs)
    resposta = openai.ChatCompletion.create(
        model=GPT_MODEL,
        messages=[
            {"role": "system", "content": "Você é um assistente da CIMT."},
            {"role": "user", "content": prompt}
        ]
    )
    return resposta.choices[0].message.content
