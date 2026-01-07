#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Interativo para Cadastro de Agendamentos
"""

import sys
import requests
import json
from datetime import datetime
from utils import Colors, print_header, print_success, print_error, print_info

# Configurações
API_AGENDAMENTO = "http://localhost:8080/api/agendamentos"
API_USUARIOS = "http://localhost:5000/users"

def listar_medicos():
    """Busca e lista médicos disponíveis"""
    try:
        response = requests.get(API_USUARIOS, params={"role": "DOCTOR"}, timeout=5)
        if response.status_code == 200:
            data = response.json()
            users = data.get('users', data.get('data', [])) if isinstance(data, dict) else data
            # Filtrar manual caso a API não filtre
            return [u for u in users if u.get('role') == 'DOCTOR']
        return []
    except:
        return []

def solicitar_dados_interativo():
    """Solicita dados via prompt interativo"""
    print(f"{Colors.BLUE}Preencha os dados do agendamento:{Colors.END}\n")
    
    # 1. Paciente
    paciente_id = input(f"{Colors.CYAN}ID do Paciente: {Colors.END}").strip()
    paciente_email = input(f"{Colors.CYAN}Email do Paciente: {Colors.END}").strip()
    
    # 2. Médico (Oferecer lista)
    print(f"\n{Colors.YELLOW}Buscando médicos...{Colors.END}")
    medicos = listar_medicos()
    
    medico_id = ""
    medico_email = ""
    
    if medicos:
        print(f"{Colors.BOLD}Médicos Disponíveis:{Colors.END}")
        for m in medicos:
            print(f"  ID: {m['id']} - {m['name']} ({m['email']})")
        print()
        medico_id = input(f"{Colors.CYAN}ID do Médico: {Colors.END}").strip()
        
        # Tentar achar email automaticamente
        selected = next((m for m in medicos if str(m['id']) == medico_id), None)
        if selected:
            medico_email = selected['email']
            print(f"{Colors.GREEN}Email do médico selecionado automaticamente: {medico_email}{Colors.END}")
        else:
            medico_email = input(f"{Colors.CYAN}Email do Médico: {Colors.END}").strip()
    else:
        print_info("Não foi possível listar médicos. Digite manualmente.")
        medico_id = input(f"{Colors.CYAN}ID do Médico: {Colors.END}").strip()
        medico_email = input(f"{Colors.CYAN}Email do Médico: {Colors.END}").strip()
    
    # 3. Especialidade
    especialidade = input(f"{Colors.CYAN}Especialidade (ex: Cardiologia): {Colors.END}").strip()
    
    # 4. Data e Hora
    while True:
        data_str = input(f"{Colors.CYAN}Data e Hora (DD/MM/AAAA HH:MM): {Colors.END}").strip()
        try:
            dt = datetime.strptime(data_str, "%d/%m/%Y %H:%M")
            data_hora_iso = dt.strftime("%Y-%m-%dT%H:%M:%S")
            break
        except ValueError:
            print_error("Formato inválido! Use DD/MM/AAAA HH:MM")

    return {
        "pacienteId": int(paciente_id),
        "pacienteEmail": paciente_email,
        "medicoId": int(medico_id),
        "medicoEmail": medico_email,
        "especialidade": especialidade,
        "dataHora": data_hora_iso
    }

def cadastrar_agendamento(dados):
    """Envia requisição para criar agendamento"""
    try:
        print_info("Enviando requisição...")
        # Converter IDs para int se forem strings
        dados['pacienteId'] = int(dados['pacienteId'])
        dados['medicoId'] = int(dados['medicoId'])

        response = requests.post(
            API_AGENDAMENTO,
            json=dados,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            result = response.json()
            print_success("Agendamento realizado com sucesso!")
            print(f"\n{Colors.BOLD}Detalhes:{Colors.END}")
            print(f"  ID: {result.get('id')}")
            print(f"  Status: {result.get('status')}")
            print(f"  Data: {result.get('dataHora')}")
            return True
        else:
            print_error(f"Erro ao agendar! Status: {response.status_code}")
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
        print_header("CADASTRO DE AGENDAMENTO")
        
        if len(sys.argv) > 1:
            # Modo CLI (simplificado, assume ISO date)
            if len(sys.argv) < 7:
                print("Uso: python cadastrar_agendamento.py <pid> <pemail> <mid> <memail> <esp> <iso_date>")
                return
            
            dados = {
                "pacienteId": sys.argv[1],
                "pacienteEmail": sys.argv[2],
                "medicoId": sys.argv[3],
                "medicoEmail": sys.argv[4],
                "especialidade": sys.argv[5],
                "dataHora": sys.argv[6]
            }
            cadastrar_agendamento(dados)
        else:
            # Modo Interativo
            dados = solicitar_dados_interativo()
            
            print(f"\n{Colors.YELLOW}Confirmar Agendamento?{Colors.END}")
            print(f"  Paciente ID: {dados['pacienteId']}")
            print(f"  Médico ID:   {dados['medicoId']}")
            print(f"  Data:        {dados['dataHora']}")
            
            if input(f"\n{Colors.CYAN}Confirmar (s/n)? {Colors.END}").lower() == 's':
                cadastrar_agendamento(dados)
            else:
                print_info("Operação cancelada.")
                
    except KeyboardInterrupt:
        print("\nCancelado pelo usuário.")

if __name__ == "__main__":
    main()
