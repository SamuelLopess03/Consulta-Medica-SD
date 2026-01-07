#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Excluir Agendamento
"""

import sys
import requests
from utils import Colors, print_header, print_success, print_error, print_info

def excluir_agendamento(agendamento_id):
    API_URL = f"http://localhost:8080/api/agendamentos/{agendamento_id}"
    
    try:
        print_info(f"Excluindo agendamento {agendamento_id}...")
        response = requests.delete(API_URL, timeout=10)
        
        if response.status_code == 200:
            print_success("Agendamento excluído/cancelado com sucesso!")
        else:
            print_error(f"Erro ao excluir! Status: {response.status_code}")
    except Exception as e:
        print_error(f"Erro: {str(e)}")

def main():
    try:
        print_header("EXCLUIR AGENDAMENTO")
        
        if len(sys.argv) > 1:
            excluir_agendamento(sys.argv[1])
        else:
            aid = input(f"{Colors.CYAN}ID do Agendamento para excluir: {Colors.END}").strip()
            if input(f"{Colors.RED}Tem certeza? (s/n): {Colors.END}").lower() == 's':
                excluir_agendamento(aid)
            else:
                print_info("Operação cancelada.")
            
    except KeyboardInterrupt:
        print("\nCancelado.")

if __name__ == "__main__":
    main()