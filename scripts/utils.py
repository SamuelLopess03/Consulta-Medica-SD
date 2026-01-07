# -*- coding: utf-8 -*-
"""
Utilitários compartilhados para os scripts
"""

import sys
import requests

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header(title):
    """Imprime o cabeçalho do script"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
    print(f"🏥 {title} - Consulta Médica SD")
    print(f"{'='*80}{Colors.END}\n")

def print_success(message):
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def print_error(message):
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.END}")

def get_role_emoji(role):
    emojis = {
        "PATIENT": "👤",
        "DOCTOR": "👨‍⚕️",
        "RECEPTIONIST": "🧑‍💼",
        "ADMIN": "🔧"
    }
    return emojis.get(role, "❓")

def check_service_health(url, service_name):
    try:
        requests.get(url, timeout=2)
        return True
    except:
        print_error(f"Serviço {service_name} parece estar indisponível ({url})")
        return False
