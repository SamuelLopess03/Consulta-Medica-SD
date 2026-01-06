import sys
import requests

def consultar_status(agendamento_id):
    API_URL = f"http://localhost:8080/api/agendamentos/{agendamento_id}"
    
    response = requests.get(API_URL)
    
    if response.status_code == 200:
        print(f"✅ Agendamento ID {agendamento_id}:")
        print(response.json())
    elif response.status_code == 404:
        print(f"❌ Agendamento não encontrado (ID: {agendamento_id})")
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
            "python consultar_status_agendamento.py <agendamento_id>"
        )
        sys.exit(1)

    agendamento_id = sys.argv[1]
    consultar_status(agendamento_id)