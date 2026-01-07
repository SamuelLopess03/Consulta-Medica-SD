#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Autenticar e Obter Token
Sistema de Consultas Médicas - Sistemas Distribuídos
"""

import sys
import requests
import json

# Configuração da API
API_URL = "http://localhost:5000/users/authenticate"

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def autenticar(email, senha):
    """Autentica usuário e retorna o token"""
    payload = {
        "email": email,
        "password": senha
    }
    
    try:
        response = requests.post(
            API_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            user = data.get('user', {})
            
            print(f"{Colors.GREEN}✅ Autenticação bem-sucedida!{Colors.END}")
            print(f"\n{Colors.BOLD}Token:{Colors.END}")
            print(token)
            print(f"\n{Colors.BOLD}Usuário:{Colors.END}")
            print(f"  ID:   {user.get('id')}")
            print(f"  Nome: {user.get('name')}")
            print(f"  Role: {user.get('role')}")
            print()
            
            return token
        else:
            print(f"{Colors.RED}❌ Falha na autenticação! Status: {response.status_code}{Colors.END}")
            try:
                print(f"Resposta: {response.json()}")
            except:
                print(f"Resposta: {response.text}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"{Colors.RED}❌ Não foi possível conectar à API!{Colors.END}")
        print(f"{Colors.YELLOW}ℹ️  Verifique se os serviços estão rodando: docker compose ps{Colors.END}")
        return None
    except Exception as e:
        print(f"{Colors.RED}❌ Erro: {str(e)}{Colors.END}")
        return None

def main():
    """Função principal"""
    if len(sys.argv) != 3:
        print(f"{Colors.YELLOW}Uso:{Colors.END}")
        print("  python obter_token.py <email> <senha>")
        print(f"\n{Colors.YELLOW}Exemplo:{Colors.END}")
        print('  python obter_token.py "admin@email.com" "senha123"')
        print()
        sys.exit(1)
    
    email = sys.argv[1]
    senha = sys.argv[2]
    
    token = autenticar(email, senha)
    
    if token:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
