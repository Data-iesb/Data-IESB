import psycopg2
import os

DATABASE_URL = os.getenv("DATABASE_URL")

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    
    cur.execute("SELECT version();")
    version = cur.fetchone()

    print("Conexão bem-sucedida!")
    print("Versão do PostgreSQL:", version[0])

    cur.close()
    conn.close()

except Exception as e:
    print("Erro na conexão com o banco de dados:")
    print(e)
