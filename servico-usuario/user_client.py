#!/usr/bin/env python3
"""
Script Cliente para interagir com o Serviço de Usuários
Uso: python users_client.py <ação> [parâmetros]
"""
import sys
import requests
import json

BASE_URL = "http://localhost:5000"

def print_response(response):
    """Imprime resposta formatada"""
    try:
        data = response.json()
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(response.text)

def create_user(name, cpf, email, password, role, phone=None, crm=None, specialty=None):
    """Cria um novo usuário"""
    data = {
        "name": name,
        "cpf": cpf,
        "email": email,
        "password": password,
        "role": role,
    }
    
    if phone:
        data["phone"] = phone
    if crm:
        data["crm"] = crm
    if specialty:
        data["specialty"] = specialty
    
    response = requests.post(f"{BASE_URL}/users", json=data)
    print(f"Status: {response.status_code}")
    print_response(response)
    return response

def authenticate(email, password):
    """Autentica um usuário"""
    data = {
        "email": email,
        "password": password
    }
    
    response = requests.post(f"{BASE_URL}/users/authenticate", json=data)
    print(f"Status: {response.status_code}")
    print_response(response)
    
    if response.status_code == 200:
        token = response.json().get('token')
        print(f"\n🔑 Token salvo! Use-o nos próximos comandos.")
        return token
    return None

def get_user(user_id):
    """Busca informações de um usuário"""
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(f"Status: {response.status_code}")
    print_response(response)

def update_user(user_id, token, **kwargs):
    """Atualiza informações de um usuário"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.put(
        f"{BASE_URL}/users/{user_id}",
        json=kwargs,
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print_response(response)

def delete_user(user_id, token):
    """Desativa um usuário"""
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.delete(
        f"{BASE_URL}/users/{user_id}",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print_response(response)

def list_users(token, role=None, active=None):
    """Lista usuários"""
    headers = {"Authorization": f"Bearer {token}"}
    params = {}
    
    if role:
        params["role"] = role
    if active is not None:
        params["active"] = active
    
    response = requests.get(
        f"{BASE_URL}/users",
        params=params,
        headers=headers
    )
    print(f"Status: {response.status_code}")
    print_response(response)

def health_check():
    """Verifica status da API"""
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print_response(response)

def print_usage():
    """Imprime instruções de uso"""
    print("""
Uso: python users_client.py <ação> [parâmetros]

Ações disponíveis:
  health                        - Verifica status da API
  
  create <nome> <cpf> <email> <senha> <role> [telefone] [crm] [especialidade]
                                - Cria novo usuário
                                - Roles: PATIENT, DOCTOR, RECEPTIONIST, ADMIN
  
  auth <email> <senha>          - Autentica e retorna token
  
  get <user_id>                 - Busca informações do usuário
  
  update <user_id> <token> <campo=valor> [campo2=valor2...]
                                - Atualiza usuário
                                - Exemplo: name="João Silva" phone="85999999999"
  
  delete <user_id> <token>      - Desativa usuário (apenas admin)
  
  list <token> [role] [active]  - Lista usuários
                                - role: PATIENT, DOCTOR, RECEPTIONIST, ADMIN
                                - active: 0 ou 1

Exemplos:
  python users_client.py health
  python users_client.py create "João Silva" "123.456.789-00" "joao@email.com" "senha123" "PATIENT" "85999999999"
  python users_client.py create "Dra. Maria" "987.654.321-00" "maria@email.com" "senha123" "DOCTOR" "85988888888" "CRM12345" "Cardiologia"
  python users_client.py auth "joao@email.com" "senha123"
  python users_client.py get 1
  python users_client.py list "seu_token_aqui"
  python users_client.py list "seu_token_aqui" "DOCTOR"
  python users_client.py update 1 "seu_token_aqui" name="João da Silva" phone="85977777777"
  python users_client.py delete 1 "seu_token_aqui"
    """)

def main():
    if len(sys.argv) < 2:
        print_usage()
        return
    
    action = sys.argv[1].lower()
    
    try:
        if action == "health":
            health_check()
        
        elif action == "create":
            if len(sys.argv) < 7:
                print("❌ Erro: Parâmetros insuficientes para criar usuário")
                print("Uso: python users_client.py create <nome> <cpf> <email> <senha> <role> [telefone] [crm] [especialidade]")
                return
            
            name = sys.argv[2]
            cpf = sys.argv[3]
            email = sys.argv[4]
            password = sys.argv[5]
            role = sys.argv[6].upper()
            phone = sys.argv[7] if len(sys.argv) > 7 else None
            crm = sys.argv[8] if len(sys.argv) > 8 else None
            specialty = sys.argv[9] if len(sys.argv) > 9 else None
            
            create_user(name, cpf, email, password, role, phone, crm, specialty)
        
        elif action == "auth":
            if len(sys.argv) < 4:
                print("❌ Erro: Parâmetros insuficientes")
                print("Uso: python users_client.py auth <email> <senha>")
                return
            
            email = sys.argv[2]
            password = sys.argv[3]
            authenticate(email, password)
        
        elif action == "get":
            if len(sys.argv) < 3:
                print("❌ Erro: ID do usuário não fornecido")
                print("Uso: python users_client.py get <user_id>")
                return
            
            user_id = int(sys.argv[2])
            get_user(user_id)
        
        elif action == "update":
            if len(sys.argv) < 5:
                print("❌ Erro: Parâmetros insuficientes")
                print("Uso: python users_client.py update <user_id> <token> <campo=valor> [campo2=valor2...]")
                return
            
            user_id = int(sys.argv[2])
            token = sys.argv[3]
            
            updates = {}
            for arg in sys.argv[4:]:
                if '=' in arg:
                    key, value = arg.split('=', 1)
                    updates[key] = value.strip('"').strip("'")
            
            update_user(user_id, token, **updates)
        
        elif action == "delete":
            if len(sys.argv) < 4:
                print("❌ Erro: Parâmetros insuficientes")
                print("Uso: python users_client.py delete <user_id> <token>")
                return
            
            user_id = int(sys.argv[2])
            token = sys.argv[3]
            delete_user(user_id, token)
        
        elif action == "list":
            if len(sys.argv) < 3:
                print("❌ Erro: Token não fornecido")
                print("Uso: python users_client.py list <token> [role] [active]")
                return
            
            token = sys.argv[2]
            role = sys.argv[3].upper() if len(sys.argv) > 3 else None
            active = int(sys.argv[4]) if len(sys.argv) > 4 else None
            
            list_users(token, role, active)
        
        else:
            print(f"❌ Ação desconhecida: {action}")
            print_usage()
    
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()