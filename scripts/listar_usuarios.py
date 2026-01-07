#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para Listar Usuários Cadastrados
Sistema de Consultas Médicas - Sistemas Distribuídos
"""

import sys
import requests
from typing import List, Dict, Optional
import getpass

# Configuração da API
API_URL = "http://localhost:5000/users"
AUTH_URL = "http://localhost:5000/users/authenticate"

# Cores para output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_header():
    """Imprime o cabeçalho do script"""
    print(f"\n{Colors.CYAN}{Colors.BOLD}{'='*80}")
    print("👥 LISTA DE USUÁRIOS - Sistema de Consultas Médicas")
    print(f"{'='*80}{Colors.END}\n")

def print_error(message):
    """Imprime mensagem de erro"""
    print(f"{Colors.RED}❌ {message}{Colors.END}")

def print_info(message):
    """Imprime mensagem informativa"""
    print(f"{Colors.YELLOW}ℹ️  {message}{Colors.END}")

def print_success(message):
    """Imprime mensagem de sucesso"""
    print(f"{Colors.GREEN}✅ {message}{Colors.END}")

def normalize_role(role: str) -> str:
    """Normaliza o nome da role para inglês (padrão interno)"""
    role = role.upper()
    mapa = {
        "ADMINISTRADOR": "ADMIN",
        "MEDICO": "DOCTOR",
        "PACIENTE": "PATIENT",
        "RECEPCIONISTA": "RECEPTIONIST" 
    }
    return mapa.get(role, role)

def get_role_emoji(role: str) -> str:
    """Retorna emoji correspondente ao tipo de usuário"""
    # Garantir normalização
    role = normalize_role(role)
    emojis = {
        "PATIENT": "👤",
        "DOCTOR": "👨‍⚕️",
        "RECEPTIONIST": "🧑‍💼",
        "ADMIN": "🔧"
    }
    return emojis.get(role, "❓")

def get_role_color(role: str) -> str:
    """Retorna cor correspondente ao tipo de usuário"""
    # Garantir normalização
    role = normalize_role(role)
    cores = {
        "PATIENT": Colors.BLUE,
        "DOCTOR": Colors.GREEN,
        "RECEPTIONIST": Colors.YELLOW,
        "ADMIN": Colors.RED
    }
    return cores.get(role, Colors.END)

def autenticar_usuario(email: Optional[str] = None, senha: Optional[str] = None) -> Optional[str]:
    """Autentica usuário e retorna o token"""
    try:
        # Se não fornecido, solicitar credenciais
        if not email:
            print(f"\n{Colors.BOLD}🔐 Autenticação Necessária{Colors.END}")
            email = input(f"{Colors.CYAN}Email: {Colors.END}").strip()
        
        if not senha:
            senha = getpass.getpass(f"{Colors.CYAN}Senha: {Colors.END}")
        
        payload = {
            "email": email,
            "password": senha
        }
        
        print_info("Autenticando...")
        response = requests.post(
            AUTH_URL,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('token')
            user = data.get('user', {})
            print_success(f"Autenticado como: {user.get('name')} ({user.get('role')})")
            return token
        else:
            print_error("Falha na autenticação!")
            return None
            
    except Exception as e:
        print_error(f"Erro na autenticação: {str(e)}")
        return None

def listar_usuarios(token: Optional[str] = None) -> List[Dict]:
    """Busca todos os usuários da API"""
    try:
        print_info("Buscando usuários...")
        
        headers = {"Content-Type": "application/json"}
        if token:
            headers["Authorization"] = f"Bearer {token}"
        
        response = requests.get(API_URL, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            # Verificar se é uma lista ou um objeto com lista
            if isinstance(data, dict):
                usuarios = data.get('users', data.get('data', []))
            else:
                usuarios = data
            
            return usuarios if isinstance(usuarios, list) else []
        elif response.status_code == 401:
            print_error("Erro de autenticação (401)!")
            print_info("Você precisa estar autenticado para listar usuários.")
            return []
        else:
            print_error(f"Erro ao buscar usuários! Status: {response.status_code}")
            try:
                print(f"Resposta: {response.json()}")
            except:
                print(f"Resposta: {response.text}")
            return []
            
    except requests.exceptions.ConnectionError:
        print_error("Não foi possível conectar à API!")
        print_info("Verifique se os serviços estão rodando:")
        print("  docker compose ps")
        print("  docker compose up -d")
        return []
    except requests.exceptions.Timeout:
        print_error("Timeout ao conectar com a API!")
        return []
    except Exception as e:
        print_error(f"Erro inesperado: {str(e)}")
        return []

def exibir_usuarios_tabela(usuarios: List[Dict]):
    """Exibe os usuários em formato de tabela"""
    if not usuarios:
        print(f"\n{Colors.YELLOW}Nenhum usuário encontrado.{Colors.END}\n")
        return
    
    print(f"\n{Colors.BOLD}Total de usuários: {len(usuarios)}{Colors.END}\n")
    
    # Cabeçalho da tabela (Aumentando espaçamento para compensar cores/emojis)
    print(f"{Colors.BOLD}{'ID':<5} {'Tipo':<25} {'Nome':<25} {'CPF':<15} {'Email':<30} {'Telefone':<15}{Colors.END}")
    print(f"{Colors.BOLD}{'-'*5} {'-'*25} {'-'*25} {'-'*15} {'-'*30} {'-'*15}{Colors.END}")
    
    # Linhas da tabela
    for user in usuarios:
        user_id = str(user.get('id', 'N/A'))
        role = normalize_role(user.get('role', 'UNKNOWN')) # Normalizando
        nome = user.get('name', 'N/A')[:25]
        cpf = user.get('cpf', 'N/A')
        email = user.get('email', 'N/A')[:30]
        telefone = user.get('phone', 'N/A') or 'N/A'
        
        emoji = get_role_emoji(role)
        cor = get_role_color(role)
        role_display = f"{emoji} {role}"
        
        # Imprimindo com formatação manual para evitar quebras com ANSI
        print(f"{user_id:<5} {cor}{role_display:<25}{Colors.END} {nome:<25} {cpf:<15} {email:<30} {telefone:<15}")
    
    print()

def exibir_usuarios_detalhado(usuarios: List[Dict]):
    """Exibe os usuários em formato detalhado"""
    if not usuarios:
        print(f"\n{Colors.YELLOW}Nenhum usuário encontrado.{Colors.END}\n")
        return
    
    print(f"\n{Colors.BOLD}Total de usuários: {len(usuarios)}{Colors.END}\n")
    
    for i, user in enumerate(usuarios, 1):
        user_id = user.get('id', 'N/A')
        role = normalize_role(user.get('role', 'UNKNOWN'))
        emoji = get_role_emoji(role)
        cor = get_role_color(role)
        
        print(f"{Colors.CYAN}{'─'*80}{Colors.END}")
        print(f"{cor}{Colors.BOLD}[{i}] {emoji} {role}{Colors.END}")
        print(f"  ID:       {user_id}")
        print(f"  Nome:     {user.get('name', 'N/A')}")
        print(f"  CPF:      {user.get('cpf', 'N/A')}")
        print(f"  Email:    {user.get('email', 'N/A')}")
        print(f"  Telefone: {user.get('phone', 'N/A') or 'Não informado'}")
    
    print(f"{Colors.CYAN}{'─'*80}{Colors.END}\n")

def exibir_estatisticas(usuarios: List[Dict]):
    """Exibe estatísticas sobre os usuários"""
    if not usuarios:
        return
    
    # Contar por tipo
    contagem = {
        "PATIENT": 0,
        "DOCTOR": 0,
        "RECEPTIONIST": 0,
        "ADMIN": 0
    }
    
    for user in usuarios:
        role = normalize_role(user.get('role', 'UNKNOWN'))
        if role in contagem:
            contagem[role] += 1
    
    print(f"{Colors.BOLD}📊 Estatísticas:{Colors.END}")
    print(f"  {get_role_emoji('PATIENT')} Pacientes:       {contagem['PATIENT']}")
    print(f"  {get_role_emoji('DOCTOR')} Médicos:         {contagem['DOCTOR']}")
    print(f"  {get_role_emoji('RECEPTIONIST')} Recepcionistas:  {contagem['RECEPTIONIST']}")
    print(f"  {get_role_emoji('ADMIN')} Administradores: {contagem['ADMIN']}")
    print()

def filtrar_por_tipo(usuarios: List[Dict], tipo: str) -> List[Dict]:
    """Filtra usuários por tipo"""
    return [u for u in usuarios if u.get('role', '').upper() == tipo.upper()]

def main():
    """Função principal"""
    try:
        print_header()
        
        # Verificar argumentos
        modo_detalhado = False
        filtro_tipo = None
        email = None
        senha = None
        
        i = 1
        while i < len(sys.argv):
            arg = sys.argv[i].upper()
            
            if arg in ['-D', '--DETALHADO', 'DETALHADO']:
                modo_detalhado = True
                i += 1
            elif arg in ['PATIENT', 'DOCTOR', 'RECEPTIONIST', 'ADMIN']:
                filtro_tipo = arg
                i += 1
            elif arg in ['-H', '--HELP', 'HELP']:
                print(f"{Colors.YELLOW}Uso:{Colors.END}")
                print("  python listar_usuarios.py [opções]")
                print(f"\n{Colors.YELLOW}Opções:{Colors.END}")
                print("  -d, --detalhado              Lista em formato detalhado")
                print("  PATIENT                      Filtra apenas pacientes")
                print("  DOCTOR                       Filtra apenas médicos")
                print("  RECEPTIONIST                 Filtra apenas recepcionistas")
                print("  ADMIN                        Filtra apenas administradores")
                print("  --email <email>              Email para autenticação")
                print("  --senha <senha>              Senha para autenticação")
                print(f"\n{Colors.YELLOW}Exemplos:{Colors.END}")
                print("  python listar_usuarios.py")
                print("  python listar_usuarios.py -d")
                print("  python listar_usuarios.py DOCTOR")
                print('  python listar_usuarios.py --email "admin@email.com" --senha "senha123"')
                print()
                return
            elif arg in ['--EMAIL', '-E'] and i + 1 < len(sys.argv):
                email = sys.argv[i + 1]
                i += 2
            elif arg in ['--SENHA', '-S', '--PASSWORD', '-P'] and i + 1 < len(sys.argv):
                senha = sys.argv[i + 1]
                i += 2
            else:
                i += 1
        
        # Autenticar usuário
        token = autenticar_usuario(email, senha)
        if not token:
            print_error("\nNão foi possível autenticar. Abortando.")
            sys.exit(1)
        
        # Buscar usuários
        usuarios = listar_usuarios(token)
        
        if not usuarios:
            sys.exit(1)
        
        # Aplicar filtro se necessário
        if filtro_tipo:
            usuarios_filtrados = filtrar_por_tipo(usuarios, filtro_tipo)
            emoji = get_role_emoji(filtro_tipo)
            print(f"\n{Colors.BOLD}Filtro aplicado: {emoji} {filtro_tipo}{Colors.END}\n")
            usuarios = usuarios_filtrados
        
        # Exibir usuários
        if modo_detalhado:
            exibir_usuarios_detalhado(usuarios)
        else:
            exibir_usuarios_tabela(usuarios)
        
        # Exibir estatísticas
        if not filtro_tipo:
            exibir_estatisticas(usuarios)
        
        sys.exit(0)
        
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}⚠️  Operação cancelada pelo usuário{Colors.END}\n")
        sys.exit(0)
    except Exception as e:
        print_error(f"Erro inesperado: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
