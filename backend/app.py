# TODOS
# TODO: Trocar senha do usuario
# TODO: Implementar um usuario administrador
# TODO: Implementar um páginas de controle para administradores

# TODO: Aceitar arquivos diferentes de jpg...
# TODO: Editar Aluno


from flask import Flask, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

from auth import auth_bp
from relatorios import relatorios_bp

def create_app():
    app = Flask(__name__)
    CORS(app, supports_credentials=True, resources={r"/api/*": {"origins": "*"}})

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(relatorios_bp)

    @app.route("/")
    def index():
        return send_from_directory("../frontend", "index.html")

    @app.route("/<path:filename>")
    def frontend_files(filename):
        return send_from_directory("../frontend", filename)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=False, host="0.0.0.0", port=5000)
