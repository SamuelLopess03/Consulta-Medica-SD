#!/usr/bin/env python3
"""
Script de teste automatizado para o Serviço de Usuários
Testa todos os endpoints e funcionalidades principais
"""
import requests
import time
import sys
from typing import Optional

BASE_URL = "http://localhost:5000"
COLORS = {
    'GREEN': '\033[92m',
    'RED': '\033[91m',
    'YELLOW': '\033[93m',
    'BLUE': '\033[94m',
    'END': '\033[0m'
}

class TestRunner:
    def __init__(self):
        self.tests_passed = 0
        self.tests_failed = 0
        self.admin_token = None
        self.user_token = None
    
    def print_header(self, text):
        print(f"\n{COLORS['BLUE']}{'='*60}{COLORS['END']}")
        print(f"{COLORS['BLUE']}{text:^60}{COLORS['END']}")
        print(f"{COLORS['BLUE']}{'='*60}{COLORS['END']}\n")
    
    def print_test(self, test_name):
        print(f"{COLORS['YELLOW']}🧪 Testando: {test_name}{COLORS['END']}")
    
    def print_success(self, message):
        print(f"{COLORS['GREEN']}✅ {message}{COLORS['END']}")
        self.tests_passed += 1
    
    def print_error(self, message):
        print(f"{COLORS['RED']}❌ {message}{COLORS['END']}")
        self.tests_failed += 1
    
    def test_health_check(self):
        """Teste 1: Health Check"""
        self.print_test("Health Check")
        try:
            response = requests.get(f"{BASE_URL}/health", timeout=5)
            if response.status_code == 200:
                self.print_success("API está respondendo")
                return True
            else:
                self.print_error(f"Status inesperado: {response.status_code}")
                return False
        except Exception as e:
            self.print_error(f"Erro ao conectar: {e}")
            return False
    
    def test_create_admin(self):
        """Teste 2: Criar Administrador"""
        self.print_test("Criar Administrador")
        try:
            data = {
                "name": "Admin Teste",
                "cpf": "000.000.000-00",
                "email": "admin_teste@sistema.com",
                "password": "admin123",
                "role": "ADMIN",
                "phone": "85900000000"
            }
            response = requests.post(f"{BASE_URL}/users", json=data)
            if response.status_code == 201 and response.json().get('success'):
                self.print_success("Administrador criado com sucesso")
                return True
            else:
                # Pode já existir, tenta autenticar
                auth_response = requests.post(
                    f"{BASE_URL}/users/authenticate",
                    json={"email": data["email"], "password": data["password"]}
                )
                if auth_response.status_code == 200:
                    self.print_success("Administrador já existe (OK)")
                    return True
                self.print_error(f"Falha ao criar: {response.json().get('message')}")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def test_authenticate_admin(self):
        """Teste 3: Autenticar como Admin"""
        self.print_test("Autenticar Administrador")
        try:
            data = {
                "email": "admin_teste@sistema.com",
                "password": "admin123"
            }
            response = requests.post(f"{BASE_URL}/users/authenticate", json=data)
            if response.status_code == 200 and response.json().get('success'):
                self.admin_token = response.json().get('token')
                self.print_success(f"Autenticação bem-sucedida. Token: {self.admin_token[:20]}...")
                return True
            else:
                self.print_error(f"Falha na autenticação: {response.json().get('message')}")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def test_create_doctor(self):
        """Teste 4: Criar Médico"""
        self.print_test("Criar Médico")
        try:
            data = {
                "name": "Dr. João Teste",
                "cpf": "111.111.111-11",
                "email": "drjoao_teste@email.com",
                "password": "senha123",
                "role": "DOCTOR",
                "phone": "85911111111",
                "crm": "CRM99999",
                "specialty": "Cardiologia"
            }
            response = requests.post(f"{BASE_URL}/users", json=data)
            if response.status_code == 201 and response.json().get('success'):
                self.print_success("Médico criado com sucesso")
                return True
            elif "já cadastrados" in response.json().get('message', ''):
                self.print_success("Médico já existe (OK)")
                return True
            else:
                self.print_error(f"Falha ao criar: {response.json().get('message')}")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def test_create_patient(self):
        """Teste 5: Criar Paciente"""
        self.print_test("Criar Paciente")
        try:
            data = {
                "name": "Maria Teste",
                "cpf": "222.222.222-22",
                "email": "maria_teste@email.com",
                "password": "senha123",
                "role": "PATIENT",
                "phone": "85922222222"
            }
            response = requests.post(f"{BASE_URL}/users", json=data)
            if response.status_code == 201 and response.json().get('success'):
                self.print_success("Paciente criado com sucesso")
                return True
            elif "já cadastrados" in response.json().get('message', ''):
                self.print_success("Paciente já existe (OK)")
                return True
            else:
                self.print_error(f"Falha ao criar: {response.json().get('message')}")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def test_authenticate_patient(self):
        """Teste 6: Autenticar como Paciente"""
        self.print_test("Autenticar Paciente")
        try:
            data = {
                "email": "maria_teste@email.com",
                "password": "senha123"
            }
            response = requests.post(f"{BASE_URL}/users/authenticate", json=data)
            if response.status_code == 200 and response.json().get('success'):
                self.user_token = response.json().get('token')
                self.print_success(f"Autenticação bem-sucedida. Token: {self.user_token[:20]}...")
                return True
            else:
                self.print_error(f"Falha na autenticação: {response.json().get('message')}")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def test_list_all_users(self):
        """Teste 7: Listar Todos os Usuários"""
        self.print_test("Listar Todos os Usuários")
        try:
            if not self.admin_token:
                self.print_error("Token de admin não disponível")
                return False
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{BASE_URL}/users", headers=headers)
            
            if response.status_code == 200 and response.json().get('success'):
                count = response.json().get('count', 0)
                self.print_success(f"Listagem bem-sucedida. Total de usuários: {count}")
                return True
            else:
                self.print_error(f"Falha ao listar: {response.json().get('message')}")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def test_list_doctors_only(self):
        """Teste 8: Listar Apenas Médicos"""
        self.print_test("Listar Apenas Médicos")
        try:
            if not self.admin_token:
                self.print_error("Token de admin não disponível")
                return False
            
            headers = {"Authorization": f"Bearer {self.admin_token}"}
            response = requests.get(f"{BASE_URL}/users?role=DOCTOR", headers=headers)
            
            if response.status_code == 200 and response.json().get('success'):
                count = response.json().get('count', 0)
                self.print_success(f"Listagem bem-sucedida. Total de médicos: {count}")
                return True
            else:
                self.print_error(f"Falha ao listar: {response.json().get('message')}")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def test_get_user(self):
        """Teste 9: Buscar Usuário Específico"""
        self.print_test("Buscar Usuário por ID")
        try:
            response = requests.get(f"{BASE_URL}/users/1")
            
            if response.status_code == 200 and response.json().get('success'):
                user = response.json().get('user', {})
                self.print_success(f"Usuário encontrado: {user.get('name')}")
                return True
            else:
                self.print_error(f"Falha ao buscar: {response.json().get('message')}")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def test_update_user(self):
        """Teste 10: Atualizar Usuário"""
        self.print_test("Atualizar Dados do Usuário")
        try:
            if not self.user_token:
                self.print_error("Token de usuário não disponível")
                return False
            
            headers = {"Authorization": f"Bearer {self.user_token}"}
            data = {
                "phone": "85999999999"
            }
            
            # Assumindo que o paciente criado tem ID 3 (ou buscar dinâmicamente)
            response = requests.put(f"{BASE_URL}/users/3", json=data, headers=headers)
            
            if response.status_code == 200 and response.json().get('success'):
                self.print_success("Usuário atualizado com sucesso")
                return True
            else:
                self.print_error(f"Falha ao atualizar: {response.json().get('message')}")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def test_invalid_authentication(self):
        """Teste 11: Autenticação com Credenciais Inválidas"""
        self.print_test("Autenticação com Credenciais Inválidas")
        try:
            data = {
                "email": "invalido@email.com",
                "password": "senhaerrada"
            }
            response = requests.post(f"{BASE_URL}/users/authenticate", json=data)
            
            if response.status_code == 401 and not response.json().get('success'):
                self.print_success("Autenticação rejeitada corretamente")
                return True
            else:
                self.print_error("Sistema permitiu autenticação inválida!")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def test_unauthorized_delete(self):
        """Teste 12: Tentar Deletar sem Permissão"""
        self.print_test("Tentativa de Exclusão sem Permissão de Admin")
        try:
            if not self.user_token:
                self.print_error("Token de usuário não disponível")
                return False
            
            headers = {"Authorization": f"Bearer {self.user_token}"}
            response = requests.delete(f"{BASE_URL}/users/1", headers=headers)
            
            if response.status_code == 403:
                self.print_success("Acesso negado corretamente (apenas admin pode deletar)")
                return True
            else:
                self.print_error("Sistema permitiu exclusão sem permissão!")
                return False
        except Exception as e:
            self.print_error(f"Erro: {e}")
            return False
    
    def run_all_tests(self):
        """Executa todos os testes"""
        self.print_header("INICIANDO TESTES DO SERVIÇO DE USUÁRIOS")
        
        print("⏳ Aguardando serviço estar pronto...")
        time.sleep(2)
        
        # Lista de testes
        tests = [
            self.test_health_check,
            self.test_create_admin,
            self.test_authenticate_admin,
            self.test_create_doctor,
            self.test_create_patient,
            self.test_authenticate_patient,
            self.test_list_all_users,
            self.test_list_doctors_only,
            self.test_get_user,
            self.test_update_user,
            self.test_invalid_authentication,
            self.test_unauthorized_delete,
        ]
        
        # Executar testes
        for i, test in enumerate(tests, 1):
            print(f"\n{'─'*60}")
            print(f"Teste {i}/{len(tests)}")
            test()
            time.sleep(0.5)
        
        # Resultado final
        self.print_header("RESULTADO DOS TESTES")
        total = self.tests_passed + self.tests_failed
        
        print(f"Total de testes: {total}")
        print(f"{COLORS['GREEN']}✅ Testes bem-sucedidos: {self.tests_passed}{COLORS['END']}")
        print(f"{COLORS['RED']}❌ Testes falhados: {self.tests_failed}{COLORS['END']}")
        
        if self.tests_failed == 0:
            print(f"\n{COLORS['GREEN']}🎉 TODOS OS TESTES PASSARAM! 🎉{COLORS['END']}\n")
            return 0
        else:
            print(f"\n{COLORS['RED']}⚠️  ALGUNS TESTES FALHARAM ⚠️{COLORS['END']}\n")
            return 1

if __name__ == "__main__":
    runner = TestRunner()
    exit_code = runner.run_all_tests()
    sys.exit(exit_code)