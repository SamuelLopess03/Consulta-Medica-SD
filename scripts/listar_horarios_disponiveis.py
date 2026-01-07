#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Listar Horários Disponíveis
"""

import sys
import requests
from utils import Colors, print_header, print_success, print_error, print_info

API_URL = "http://localhost:8080/api/agendamentos/horarios"

def listar_horarios(medico_id, especialidade):
    try:
        print_info(f"Buscando horários para Médico ID {medico_id} ({especialidade})...")
        response = requests.get(
            API_URL, 
            params={"medicoId": medico_id, "especialidade": especialidade},
            timeout=10
        )
        
        if response.status_code == 200:
            horarios = response.json()
            if not horarios:
                print(f"\n{Colors.YELLOW}Nenhum horário encontrado.{Colors.END}")
                return
            
            print(f"\n{Colors.BOLD}Horários Disponíveis:{Colors.END}")
            for h in horarios:
                print(f"  📅 {h.get('data')} | ⏰ {h.get('horaInicio')} - {h.get('horaFim')}")
        else:
            print_error(f"Erro ao buscar horários! Status: {response.status_code}")
    except Exception as e:
        print_error(f"Erro: {str(e)}")

def main():
    try:
        print_header("LISTAR HORÁRIOS DISPONÍVEIS")
        
        if len(sys.argv) > 1:
            if len(sys.argv) != 3:
                print("Uso: python listar_horarios_disponiveis.py <medico_id> <especialidade>")
                return
            listar_horarios(sys.argv[1], sys.argv[2])
        else:
            medico_id = input(f"{Colors.CYAN}ID do Médico: {Colors.END}").strip()
            especialidade = input(f"{Colors.CYAN}Especialidade: {Colors.END}").strip()
            listar_horarios(medico_id, especialidade)
            
    except KeyboardInterrupt:
        print("\nCancelado.")

if __name__ == "__main__":
    main()