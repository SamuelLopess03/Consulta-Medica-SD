#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de Inicialização Automática do Sistema (Seed)
Executado automaticamente pelo Docker Compose
"""

import time
import requests
import sys
from utils import Colors, print_header, print_success, print_error, print_info

API_USUARIOS = "http://servico-usuario-interface:5000/users"
# Nota: Usamos o nome do serviço no Docker (servico-usuario-interface) em vez de localhost

def esperar_servico(url, nome, max_retries=30):
    print_info(f"Aguardando serviço de {nome} iniciar...")
    for i in range(max_retries):
        try:
            requests.get(f"{url}/health", timeout=2)
            print_success(f"Serviço de {nome} está online!")
            return True
        except:
            time.sleep(2)
            sys.stdout.write(".")
            sys.stdout.flush()
    print_error(f"Timeout aguardando serviço de {nome}")
    return False

def usuario_existe_por_email(email):
    try:
        # Tenta autenticar para verificar existência, ou listagem (mas listagem precisa de token)
        # Vamos assumir que se tentarmos criar e der erro de conflito, já existe.
        # Ou melhor: usar um endpoint de busca se houver, ou apenas tentar criar e tratar o erro 400.
        return False 
    except:
        return False

def criar_usuario_se_nao_existir(nome, cpf, email, senha, role, telefone=None):
    payload = {
        "name": nome,
        "cpf": cpf,
        "email": email,
        "password": senha,
        "role": role,
        "phone": telefone
    }
    
    try:
        print_info(f"Tentando criar usuário: {nome} ({role})...")
        response = requests.post(API_USUARIOS, json=payload, timeout=5)
        
        if response.status_code in [200, 201]:
            print_success(f"Usuário {nome} criado com sucesso!")
            return True
        elif response.status_code == 400 and "já cadastrado" in response.text:
            print_info(f"Usuário {nome} já existe.")
            return True
        else:
            print_error(f"Erro ao criar {nome}: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print_error(f"Erro de conexão ao criar {nome}: {str(e)}")
        return False

def main():
    print_header("INICIALIZAÇÃO DO SISTEMA (SEED)")
    
    # 1. Aguardar Serviço de Usuários
    if not esperar_servico("http://servico-usuario-interface:5000", "Usuários"):
        sys.exit(1)
        
    time.sleep(2) # Margem de segurança
    
    # 2. Criar Usuários Iniciais
    print(f"\n{Colors.BOLD}Populando Banco de Dados...{Colors.END}")
    
    # Admin
    criar_usuario_se_nao_existir(
        "Administrador do Sistema", 
        "000.000.000-00", 
        "admin@email.com", 
        "admin123", 
        "ADMIN"
    )
    
    # Médico Exemplo
    criar_usuario_se_nao_existir(
        "Dr. House", 
        "111.111.111-11", 
        "house@email.com", 
        "senha123", 
        "DOCTOR",
        "85999991111"
    )
    
    # Paciente Exemplo
    criar_usuario_se_nao_existir(
        "Paciente Teste", 
        "222.222.222-22", 
        "paciente@email.com", 
        "senha123", 
        "PATIENT",
        "85988882222"
    )
    
    # Recepcionista Exemplo
    criar_usuario_se_nao_existir(
        "Ana Recepcionista", 
        "333.333.333-33", 
        "ana@email.com", 
        "senha123", 
        "RECEPTIONIST"
    )
    
    print_success("\nInicialização concluída! O sistema está pronto para uso.")

if __name__ == "__main__":
    main()
