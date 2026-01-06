import sys
import requests

API_URL = "http://localhost:8000/api/payloads"

def criar_pagamento(agendamento_id, total, metodo_pagamento, email_cliente):
    payload = {
        "agendamento_id": int(agendamento_id),
        "total": float(total),
        "payment_method": metodo_pagamento,
        "customer_email": email_cliente
    }

    response = requests.post(
        API_URL,
        json=payload,
        headers={"Content-Type": "application/json"}
    )

    try:
        print("Status:", response.status_code)
        print("Resposta:", response.json())
        return response.json().get('id') if response.status_code == 201 else None
    except Exception:
        print("Resposta bruta:", response.text)
        return None

def confirmar_pagamento(pagamento_id):
    confirm_url = f"{API_URL}/{pagamento_id}/pay"
    
    response = requests.post(
        confirm_url,
        headers={"Content-Type": "application/json"}
    )

    try:
        print("Status:", response.status_code)
        print("Resposta:", response.json())
        return response.json().get('status') == 'paid'
    except Exception:
        print("Resposta bruta:", response.text)
        return False

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            "Uso:\n"
            "python pagar_agendamento.py <agendamento_id> <total> <metodo_pagamento> <email_cliente>\n\n"
            "Métodos de pagamento: pix, credit_card, debit_card"
        )
        sys.exit(1)

    agendamento_id = sys.argv[1]
    total = sys.argv[2]
    metodo_pagamento = sys.argv[3]
    email_cliente = sys.argv[4]

    print("📝 Criando pagamento...")
    pagamento_id = criar_pagamento(agendamento_id, total, metodo_pagamento, email_cliente)
    
    if pagamento_id:
        print(f"\n💰 Confirmando pagamento ID: {pagamento_id}...")
        confirmado = confirmar_pagamento(pagamento_id)
        
        if confirmado:
            print("✅ Pagamento confirmado com sucesso!")
        else:
            print("❌ Falha ao confirmar pagamento")