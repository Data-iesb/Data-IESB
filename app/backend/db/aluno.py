import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SCHEMA = os.getenv("SCHEMA")



def criar_aluno(nome, email, curso, periodo, senha):
    try:
        periodo = int(periodo)
    except ValueError:
        print("O período deve ser um número inteiro.")
        return

    senha_hash = generate_password_hash(senha)

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {SCHEMA};")

        cur.execute("""
            INSERT INTO aluno (nome, email, curso, periodo, senha)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome, email, curso, periodo, senha_hash))

        conn.commit()
        cur.close()
        conn.close()

        print("Aluno cadastrado com sucesso!")

    except Exception as e:
        print("Erro ao cadastrar aluno:")
        print(e)



def buscar_aluno_por_id(id_aluno):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {SCHEMA};")

        cur.execute("""
            SELECT id, nome, email, curso, periodo
            FROM aluno
            WHERE id = %s
        """, (id_aluno,))
        resultado = cur.fetchone()

        cur.close()
        conn.close()

        if resultado:
            return {
                "id": resultado[0],
                "nome": resultado[1],
                "email": resultado[2],
                "curso": resultado[3],
                "periodo": resultado[4]
            }
        else:
            return None

    except Exception as e:
        raise e



def editar_aluno(id_aluno, nome, curso, periodo):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {SCHEMA};")

        cur.execute("""
            UPDATE aluno
            SET nome = %s,
                curso = %s,
                periodo = %s
            WHERE id = %s
        """, (nome, curso, periodo, int(id_aluno)))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        raise e



def atualizar_senha(id_aluno, senha_atual, nova_senha):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {SCHEMA};")

        # Busca o hash da senha atual
        cur.execute("SELECT senha FROM aluno WHERE id = %s", (id_aluno,))
        resultado = cur.fetchone()

        if not resultado:
            raise Exception("Aluno não encontrado.")

        senha_hash_atual = resultado[0]

        # Verifica se a senha atual está correta
        if not check_password_hash(senha_hash_atual, senha_atual):
            raise Exception("Senha atual incorreta.")

        nova_hash = generate_password_hash(nova_senha)

        cur.execute("UPDATE aluno SET senha = %s WHERE id = %s", (nova_hash, id_aluno))
        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        raise e



if __name__ == "__main__":
    criar_aluno("Marley Abe", "marleyabe@gmail.com", "Ciência de Dados", 6, "senha123")
