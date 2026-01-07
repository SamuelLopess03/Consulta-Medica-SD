#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Excluir Usuário
"""

import sys
import requests
import getpass
from utils import Colors, print_header, print_success, print_error, print_info

API_URL = "http://localhost:5000/users"
AUTH_URL = "http://localhost:5000/users/authenticate"

def autenticar():
    print(f"\n{Colors.YELLOW}🔐 Autenticação Requerida (Admin){Colors.END}")
    email = input(f"{Colors.CYAN}Email: {Colors.END}").strip()
    senha = getpass.getpass(f"{Colors.CYAN}Senha: {Colors.END}")
    
    try:
        response = requests.post(AUTH_URL, json={"email": email, "password": senha}, timeout=5)
        if response.status_code == 200:
            return response.json()['token']
        print_error("Falha na autenticação.")
        return None
    except:
        print_error("Erro ao conectar.")
        return None

def excluir_usuario(usuario_id, token):
    url = f"{API_URL}/{usuario_id}"
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        print_info(f"Excluindo usuário {usuario_id}...")
        response = requests.delete(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print_success("Usuário excluído/desativado com sucesso!")
        else:
            print_error(f"Erro ao excluir! Status: {response.status_code}")
            try:
                print(response.json())
            except:
                print(response.text)
    except Exception as e:
        print_error(f"Erro: {str(e)}")

def main():
    try:
        print_header("EXCLUIR USUÁRIO")
        
        token = autenticar()
        if not token:
            return

        usuario_id = input(f"\n{Colors.CYAN}ID do Usuário a excluir: {Colors.END}").strip()
        
        if input(f"{Colors.RED}Tem certeza? (s/n): {Colors.END}").lower() == 's':
            excluir_usuario(usuario_id, token)
        else:
            print_info("Operação cancelada.")
            
    except KeyboardInterrupt:
        print("\nCancelado.")

if __name__ == "__main__":
    main()