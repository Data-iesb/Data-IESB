import psutil
import subprocess
import socket
import time
from flask import jsonify
import os

def encerrar_porta(porta):
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            for conn in proc.connections(kind='inet'):
                if conn.laddr.port == porta:
                    proc.terminate()
                    proc.wait(timeout=5)
                    break
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue


def buscar_streamlit(pasta_absoluta):
    app_streamlit = None
    for root, dirs, files in os.walk(pasta_absoluta):
        for file in files:
            if file.endswith(".py"):
                app_streamlit = os.path.join(root, file)
                break
        if app_streamlit:
            break

    if not app_streamlit:
        return jsonify({"erro": "Nenhum app.py encontrado na pasta"}), 400
    else:
        return app_streamlit


def iniciar_streamlit(app_streamlit, relatorio):
    subprocess.Popen([
        "streamlit", "run", app_streamlit,
        "--server.headless", "true",
        "--server.port", str(8501),
        "--server.baseUrlPath", f"relatorio/{relatorio["id"]}"
    ])

    while True:
        try:
            socket.create_connection(("localhost", 8501))

            return jsonify({
                "relatorio": relatorio,
                }), 200
        
        except socket.error:
            time.sleep(0.5)

