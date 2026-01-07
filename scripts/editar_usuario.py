#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Editar Usuário
"""

import sys
import requests
import getpass
from utils import Colors, print_header, print_success, print_error, print_info

API_URL = "http://localhost:5000/users"
AUTH_URL = "http://localhost:5000/users/authenticate"

def autenticar():
    print(f"\n{Colors.YELLOW}🔐 Autenticação Requerida (Admin ou Próprio Usuário){Colors.END}")
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

def editar_usuario(usuario_id, token, dados):
    url = f"{API_URL}/{usuario_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    try:
        print_info("Enviando atualização...")
        response = requests.put(url, json=dados, headers=headers, timeout=10)
        
        if response.status_code == 200:
            print_success("Usuário atualizado com sucesso!")
        else:
            print_error(f"Erro ao atualizar! Status: {response.status_code}")
            try:
                print(response.json())
            except:
                print(response.text)
    except Exception as e:
        print_error(f"Erro: {str(e)}")

def main():
    try:
        print_header("EDITAR USUÁRIO")
        
        token = autenticar()
        if not token:
            return

        usuario_id = input(f"\n{Colors.CYAN}ID do Usuário a editar: {Colors.END}").strip()
        
        print(f"\n{Colors.BOLD}Novos Dados (Deixe em branco para manter):{Colors.END}")
        nome = input(f"{Colors.CYAN}Novo Nome: {Colors.END}").strip()
        email = input(f"{Colors.CYAN}Novo Email: {Colors.END}").strip()
        telefone = input(f"{Colors.CYAN}Novo Telefone: {Colors.END}").strip()
        role = input(f"{Colors.CYAN}Nova Role (PATIENT/DOCTOR/etc): {Colors.END}").strip().upper()
        
        dados = {}
        if nome: dados['name'] = nome
        if email: dados['email'] = email
        if telefone: dados['phone'] = telefone
        if role: dados['role'] = role
        
        if not dados:
            print_info("Nenhuma alteração informada.")
            return

        editar_usuario(usuario_id, token, dados)
            
    except KeyboardInterrupt:
        print("\nCancelado.")

if __name__ == "__main__":
    main()