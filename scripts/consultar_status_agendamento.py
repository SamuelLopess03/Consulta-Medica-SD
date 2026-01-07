#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Consultar Status do Agendamento
"""

import sys
import requests
from utils import Colors, print_header, print_success, print_error, print_info

def consultar_status(agendamento_id):
    API_URL = f"http://localhost:8080/api/agendamentos/{agendamento_id}"
    
    try:
        print_info(f"Consultando agendamento {agendamento_id}...")
        response = requests.get(API_URL, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Agendamento encontrado!")
            print(f"\n{Colors.BOLD}Detalhes:{Colors.END}")
            print(f"  ID:            {data.get('id')}")
            print(f"  Status:        {Colors.MAGENTA}{data.get('status')}{Colors.END}")
            print(f"  Data:          {data.get('dataHora')}")
            print(f"  Paciente:      {data.get('pacienteEmail')}")
            print(f"  Médico:        {data.get('medicoEmail')}")
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