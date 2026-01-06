import sys
import requests

def excluir_agendamento(agendamento_id):
    API_URL = f"http://localhost:8080/api/agendamentos/{agendamento_id}"
    
    response = requests.delete(API_URL)
    
    if response.status_code == 200:
        print(f"✅ Agendamento ID {agendamento_id} cancelado com sucesso!")
        try:
            print("Resposta:", response.json())
        except:
            pass
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
            "python excluir_agendamento.py <agendamento_id>"
        )
        sys.exit(1)

    agendamento_id = sys.argv[1]
    excluir_agendamento(agendamento_id)