#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Interativo para Cadastro de Usuários
Sistema de Consultas Médicas - Sistemas Distribuídos
"""

import sys
import requests

# Configuração da API
API_URL = "http://localhost:5000/users"

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """Imprime o cabeçalho do script"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*60}")
    print("🏥 CADASTRO DE USUÁRIO - Sistema de Consultas Médicas")
    print(f"{'='*60}{Colors.END}\n")

def print_success(message):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    """Imprime mensagem de erro"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    """Imprime mensagem informativa"""
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.END}")

def selecionar_tipo_usuario():
    """Permite ao usuário selecionar o tipo de usuário"""
    print(f"{Colors.BLUE}Tipos de Usuário Disponíveis:{Colors.END}")
    print("  1. 👤 PATIENT (Paciente)")
    print("  2. 👨‍⚕️ DOCTOR (Médico)")
    print("  3. 🧑‍💼 RECEPTIONIST (Recepcionista)")
    print("  4. 🔧 ADMIN (Administrador)")
    print()
    
    tipos = {
        "1": "PATIENT",
        "2": "DOCTOR",
        "3": "RECEPTIONIST",
        "4": "ADMIN"
    }
    
    while True:
        escolha = input(f"{Colors.CYAN}Selecione o tipo de usuário (1-4): {Colors.END}").strip()
        if escolha in tipos:
            return tipos[escolha]
        else:
            print_error("Opção inválida! Escolha entre 1 e 4.")

def obter_dados_usuario():
    """Coleta os dados do usuário de forma interativa"""
    print(f"\n{Colors.BLUE}Preencha os dados do usuário:{Colors.END}\n")
    
    nome = input(f"{Colors.CYAN}Nome completo: {Colors.END}").strip()
    cpf = input(f"{Colors.CYAN}CPF (formato: XXX.XXX.XXX-XX): {Colors.END}").strip()
    email = input(f"{Colors.CYAN}Email: {Colors.END}").strip()
    senha = input(f"{Colors.CYAN}Senha: {Colors.END}").strip()
    telefone = input(f"{Colors.CYAN}Telefone (opcional, ex: 85999999999): {Colors.END}").strip()
    
    return {
        "nome": nome,
        "cpf": cpf,
        "email": email,
        "senha": senha,
        "telefone": telefone if telefone else None
    }

def confirmar_dados(dados, role):
    """Exibe os dados para confirmação"""
    print(f"\n{Colors.YELLOW}{'='*60}")
    print("📋 CONFIRME OS DADOS:")
    print(f"{'='*60}{Colors.END}")
    print(f"  Nome:     {dados['nome']}")
    print(f"  CPF:      {dados['cpf']}")
    print(f"  Email:    {dados['email']}")
    print(f"  Senha:    {'*' * len(dados['senha'])}")
    print(f"  Telefone: {dados['telefone'] or 'Não informado'}")
    print(f"  Tipo:     {role}")
    print()
    
    confirmacao = input(f"{Colors.CYAN}Os dados estão corretos? (s/n): {Colors.END}").strip().lower()
    return confirmacao == 's' or confirmacao == 'sim'

def criar_usuario(nome, cpf, email, senha, role, telefone=None):
    """Envia requisição para criar o usuário"""
    payload = {
        "name": nome,
        "cpf": cpf,
        "email": email,
        "password": senha,
        "role": role
    }
    
    if telefone:
        payload["phone"] = telefone
    
    try:
        print_info("Enviando requisição para a API...")
        response = requests.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            user_id = data.get('id') or data.get('user', {}).get('id')
            
            print(f"\n{Colors.GREEN}{'='*60}")
            print("✅ USUÁRIO CADASTRADO COM SUCESSO!")
            print(f"{'='*60}{Colors.END}")
            print(f"  ID do Usuário: {user_id}")
            print(f"  Nome: {nome}")
            print(f"  Email: {email}")
            print(f"  Tipo: {role}")
            print()
            
            return True
        else:
            print_error(f"Erro ao criar usuário! Status: {response.status_code}")
            print(f"\n{Colors.RED}Resposta da API:{Colors.END}")
            try:
                print(response.json())
            except:
                print(response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API!")
        print_info("Verifique se os serviços estão rodando:")
        print("  docker compose ps")
        print("  docker compose up -d")
        return False
    except requests.exceptions.Timeout:
        print_error("Timeout ao conectar com a API!")
        return False
    except Exception as e:
        print_error(f"Erro inesperado: {str(e)}")
        return False

def modo_interativo():
    """Modo interativo com prompts"""
    print_header()
    
    # Selecionar tipo de usuário
    role = selecionar_tipo_usuario()
    
    # Obter dados do usuário
    dados = obter_dados_usuario()
    
    # Confirmar dados
    if not confirmar_dados(dados, role):
        print_error("Cadastro cancelado pelo usuário.")
        return False
    
    # Criar usuário
    return criar_usuario(
        dados['nome'],
        dados['cpf'],
        dados['email'],
        dados['senha'],
        role,
        dados['telefone']
    )

def modo_linha_comando():
    """Modo de linha de comando (argumentos)"""
    if len(sys.argv) < 6:
        print_error("Argumentos insuficientes!")
        print(f"\n{Colors.YELLOW}Uso:{Colors.END}")
        print(f"  python cadastrar_usuario.py <nome> <cpf> <email> <senha> <role> [telefone]")
        print(f"\n{Colors.YELLOW}Tipos de usuário (role):{Colors.END}")
        print("  • PATIENT      - Paciente")
        print("  • DOCTOR       - Médico")
        print("  • RECEPTIONIST - Recepcionista")
        print("  • ADMIN        - Administrador")
        print(f"\n{Colors.YELLOW}Exemplo:{Colors.END}")
        print('  python cadastrar_usuario.py "João Silva" "123.456.789-00" "joao@email.com" "senha123" "PATIENT" "85999999999"')
        print(f"\n{Colors.CYAN}💡 Dica: Execute sem argumentos para usar o modo interativo!{Colors.END}\n")
        return False
    
    nome = sys.argv[1]
    cpf = sys.argv[2]
    email = sys.argv[3]
    senha = sys.argv[4]
    role = sys.argv[5].upper()
    telefone = sys.argv[6] if len(sys.argv) > 6 else None
    
    # Validar role
    roles_validos = ["PATIENT", "DOCTOR", "RECEPTIONIST", "ADMIN"]
    if role not in roles_validos:
        print_error(f"Tipo de usuário inválido: {role}")
        print_info(f"Tipos válidos: {', '.join(roles_validos)}")
        return False
    
    return criar_usuario(nome, cpf, email, senha, role, telefone)

def main():
    """Função principal"""
    try:
        # Se não houver argumentos, usar modo interativo
        if len(sys.argv) == 1:
            sucesso = modo_interativo()
        else:
            sucesso = modo_linha_comando()
        
        if sucesso:
            sys.exit(0)
        else:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Operação cancelada pelo usuário{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print_error(f"Erro inesperado: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
