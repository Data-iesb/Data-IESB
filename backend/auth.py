from flask import Blueprint, request, jsonify
import psycopg2
import jwt
import os
from werkzeug.security import check_password_hash
from datetime import datetime, timedelta
from db.aluno import criar_aluno, buscar_aluno_por_id, editar_aluno, atualizar_senha, buscar_aluno_por_email
from flask_cors import cross_origin

from utils.verificar_token import verificar_token

auth_bp = Blueprint("auth", __name__)


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



@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    senha = data.get("senha")

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    try:
        resultado = buscar_aluno_por_email(email)

        if not resultado:
            return jsonify({"erro": "Aluno não encontrado"}), 404

        aluno_id, senha_hash = resultado

        if not check_password_hash(senha_hash, senha):
            return jsonify({"erro": "Senha ou email incorreto"}), 401

        token = jwt.encode({
            "id": aluno_id,
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=1)
        }, JWT_SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@auth_bp.route("/api/aluno/me", methods=["GET"])
@cross_origin()
def perfil_aluno():
    try:
        aluno_id = verificar_token(request)

        aluno = buscar_aluno_por_id(aluno_id)

        if not aluno:
            return jsonify({"erro": "Aluno não encontrado"}), 404

        return jsonify(aluno), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@auth_bp.route("/api/aluno/me", methods=["PUT"])
def atualizar_perfil():
    try:
        aluno_id = verificar_token(request)

        data = request.get_json()
        nome = data.get("nome")
        curso = data.get("curso")
        periodo = data.get("periodo")

        if not nome or not curso or periodo is None:
            return jsonify({"erro": "Nome, curso e período são obrigatórios"}), 400

        editar_aluno(aluno_id, nome, curso, int(periodo))

        return jsonify({"mensagem": "Dados atualizados com sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@auth_bp.route("/api/aluno/senha", methods=["PUT"])
def trocar_senha():
    try:
        aluno_id = verificar_token(request)

        data = request.get_json()
        senha_atual = data.get("senha_atual")
        nova_senha = data.get("nova_senha")

        if not senha_atual or not nova_senha:
            return jsonify({"erro": "Informe a senha atual e a nova senha"}), 400

        atualizar_senha(aluno_id, senha_atual, nova_senha)

        return jsonify({"mensagem": "Senha atualizada com sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 403 if "incorreta" in str(e) else 500
