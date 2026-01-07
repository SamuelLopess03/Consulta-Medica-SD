#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Interativo para Cadastrar Horários de Doutor
"""

import sys
import requests
from datetime import datetime
from utils import Colors, print_header, print_success, print_error, print_info

API_URL = "http://localhost:8080/doctors/schedule"

def cadastrar_horario(dados):
    try:
        print_info("Enviando requisição...")
        response = requests.post(
            API_URL,
            json=dados,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            print_success("Horário cadastrado com sucesso!")
            try:
                print(response.json())
            except:
                pass
            return True
        else:
            print_error(f"Erro ao cadastrar! Status: {response.status_code}")
            try:
                print(response.json())
            except:
                print(response.text)
            return False
    except Exception as e:
        print_error(f"Erro de conexão: {str(e)}")
        return False

def main():
    try:
        print_header("CADASTRO DE HORÁRIO MÉDICO")
        
        if len(sys.argv) > 1:
            if len(sys.argv) != 5:
                print("Uso: python cadastrar_horario_doutor.py <doctor_id> <data> <inicio> <fim>")
                return
            
            dados = {
                "doctor_id": int(sys.argv[1]),
                "date": sys.argv[2],
                "start_time": sys.argv[3],
                "end_time": sys.argv[4],
                "available": True
            }
            cadastrar_horario(dados)
        else:
            # Modo Interativo
            print(f"{Colors.BLUE}Preencha os dados do horário:{Colors.END}\n")
            
            doctor_id = input(f"{Colors.CYAN}ID do Médico: {Colors.END}").strip()
            
            # Data
            while True:
                data_str = input(f"{Colors.CYAN}Data (AAAA-MM-DD): {Colors.END}").strip()
                try:
                    datetime.strptime(data_str, "%Y-%m-%d")
                    break
                except ValueError:
                    print_error("Formato inválido! Use AAAA-MM-DD")
            
            # Horários
            inicio = input(f"{Colors.CYAN}Hora Início (HH:MM): {Colors.END}").strip()
            fim = input(f"{Colors.CYAN}Hora Fim (HH:MM): {Colors.END}").strip()
            
            dados = {
                "doctor_id": int(doctor_id),
                "date": data_str,
                "start_time": inicio,
                "end_time": fim,
                "available": True
            }
            
            if input(f"\n{Colors.CYAN}Confirmar cadastro (s/n)? {Colors.END}").lower() == 's':
                cadastrar_horario(dados)
            else:
                print_info("Cancelado.")
                
    except KeyboardInterrupt:
        print("\nCancelado.")

if __name__ == "__main__":
    main()