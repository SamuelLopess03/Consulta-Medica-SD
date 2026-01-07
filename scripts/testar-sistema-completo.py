import sys
import time
import requests

# Configurações
BASE_URL_USUARIOS = "http://localhost:5000"
BASE_URL_AGENDAMENTO = "http://localhost:8080"
BASE_URL_PAGAMENTOS = "http://localhost:8000"

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_step(step_num, description):
    print(f"\n{Colors.BLUE}{'='*60}")
    print(f"PASSO {step_num}: {description}")
    print(f"{'='*60}{Colors.END}\n")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.END}")

def verificar_servicos():
    """Verifica se todos os serviços estão disponíveis"""
    print_step(0, "Verificando disponibilidade dos serviços")
    
    servicos = {
        "Usuários": f"{BASE_URL_USUARIOS}/health",
        "Agendamento": f"{BASE_URL_AGENDAMENTO}/actuator/health",
        "Pagamentos": f"{BASE_URL_PAGAMENTOS}/api/health"
    }
    
    todos_ok = True
    for nome, url in servicos.items():
        try:
            # Tentar endpoint de health, se não existir, tentar a raiz
            try:
                response = requests.get(url, timeout=5)
            except:
                response = requests.get(url.rsplit('/', 1)[0], timeout=5)
            
            if response.status_code < 500:
                print_success(f"{nome}: Disponível")
            else:
                print_error(f"{nome}: Erro {response.status_code}")
                todos_ok = False
        except Exception as e:
            print_error(f"{nome}: Não disponível - {str(e)}")
            todos_ok = False
    
    if not todos_ok:
        print_error("\nAlguns serviços não estão disponíveis!")
        print_info("Execute: docker compose up -d")
        print_info("Aguarde cerca de 30 segundos e tente novamente.")
        sys.exit(1)
    
    print_success("\nTodos os serviços estão disponíveis!\n")
    time.sleep(1)

def criar_paciente():
    """Cria um paciente de teste"""
    print_step(1, "Criando Paciente")
    
    payload = {
        "name": "Paciente Teste Sistema",
        "cpf": "111.222.333-44",
        "email": "paciente.teste@sistema.com",
        "password": "senha123",
        "role": "PATIENT",
        "phone": "85999999999"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL_USUARIOS}/users",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            user_id = data.get('id') or data.get('user', {}).get('id')
            print_success(f"Paciente criado com ID: {user_id}")
            print_info(f"Email: {payload['email']}")
            return user_id, payload['email']
        else:
            print_error(f"Erro ao criar paciente: {response.status_code}")
            print(response.text)
            return None, None
    except Exception as e:
        print_error(f"Exceção ao criar paciente: {str(e)}")
        return None, None

def criar_medico():
    """Cria um médico de teste"""
    print_step(2, "Criando Médico")
    
    payload = {
        "name": "Dr. Médico Teste",
        "cpf": "555.666.777-88",
        "email": "medico.teste@sistema.com",
        "password": "senha456",
        "role": "DOCTOR",
        "phone": "85988888888"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL_USUARIOS}/users",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            user_id = data.get('id') or data.get('user', {}).get('id')
            print_success(f"Médico criado com ID: {user_id}")
            print_info(f"Email: {payload['email']}")
            return user_id, payload['email']
        else:
            print_error(f"Erro ao criar médico: {response.status_code}")
            print(response.text)
            return None, None
    except Exception as e:
        print_error(f"Exceção ao criar médico: {str(e)}")
        return None, None

