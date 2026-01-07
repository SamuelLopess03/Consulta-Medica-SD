#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Editar Agendamento
"""

import sys
import requests
from utils import Colors, print_header, print_success, print_error, print_info

def editar_agendamento(agendamento_id, status):
    API_URL = f"http://localhost:8080/api/agendamentos/{agendamento_id}/status"
    
    try:
        print_info(f"Atualizando agendamento {agendamento_id} para {status}...")
        response = requests.put(
            API_URL, 
            params={"status": status},
            timeout=10
        )
        
        if response.status_code == 200:
            print_success("Status atualizado com sucesso!")
            data = response.json()
            print(f"Novo Status: {Colors.MAGENTA}{data.get('status')}{Colors.END}")
        else:
            print_error(f"Erro ao atualizar! Status: {response.status_code}")
    except Exception as e:
        print_error(f"Erro: {str(e)}")

def main():
    try:
        print_header("EDITAR AGENDAMENTO")
        
        if len(sys.argv) > 1:
            if len(sys.argv) != 3:
                print("Uso: python editar_agendamento.py <id> <status>")
                return
            editar_agendamento(sys.argv[1], sys.argv[2])
        else:
            aid = input(f"{Colors.CYAN}ID do Agendamento: {Colors.END}").strip()
            
            print(f"\n{Colors.BOLD}Novos Status Possíveis:{Colors.END}")
            status_list = ["AGENDADA", "CONFIRMADA", "CANCELADA", "REALIZADA"]
            for i, s in enumerate(status_list, 1):
                print(f"  {i}. {s}")
            
            opcao = input(f"{Colors.CYAN}Escolha (1-4): {Colors.END}").strip()
            try:
                status = status_list[int(opcao)-1]
                editar_agendamento(aid, status)
            except:
                print_error("Opção inválida!")
            
    except KeyboardInterrupt:
        print("\nCancelado.")

if __name__ == "__main__":
    main()