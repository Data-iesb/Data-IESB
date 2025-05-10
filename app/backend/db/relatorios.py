import psycopg2
import os
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SCHEMA = os.getenv("SCHEMA")

def salvar_relatorio(nome_pasta, titulo, descricao, assunto, aluno_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {SCHEMA};")

        cur.execute("""
            INSERT INTO relatorio (caminho_pasta, titulo, descricao, assunto, aluno_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (nome_pasta, titulo, descricao, assunto, aluno_id))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        raise e
    


def listar_relatorios_paginado(page=1, limite=12):
    try:
        offset = (page - 1) * limite

        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {SCHEMA};")

        cur.execute("""
            SELECT r.id, r.titulo, r.assunto, r.descricao, r.data_publicacao, r.caminho_pasta, a.id
            FROM relatorio r
            JOIN aluno a ON r.aluno_id = a.id
            ORDER BY r.data_publicacao DESC
            LIMIT %s OFFSET %s
        """, (limite, offset))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        relatorios = []
        for row in rows:
            relatorios.append({
                "id": row[0],
                "titulo": row[1],
                "assunto": row[2],
                "descricao": row[3],
                "data_publicacao": row[4].isoformat(),
                "caminho_pasta": row[5],
                "autor": row[6]
            })

        return relatorios

    except Exception as e:
        raise e
    


def buscar_relatorio(relatorio_id):
    print(type(relatorio_id))
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute(f"SET search_path TO {SCHEMA};")

    cur.execute("""
        SELECT r.id, r.caminho_pasta, r.descricao, r.data_publicacao,
            r.assunto, a.nome AS autor
        FROM relatorio r
        JOIN aluno a ON r.aluno_id = a.id
        WHERE r.id = %s;
    """, (relatorio_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()

    print(row)

    if row:
        return {
            "id": row[0],
            "caminho_pasta": row[1],
            "descricao": row[2],
            "data_publicacao": row[3].isoformat(),
            "assunto": row[4],
            "autor": row[5]
        }
    else:
        return None



def editar_relatorio(relatorio_id, aluno_id, titulo, descricao, assunto):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {SCHEMA};")

        # Verifica se o relatório existe e pertence ao aluno
        cur.execute("SELECT aluno_id FROM relatorio WHERE id = %s", (relatorio_id,))
        resultado = cur.fetchone()

        if not resultado:
            raise Exception("Relatório não encontrado.")
        if resultado[0] != aluno_id:
            raise Exception("Você não tem permissão para editar este relatório.")

        cur.execute("""
            UPDATE relatorio
            SET titulo = %s,
                assunto = %s,
                descricao = %s
            WHERE id = %s
        """, (titulo, assunto, descricao, relatorio_id))

        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        raise e
    


def listar_relatorios_por_aluno(aluno_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {SCHEMA};")

        cur.execute("""
            SELECT id, assunto, descricao, data_publicacao, caminho_pasta
            FROM relatorio
            WHERE aluno_id = %s
            ORDER BY data_publicacao DESC
        """, (aluno_id,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        relatorios = []
        for row in rows:
            relatorios.append({
                "id": row[0],
                "assunto": row[1],
                "descricao": row[2],
                "data_publicacao": row[3].isoformat(),
                "caminho_pasta": row[4]
            })

        return relatorios

    except Exception as e:
        raise e
    


def deletar_relatorio(relatorio_id, aluno_id):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {SCHEMA};")

        # Verifica se o relatório pertence ao aluno
        cur.execute("SELECT caminho_pasta, aluno_id FROM relatorio WHERE id = %s", (relatorio_id,))
        resultado = cur.fetchone()

        if not resultado:
            raise Exception("Relatório não encontrado.")

        caminho_pasta, autor_id = resultado

        if autor_id != aluno_id:
            raise Exception("Você não tem permissão para deletar este relatório.")

        # Exclui do banco
        cur.execute("DELETE FROM relatorio WHERE id = %s", (relatorio_id,))
        conn.commit()

        cur.close()
        conn.close()

        return caminho_pasta  # para exclusão da pasta depois

    except Exception as e:
        raise e
