import sys
import requests

API_URL = "http://localhost:5000/users"

def cadastrar_usuario(nome, cpf, email, senha, role, telefone):
    payload = {
        "name": nome,
        "cpf": cpf,
        "email": email,
        "password": senha,
        "role": role,
        "phone": telefone
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
    if len(sys.argv) != 7:
        print(
            "Uso:\n"
            "python cadastrar_usuario_unificado.py <nome> <cpf> <email> <senha> <role> <telefone>\n\n"
            "Roles disponíveis: PATIENT, DOCTOR, RECEPTIONIST, ADMIN"
        )
        sys.exit(1)

    nome = sys.argv[1]
    cpf = sys.argv[2]
    email = sys.argv[3]
    senha = sys.argv[4]
    role = sys.argv[5]
    telefone = sys.argv[6]

    cadastrar_usuario(nome, cpf, email, senha, role, telefone)