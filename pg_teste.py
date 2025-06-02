import psycopg2
from psycopg2 import OperationalError

try:
    conn = psycopg2.connect(
        host="db.yignltxsqnbuvtobhtbw.supabase.co",
        port=5432,
        dbname="postgres",
        user="postgres",
        password="Q9Ee8Bd7hNnlE9A1"
    )
    print("✅ Conexão estabelecida com sucesso!")
    conn.close()
except OperationalError as e:
    print("❌ Falha na conexão:")
    print(e)
