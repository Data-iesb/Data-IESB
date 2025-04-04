from flask import Blueprint, request, jsonify
import os
import jwt
import uuid
from db.relatorios import salvar_relatorio, editar_relatorio, listar_relatorios_paginado, listar_relatorios_por_aluno, deletar_relatorio
from flask import Blueprint, jsonify
import shutil
 
relatorios_bp = Blueprint("relatorios", __name__)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "chave_padrao")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "uploads")

@relatorios_bp.route("/api/relatorios", methods=["POST"])
def publicar_relatorio():
    auth_header = request.headers.get("Authorization")
    print(request)

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"erro": "Token JWT ausente ou inválido"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        aluno_id = payload.get("id")

        if "arquivo" not in request.files or "assunto" not in request.form or "titulo" not in request.form:
            return jsonify({"erro": "Arquivo HTML e assunto são obrigatórios"}), 400

        arquivo = request.files["arquivo"]
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]
        assunto = request.form["assunto"]

        if not arquivo.filename.endswith(".html"):
            return jsonify({"erro": "O arquivo deve ser .html"}), 400

        # Cria subpasta única para o relatório
        pasta_id = uuid.uuid4().hex
        pasta_destino = os.path.join(UPLOAD_FOLDER, pasta_id)
        os.makedirs(pasta_destino, exist_ok=True)

        # Salva o arquivo como relatorio.html
        caminho_arquivo = os.path.join(pasta_destino, "relatorio.html")
        arquivo.save(caminho_arquivo)

        # Salva no banco o nome da pasta (não o caminho completo)
        salvar_relatorio(pasta_id, titulo, descricao, assunto, aluno_id)

        return jsonify({"mensagem": "Relatório enviado com sucesso"}), 201

    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@relatorios_bp.route("/api/relatorios", methods=["GET"])
def listar():
    try:
        page = request.args.get("page", default=1, type=int)
        relatorios = listar_relatorios_paginado(page)
        return jsonify(relatorios), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    

    
@relatorios_bp.route("/api/relatorios/<int:relatorio_id>", methods=["PUT"])
def editar(relatorio_id):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"erro": "Token JWT ausente ou inválido"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        aluno_id = payload.get("id")

        data = request.get_json()
        titulo = data.get("titulo")
        descricao = data.get("descricao")
        assunto = data.get("assunto")

        if not titulo or not assunto:
            return jsonify({"erro": "Título e assunto são obrigatórios"}), 400

        editar_relatorio(relatorio_id, aluno_id, titulo, descricao, assunto)

        return jsonify({"mensagem": "Relatório atualizado com sucesso"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 403 if "permissão" in str(e) else 500
    


@relatorios_bp.route("/api/relatorios/me", methods=["GET"])
def listar_meus_relatorios():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"erro": "Token JWT ausente ou inválido"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        aluno_id = payload.get("id")

        relatorios = listar_relatorios_por_aluno(aluno_id)
        return jsonify(relatorios), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    


@relatorios_bp.route("/api/relatorios/<int:relatorio_id>", methods=["DELETE"])
def deletar(relatorio_id):
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"erro": "Token JWT ausente ou inválido"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        aluno_id = payload.get("id")

        caminho_pasta = deletar_relatorio(relatorio_id, aluno_id)

        # Remove a pasta do relatório fisicamente
        pasta_completa = os.path.join(UPLOAD_FOLDER, caminho_pasta)
        if os.path.exists(pasta_completa):
            shutil.rmtree(pasta_completa)

        return jsonify({"mensagem": "Relatório excluído com sucesso"}), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"erro": "Token inválido"}), 401
    except Exception as e:
        return jsonify({"erro": str(e)}), 403 if "permissão" in str(e) else 500