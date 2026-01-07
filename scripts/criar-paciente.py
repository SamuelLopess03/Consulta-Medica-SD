import sys
import json
import requests

API_URL = "http://localhost:5000/users"

def criar_usuario(nome, cpf, email, senha, role):
    payload = {
        "name": nome,
        "cpf": cpf,
        "email": email,
        "password": senha,
        "role": role
    }

    response = requests.post(
        API_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        print("Status:", response.status_code)
        print("Resposta:", response.json())
    except Exception:
        print("Resposta bruta:", response.text)


if __name__ == "__main__":
    if len(sys.argv) != 6:
        print(
            "Uso:\n"
            "python criar_usuario.py <nome> <cpf> <email> <senha> <role>"
        )
        sys.exit(1)

    nome = sys.argv[1]
    cpf = sys.argv[2]
    email = sys.argv[3]
    senha = sys.argv[4]
    role = sys.argv[5]

    criar_usuario(nome, cpf, email, senha, role)