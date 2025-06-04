import os
import jwt
from flask import jsonify


def verificar_token(request):
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "chave_padrao")
    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        raise ValueError("Token JWT ausente ou inválido")
    
    token = auth_header.split(" ")[1]

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=["HS256"])
        return payload.get("id")
    except jwt.ExpiredSignatureError:
        raise ValueError("Token expirado")
    except jwt.InvalidTokenError:
        raise ValueError("Token inválido")
