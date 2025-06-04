from flask import Blueprint, request, jsonify
import os
import uuid
from db.relatorios import salvar_relatorio, editar_relatorio, listar_relatorios_paginado, listar_relatorios_por_aluno, deletar_relatorio, buscar_relatorio
from flask import Blueprint, jsonify
import shutil

from utils.arquivos import carregar_arquivo, remover_arquivo
from utils.streamlit import encerrar_porta, buscar_streamlit, iniciar_streamlit
from utils.verificar_token import verificar_token

relatorios_bp = Blueprint("relatorios", __name__)

STREAMLIT_FOLDER = os.path.join(os.path.dirname(__file__), "streamlit_apps")
CAPA_FOLDER = "backend/static"

@relatorios_bp.route("/api/relatorios", methods=["POST"])
def publicar_relatorio():
    try:
        aluno_id = verificar_token(request)

        arquivo = request.files["arquivo"]
        assunto = request.form["assunto"]
        capa = request.files.get("capa")
        titulo = request.form["titulo"]
        descricao = request.form["descricao"]

        if not arquivo and not capa and not titulo and not descricao and not assunto:
            return jsonify({"message": "Relatório publicado com sucesso!"}), 200
        elif not arquivo.filename.endswith(".zip"):
            return jsonify({"erro": "O arquivo deve ser .zip"}), 400

        pasta_id = uuid.uuid4().hex
        
        carregar_arquivo(base=STREAMLIT_FOLDER, pasta_id=pasta_id, arquivo=arquivo, nome="relatorio")

        carregar_arquivo(base=CAPA_FOLDER, pasta_id=pasta_id, arquivo=capa, nome="capa")

        salvar_relatorio(pasta_id, titulo, descricao, assunto, aluno_id)

        return jsonify({"mensagem": "Relatório enviado com sucesso"}), 201

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
    try:
        aluno_id = verificar_token(request)

        data = request.get_json()
        titulo = data.get("titulo")
        descricao = data.get("descricao")
        assunto = data.get("assunto")

        if not titulo or not assunto:
            return jsonify({"erro": "Título e assunto são obrigatórios"}), 400

        editar_relatorio(relatorio_id, aluno_id, titulo, descricao, assunto)

        return jsonify({"mensagem": "Relatório atualizado com sucesso"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 403 if "permissão" in str(e) else 500



@relatorios_bp.route("/api/relatorios/me", methods=["GET"])
def listar_meus_relatorios():
    try:
        aluno_id = verificar_token(request)

        relatorios = listar_relatorios_por_aluno(aluno_id)
        return jsonify(relatorios), 200
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@relatorios_bp.route("/api/relatorios/<int:relatorio_id>", methods=["GET"])
def obter_relatorio(relatorio_id):
    try:
        relatorio = buscar_relatorio(relatorio_id)
        if not relatorio:
            return jsonify({"erro": "Relatório não encontrado"}), 404

        pasta_id = relatorio["caminho_pasta"]  # ou o campo equivalente
        pasta_absoluta = os.path.join(STREAMLIT_FOLDER, pasta_id)

        if not os.path.exists(pasta_absoluta):
            return jsonify({"erro": "Pasta do relatório não encontrada"}), 404

        app_streamlit = buscar_streamlit(pasta_absoluta)

        encerrar_porta(8501)

        relatorio = iniciar_streamlit(app_streamlit, relatorio)

        return relatorio
                
    except Exception as e:
        return jsonify({"erro": str(e)}), 500



@relatorios_bp.route("/api/relatorios/<int:relatorio_id>", methods=["DELETE"])
def deletar(relatorio_id):
    try:
        aluno_id = verificar_token(request)

        caminho_pasta = deletar_relatorio(relatorio_id, aluno_id)

        remover_arquivo(STREAMLIT_FOLDER, caminho_pasta) # relatorio
        
        remover_arquivo(CAPA_FOLDER, caminho_pasta) # capa

        return jsonify({"mensagem": "Relatório excluído com sucesso"}), 200
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 500