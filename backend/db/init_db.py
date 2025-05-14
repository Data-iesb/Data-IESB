import psycopg2
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SCHEMA = os.getenv("SCHEMA") 

def init_db():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute(f"SET search_path TO {SCHEMA};")

        cur.execute("""
            CREATE TABLE IF NOT EXISTS aluno (
                id SERIAL PRIMARY KEY,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                curso TEXT NOT NULL,
                periodo INTEGER,
                senha TEXT NOT NULL                
            );
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS relatorio (
                id SERIAL PRIMARY KEY,
                caminho_pasta TEXT NOT NULL,
                titulo TEXT NOT NULL,
                descricao TEXT,
                data_publicacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                assunto TEXT NOT NULL,
                aluno_id INTEGER REFERENCES aluno(id)
            );
        """)

        conn.commit()
        cur.close()
        conn.close()
        print("Tabelas criadas com sucesso.")

    except Exception as e:
        print("Erro ao criar as tabelas:")
        print(e)

if __name__ == "__main__":
    init_db()
