import sys
import requests

def excluir_usuario(usuario_id):
    API_URL = f"http://localhost:5000/users/{usuario_id}"
    
    response = requests.delete(API_URL)
    
    if response.status_code == 204:
        print(f"✅ Usuário ID {usuario_id} excluído com sucesso!")
    elif response.status_code == 404:
        print(f"❌ Usuário não encontrado (ID: {usuario_id})")
    else:
        try:
            print("Status:", response.status_code)
            print("Resposta:", response.json())
        except Exception:
            print("Resposta bruta:", response.text)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(
            "Uso:\n"
            "python excluir_usuario.py <usuario_id>"
        )
        sys.exit(1)

    usuario_id = sys.argv[1]
    excluir_usuario(usuario_id)