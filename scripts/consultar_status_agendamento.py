#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Consultar Status do Agendamento
"""

import sys
import requests
from utils import Colors, print_header, print_success, print_error, print_info

def buscar_dados_usuario(user_id):
    """Busca dados do usuário pelo ID (Endpoint user_interface: GET /users/<id>)"""
    if not user_id: return None
    try:
        # Nota: O endpoint GET /users/<id> é público, não requer token!
        response = requests.get(
            f"http://localhost:5000/users/{user_id}",
            timeout=2
        )
        if response.status_code == 200:
            data = response.json()
            # A resposta vem como {'success': True, 'user': {...}}
            return data.get('user')
    except Exception as e:
        pass
    return None

def formatar_usuario(user_id, role_label):
    """Formata a string de exibição do usuário"""
    if not user_id:
        return "Não informado"
    
    dados = buscar_dados_usuario(user_id)
    if dados:
        nome = dados.get('name', 'Desconhecido')
        email = dados.get('email', '')
        return f"{nome} ({email})"
    
    return f"ID {user_id} (Busca falhou)"

def consultar_status(agendamento_id):
    API_URL = f"http://localhost:8080/api/agendamentos/{agendamento_id}"
    
    try:
        print_info(f"Consultando agendamento {agendamento_id}...")
        response = requests.get(API_URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Agendamento encontrado!")
            
            # Tentar enriquecer dados
            # Tentar enriquecer dados
            paciente_str = formatar_usuario(data.get('pacienteId'), "Paciente")
            medico_str = formatar_usuario(data.get('medicoId'), "Médico")
            
            print(f"\n{Colors.BOLD}Detalhes:{Colors.END}")
            print(f"  ID:            {data.get('id')}")
            print(f"  Status:        {Colors.MAGENTA}{data.get('status')}{Colors.END}")
            print(f"  Data:          {data.get('dataHora')}")
            print(f"  Paciente:      {paciente_str}")
            print(f"  Médico:        {medico_str}")
            print(f"  Especialidade: {data.get('especialidade')}")
        elif response.status_code == 404:
            print_error("Agendamento não encontrado!")
        else:
            print_error(f"Erro! Status: {response.status_code}")
    except Exception as e:
        print_error(f"Erro: {str(e)}")

def main():
    try:
        print_header("CONSULTAR STATUS AGENDAMENTO")
        
        if len(sys.argv) > 1:
            consultar_status(sys.argv[1])
        else:
            aid = input(f"{Colors.CYAN}ID do Agendamento: {Colors.END}").strip()
            consultar_status(aid)
            
    except KeyboardInterrupt:
        print("\nCancelado.")

if __name__ == "__main__":
    main()