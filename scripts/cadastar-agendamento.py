import sys
import requests

API_URL = "http://localhost:8080/api/agendamentos"

def cadastrar_agendamento(paciente_id, medico_id, especialidade, data_hora):
    payload = {
        "pacienteId": int(paciente_id),
        "medicoId": int(medico_id),
        "especialidade": especialidade,
        "dataHora": data_hora
    }

    response = requests.post(
        API_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        print("Status:", response.status_code)
        print("Resposta:", response.json())
        return response.json().get('id') if response.status_code == 200 else None
    except Exception:
        print("Resposta bruta:", response.text)
        return None

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Uso:\n"
            "python cadastrar_agendamento.py <paciente_id> <medico_id> <especialidade> <data_hora>\n"
            "Exemplo:\n"
            "python cadastrar_agendamento.py 1 2 Cardiologia 2026-01-10T14:30:00"
        )
        sys.exit(1)

    paciente_id = sys.argv[1]
    medico_id = sys.argv[2]
    especialidade = sys.argv[3]
    data_hora = sys.argv[4]

    cadastrar_agendamento(paciente_id, medico_id, especialidade, data_hora)