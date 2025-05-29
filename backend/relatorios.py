from flask import Blueprint, request, jsonify
import os
import subprocess
import socket
import time
import jwt
import psutil
import uuid
from db.relatorios import salvar_relatorio, editar_relatorio, listar_relatorios_paginado, listar_relatorios_por_aluno, deletar_relatorio, buscar_relatorio
from flask import Blueprint, jsonify
import shutil
import zipfile

def matar_processos_na_porta(porta):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == porta:
                    proc.terminate()
                    proc.wait(timeout=5)
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


relatorios_bp = Blueprint("relatorios", __name__)
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "chave_padrao")
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "streamlit_apps")

@relatorios_bp.route("/api/relatorios", methods=["POST"])
def publicar_relatorio():
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"erro": "Token JWT ausente ou inválido"}), 401

    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        aluno_id = payload.get("id")

        if "arquivo" not in request.files or "assunto" not in request.form or "titulo" not in request.form:
            return jsonify({"erro": "Arquivo zip e assunto são obrigatórios"}), 400


        # TODO: Refatorar essas decisões
        arquivo = request.files["arquivo"]
        if not arquivo:
            return jsonify({"erro": "Arquivo zip é obrigatório"}), 400
        capa = request.files.get("capa")
        if not capa:
            return jsonify({"erro": "Capa é obrigatória"}), 400
        titulo = request.form["titulo"]
        if not titulo:
            return jsonify({"erro": "Título é obrigatório"}), 400
        descricao = request.form["descricao"]
        if not descricao:
            return jsonify({"erro": "Descrição é obrigatória"}), 400
        assunto = request.form["assunto"]
        if not assunto:
            return jsonify({"erro": "Assunto é obrigatório"}), 400

        if not arquivo.filename.endswith(".zip"):
            return jsonify({"erro": "O arquivo deve ser .zip"}), 400

        # Cria subpasta única para o relatório
        pasta_id = uuid.uuid4().hex
        pasta_destino = os.path.join(UPLOAD_FOLDER, pasta_id)
        os.makedirs(pasta_destino, exist_ok=True)

        # Salva o arquivo como relatorio.html
        caminho_arquivo = os.path.join(pasta_destino, "relatorio.zip")
        arquivo.save(caminho_arquivo)

        with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
            zip_ref.extractall(pasta_destino)

        os.remove(caminho_arquivo)

        extensao = os.path.splitext(capa.filename)[1].lower()
        pasta_destino = os.path.join("backend/static", pasta_id)  
        os.makedirs(pasta_destino, exist_ok=True) 

        caminho_arquivo = os.path.join(pasta_destino, f"capa{extensao}")
        capa.save(caminho_arquivo)


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
    


@relatorios_bp.route("/api/relatorios/<int:relatorio_id>", methods=["GET"])
def obter_relatorio(relatorio_id):
    try:
        relatorio = buscar_relatorio(relatorio_id)
        if not relatorio:
            return jsonify({"erro": "Relatório não encontrado"}), 404

        pasta_id = relatorio["caminho_pasta"]  # ou o campo equivalente
        pasta_absoluta = os.path.join(UPLOAD_FOLDER, pasta_id)

        if not os.path.exists(pasta_absoluta):
            return jsonify({"erro": "Pasta do relatório não encontrada"}), 404

        # Buscar o primeiro .py dentro da pasta
        app_py = None
        for root, dirs, files in os.walk(pasta_absoluta):
            for file in files:
                if file.endswith(".py"):
                    app_py = os.path.join(root, file)
                    break
            if app_py:
                break

        if not app_py:
            return jsonify({"erro": "Nenhum app .py encontrado na pasta"}), 400
        
        matar_processos_na_porta(8501)

        # Iniciar o Streamlit em uma porta aleatória
        subprocess.Popen([
            "streamlit", "run", app_py,
            "--server.headless", "true",
            "--server.port", str(8501),
            "--server.baseUrlPath", f"relatorio/{relatorio_id}"
        ])

        #esperar a porta estar disponível
        while True:
            try:
                socket.create_connection(("localhost", 8501))

                return jsonify({
                    "relatorio": relatorio,
                    }), 200
            
            except socket.error:
                time.sleep(0.5)
                
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
