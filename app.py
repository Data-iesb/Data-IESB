from flask import Flask, send_from_directory, render_template
import os

app = Flask(__name__)

# Set the path to your templates folder
TEMPLATES_FOLDER = 'templates'

# Base URL for S3 (update with your actual S3 URL if needed)
S3_BASE_URL = "d28lvm9jkyfotx.cloudfront.net"

@app.route("/")
def index():
    return send_from_directory(TEMPLATES_FOLDER, 'index.html')

@app.route("/relatorios")
def relatorios():
    return send_from_directory(TEMPLATES_FOLDER, 'relatorios.html')

@app.route("/equipe")
def equipe():
    return send_from_directory(TEMPLATES_FOLDER, 'equipe.html')

@app.route("/parceiros")
def parceiros():
    return send_from_directory(TEMPLATES_FOLDER, 'parceiros.html')

@app.route("/login")
def login():
    return send_from_directory(TEMPLATES_FOLDER, 'login.html')

@app.route("/cadastrar")
def cadastrar():
    return send_from_directory(TEMPLATES_FOLDER, 'cadastrar.html')

@app.route("/admin")
def admin():
    return send_from_directory(TEMPLATES_FOLDER, 'admin.html')

if __name__ == "__main__":
    app.run(debug=True)

