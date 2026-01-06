import sys
import requests

def atualizar_status_agendamento(agendamento_id, status):
    API_URL = f"http://localhost:8080/api/agendamentos/{agendamento_id}/status"
    
    response = requests.put(
        API_URL,
        params={"status": status},
        headers={"Content-Type": "application/json"}
    )

    try:
        print("Status:", response.status_code)
        print("Resposta:", response.json())
    except Exception:
        print("Resposta bruta:", response.text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Uso:\n"
            "python editar_agendamento.py <agendamento_id> <status>\n"
            "Status possíveis: AGENDADA, CONFIRMADA, CANCELADA, REALIZADA, etc.\n"
            "Exemplo:\n"
            "python editar_agendamento.py 1 CONFIRMADA"
        )
        sys.exit(1)

    agendamento_id = sys.argv[1]
    status = sys.argv[2]

    atualizar_status_agendamento(agendamento_id, status)