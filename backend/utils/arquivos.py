import os
import zipfile
import shutil

def carregar_arquivo(base, pasta_id, arquivo, nome):
    extensao = os.path.splitext(arquivo.filename)[1].lower()
    pasta_destino = os.path.join(base, pasta_id)
    os.makedirs(pasta_destino, exist_ok=True)

    caminho_arquivo = os.path.join(pasta_destino, f"{nome}{extensao}")
    arquivo.save(caminho_arquivo)

    if arquivo.filename.endswith(".zip"):
        with zipfile.ZipFile(caminho_arquivo, 'r') as zip_ref:
            zip_ref.extractall(pasta_destino)
        os.remove(caminho_arquivo)


    return "arquivo carregado com sucesso!"


def remover_arquivo(base, pasta_id):
    pasta_relatorio = os.path.join(base, pasta_id)
    print(pasta_relatorio)
    if os.path.exists(pasta_relatorio):
        shutil.rmtree(pasta_relatorio)