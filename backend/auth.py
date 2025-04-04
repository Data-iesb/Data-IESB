from flask import Blueprint, request, jsonify
import psycopg2
import jwt
import os
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from db.aluno import criar_aluno, buscar_aluno_por_id, editar_aluno, atualizar_senha


auth_bp = Blueprint("auth", __name__)


DATABASE_URL = os.getenv("DATABASE_URL")
SCHEMA = os.getenv("SCHEMA") 
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")



@auth_bp.route("/api/aluno", methods=["POST"])
def cadastrar_aluno():
    data = request.get_json()

    nome = data.get("nome")
    email = data.get("email")
    curso = data.get("curso")
    periodo = data.get("periodo")
    senha = data.get("senha")

    if not nome or not curso or not periodo or not senha:
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

    try:
        criar_aluno(nome, email, curso, periodo, senha)
        return jsonify({"mensagem": "Aluno cadastrado com sucesso"}), 201
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute(f"SET search_path TO {SCHEMA};")
        cur.execute("SELECT id, senha FROM aluno WHERE email = %s", (email,))
        resultado = cur.fetchone()
        cur.close()
        conn.close()

        if not resultado:
            return jsonify({"erro": "Aluno não encontrado"}), 404

        id_aluno, senha_hash = resultado

        if not check_password_hash(senha_hash, senha):
            return jsonify({"erro": "Senha ou email incorreto"}), 401

        token = jwt.encode({
            "id": id_aluno,
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, JWT_SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@auth_bp.route("/api/aluno/me", methods=["GET"])
def perfil_aluno():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"erro": "Token JWT ausente ou inválido"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        id_aluno = payload.get("id")

        aluno = buscar_aluno_por_id(id_aluno)

        if not aluno:
            return jsonify({"erro": "Aluno não encontrado"}), 404

        return jsonify(aluno), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    


@auth_bp.route("/api/aluno/me", methods=["PUT"])
def atualizar_perfil():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"erro": "Token JWT ausente ou inválido"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        id_aluno = payload.get("id")

        data = request.get_json()
        nome = data.get("nome")
        curso = data.get("curso")
        periodo = data.get("periodo")

        if not nome or not curso or periodo is None:
            return jsonify({"erro": "Nome, curso e período são obrigatórios"}), 400

        editar_aluno(id_aluno, nome, curso, int(periodo))

        return jsonify({"mensagem": "Dados atualizados com sucesso"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    


@auth_bp.route("/api/aluno/senha", methods=["PUT"])
def trocar_senha():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"erro": "Token JWT ausente ou inválido"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        id_aluno = payload.get("id")

        data = request.get_json()
        senha_atual = data.get("senha_atual")
        nova_senha = data.get("nova_senha")

        if not senha_atual or not nova_senha:
            return jsonify({"erro": "Informe a senha atual e a nova senha"}), 400

        atualizar_senha(id_aluno, senha_atual, nova_senha)

        return jsonify({"mensagem": "Senha atualizada com sucesso"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 403 if "incorreta" in str(e) else 500