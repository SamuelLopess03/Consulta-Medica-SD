import sys
import requests

API_URL = "http://localhost:8080/doctors/schedule"

def cadastrar_horario(doctor_id, data, hora_inicio, hora_fim, disponivel=True):
    payload = {
        "doctor_id": doctor_id,
        "date": data,
        "start_time": hora_inicio,
        "end_time": hora_fim,
        "available": disponivel
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
    if len(sys.argv) != 5:
        print(
            "Uso:\n"
            "python cadastrar_horario_doutor.py <doctor_id> <data> <hora_inicio> <hora_fim>"
        )
        sys.exit(1)

    doctor_id = sys.argv[1]
    data = sys.argv[2]
    hora_inicio = sys.argv[3]
    hora_fim = sys.argv[4]

    cadastrar_horario(doctor_id, data, hora_inicio, hora_fim)