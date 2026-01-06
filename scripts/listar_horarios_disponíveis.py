import sys
import requests

def listar_horarios_disponiveis(medico_id, especialidade):
    API_URL = "http://localhost:8080/api/agendamentos/horarios"
    
    params = {
        "medicoId": medico_id,
        "especialidade": especialidade
    }

    response = requests.get(
        API_URL,
        params=params,
        headers={"Content-Type": "application/json"}
    )

    try:
        print("Status:", response.status_code)
        horarios = response.json()
        print(f"Horários disponíveis para médico {medico_id}, especialidade {especialidade}:")
        for horario in horarios:
            print(f"  ID: {horario.get('id')}, DataHora: {horario.get('dataHora')}, Disponível: {horario.get('disponivel')}")
    except Exception:
        print("Resposta bruta:", response.text)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Uso:\n"
            "python listar_horarios_disponiveis.py <medico_id> <especialidade>\n"
            "Exemplo:\n"
            "python listar_horarios_disponiveis.py 1 Cardiologia"
        )
        sys.exit(1)

    medico_id = sys.argv[1]
    especialidade = sys.argv[2]

    listar_horarios_disponiveis(medico_id, especialidade)