def criar_agendamento(paciente_id, paciente_email, medico_id, medico_email):
    """Cria um agendamento de teste"""
    print_step(3, "Criando Agendamento")
    
    payload = {
        "pacienteId": paciente_id,
        "pacienteEmail": paciente_email,
        "medicoId": medico_id,
        "medicoEmail": medico_email,
        "especialidade": "Cardiologia",
        "dataHora": "2026-01-15T14:30:00"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL_AGENDAMENTO}/api/agendamentos",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            agendamento_id = data.get('id')
            print_success(f"Agendamento criado com ID: {agendamento_id}")
            print_info(f"Data/Hora: {payload['dataHora']}")
            print_info(f"Especialidade: {payload['especialidade']}")
            return agendamento_id
        else:
            print_error(f"Erro ao criar agendamento: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print_error(f"Exceção ao criar agendamento: {str(e)}")
        return None

def criar_pagamento(agendamento_id, email_cliente):
    """Cria um pagamento para o agendamento"""
    print_step(4, "Criando Pagamento")
    
    payload = {
        "agendamento_id": agendamento_id,
        "total": 150.00,
        "payment_method": "pix",
        "customer_email": email_cliente
    }
    
    try:
        response = requests.post(
            f"{BASE_URL_PAGAMENTOS}/api/payloads",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            pagamento_id = data.get('id')
            print_success(f"Pagamento criado com ID: {pagamento_id}")
            print_info(f"Valor: R$ {payload['total']:.2f}")
            print_info(f"Método: {payload['payment_method']}")
            return pagamento_id
        else:
            print_error(f"Erro ao criar pagamento: {response.status_code}")
            print(response.text)
            return None
    except Exception as e:
        print_error(f"Exceção ao criar pagamento: {str(e)}")
        return None

def confirmar_pagamento(pagamento_id):
    """Confirma o pagamento"""
    print_step(5, "Confirmando Pagamento")
    
    try:
        response = requests.post(
            f"{BASE_URL_PAGAMENTOS}/api/payloads/{pagamento_id}/pay",
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            status = data.get('status')
            print_success(f"Pagamento confirmado! Status: {status}")
            return True
        else:
            print_error(f"Erro ao confirmar pagamento: {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print_error(f"Exceção ao confirmar pagamento: {str(e)}")
        return False

def main():
    print(f"\n{Colors.BLUE}{'='*60}")
    print("🏥 TESTE COMPLETO DO SISTEMA DE CONSULTAS MÉDICAS")
    print(f"{'='*60}{Colors.END}\n")
    
    # Verificar serviços
    verificar_servicos()
    
    # Criar paciente
    paciente_id, paciente_email = criar_paciente()
    if not paciente_id:
        print_error("\nTeste abortado: Falha ao criar paciente")
        sys.exit(1)
    time.sleep(1)
    
    # Criar médico
    medico_id, medico_email = criar_medico()
    if not medico_id:
        print_error("\nTeste abortado: Falha ao criar médico")
        sys.exit(1)
    time.sleep(1)
    
    # Criar agendamento
    agendamento_id = criar_agendamento(paciente_id, paciente_email, medico_id, medico_email)
    if not agendamento_id:
        print_error("\nTeste abortado: Falha ao criar agendamento")
        sys.exit(1)
    time.sleep(1)
    
    # Criar pagamento
    pagamento_id = criar_pagamento(agendamento_id, paciente_email)
    if not pagamento_id:
        print_error("\nTeste abortado: Falha ao criar pagamento")
        sys.exit(1)
    time.sleep(1)
    
    # Confirmar pagamento
    if not confirmar_pagamento(pagamento_id):
        print_error("\nTeste abortado: Falha ao confirmar pagamento")
        sys.exit(1)
    
    # Resumo final
    print(f"\n{Colors.GREEN}{'='*60}")
    print("✅ TESTE COMPLETO EXECUTADO COM SUCESSO!")
    print(f"{'='*60}{Colors.END}\n")
    
    print_info("Resumo dos IDs criados:")
    print(f"  • Paciente ID: {paciente_id} ({paciente_email})")
    print(f"  • Médico ID: {medico_id} ({medico_email})")
    print(f"  • Agendamento ID: {agendamento_id}")
    print(f"  • Pagamento ID: {pagamento_id}")
    
    print(f"\n{Colors.YELLOW}📧 Verificar Notificações:{Colors.END}")
    print("  Execute: docker logs servico-notificacoes --tail 50")
    print("  Você deve ver mensagens de e-mail enviadas para:")
    print(f"    - {paciente_email}")
    print(f"    - {medico_email}")
    
    print(f"\n{Colors.YELLOW}🐰 Verificar RabbitMQ:{Colors.END}")
    print("  Acesse: http://localhost:15672 (admin/admin)")
    print("  Verifique as mensagens no exchange 'notificacoes_exchange'")
    
    print()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Teste interrompido pelo usuário{Colors.END}\n")
        sys.exit(0)
