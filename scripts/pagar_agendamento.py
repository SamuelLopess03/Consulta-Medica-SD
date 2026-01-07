#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Pagar Agendamento
"""

import sys
import requests
import json
from utils import Colors, print_header, print_success, print_error, print_info

API_URL = "http://localhost:8000/api/payloads"

def pagar_agendamento(dados):
    try:
        print_info("Processando pagamento...")
        
        # 1. Criar Payload
        response = requests.post(
            API_URL,
            json=dados,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        pagamento_id = None
        
        if response.status_code in [200, 201]:
            data = response.json()
            pagamento_id = data.get('id')
            print_success(f"Pagamento criado! ID: {pagamento_id}")
        else:
            print_error(f"Erro ao criar pagamento! Status: {response.status_code}")
            return
            
        # 2. Confirmar Pagamento
        print_info(f"Confirmando pagamento {pagamento_id}...")
        confirm_url = f"{API_URL}/{pagamento_id}/pay"
        
        conf_response = requests.post(confirm_url, timeout=10)
        
        if conf_response.status_code in [200, 201]:
            print_success("Pagamento confirmado com sucesso!")
            print(f"\n{Colors.BOLD}Detalhes:{Colors.END}")
            print(f"  Valor: R$ {dados['total']}")
            print(f"  Método: {dados['payment_method']}")
            print(f"  Email: {dados['customer_email']}")
        else:
            print_error(f"Erro ao confirmar! Status: {conf_response.status_code}")
            
    except Exception as e:
        print_error(f"Erro: {str(e)}")

def main():
    try:
        print_header("PAGAMENTO DE AGENDAMENTO")
        
        if len(sys.argv) > 1:
            if len(sys.argv) != 5:
                print("Uso: python pagar_agendamento.py <agendamento_id> <valor> <metodo> <email>")
                return
            dados = {
                "agendamento_id": int(sys.argv[1]),
                "total": float(sys.argv[2]),
                "payment_method": sys.argv[3],
                "customer_email": sys.argv[4]
            }
            pagar_agendamento(dados)
        else:
            agendamento_id = input(f"{Colors.CYAN}ID do Agendamento: {Colors.END}").strip()
            total = input(f"{Colors.CYAN}Valor (ex: 150.00): {Colors.END}").strip()
            
            print(f"\n{Colors.BOLD}Métodos de Pagamento:{Colors.END}")
            print("  1. pix")
            print("  2. credit_card")
            print("  3. debit_card")
            metodo_opt = input(f"{Colors.CYAN}Escolha (1-3): {Colors.END}").strip()
            metodos = {"1": "pix", "2": "credit_card", "3": "debit_card"}
            metodo = metodos.get(metodo_opt, "pix")
            
            email = input(f"{Colors.CYAN}Email do Cliente: {Colors.END}").strip()
            
            dados = {
                "agendamento_id": int(agendamento_id),
                "total": float(total),
                "payment_method": metodo,
                "customer_email": email
            }
            
            if input(f"\n{Colors.CYAN}Confirmar pagamento de R$ {total} via {metodo}? (s/n): {Colors.END}").lower() == 's':
                pagar_agendamento(dados)
            else:
                print_info("Cancelado.")
            
    except KeyboardInterrupt:
        print("\nCancelado.")

if __name__ == "__main__":
    main()