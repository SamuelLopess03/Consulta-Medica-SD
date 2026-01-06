import sys
import requests

def editar_usuario(usuario_id, nome=None, email=None, telefone=None, role=None):
    API_URL = f"http://localhost:5000/users/{usuario_id}"
    
    # Primeiro, obter o usuário atual
    response = requests.get(API_URL)
    
    if response.status_code != 200:
        print(f"❌ Usuário não encontrado (ID: {usuario_id})")
        return
    
    usuario_atual = response.json().get('user', response.json())
    
    # Atualizar apenas os campos fornecidos
    payload = {
        "name": nome or usuario_atual.get('name'),
        "email": email or usuario_atual.get('email'),
        "phone": telefone or usuario_atual.get('phone'),
        "role": role or usuario_atual.get('role')
    }

    response = requests.put(
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
    if len(sys.argv) < 2:
        print(
            "Uso:\n"
            "python editar_usuario.py <usuario_id> [--nome NOME] [--email EMAIL] "
            "[--telefone TELEFONE] [--role ROLE]\n\n"
            "Roles disponíveis: PATIENT, DOCTOR, RECEPTIONIST, ADMIN"
        )
        sys.exit(1)

    usuario_id = sys.argv[1]
    args = sys.argv[2:]
    
    params = {}
    i = 0
    while i < len(args):
        if args[i] == '--nome' and i+1 < len(args):
            params['nome'] = args[i+1]
            i += 2
        elif args[i] == '--email' and i+1 < len(args):
            params['email'] = args[i+1]
            i += 2
        elif args[i] == '--telefone' and i+1 < len(args):
            params['telefone'] = args[i+1]
            i += 2
        elif args[i] == '--role' and i+1 < len(args):
            params['role'] = args[i+1]
            i += 2
        else:
            i += 1

    editar_usuario(usuario_id, **params)