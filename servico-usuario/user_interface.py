"""
Interface REST para o Serviço de Usuários
Comunica-se com o serviço via Sockets TCP
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import socket
import json
import os

app = Flask(__name__)
CORS(app)

# Configurações
SERVICE_HOST = os.getenv('USER_SERVICE_HOST', 'user_service')
SERVICE_PORT = int(os.getenv('USER_SERVICE_PORT', 5001))

def send_to_service(action, data=None):
    """Envia requisição para o serviço via Socket TCP"""
    try:
        # Criar socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(10)
        
        # Conectar ao serviço
        client_socket.connect((SERVICE_HOST, SERVICE_PORT))
        
        # Preparar mensagem
        message = {
            'action': action,
            'data': data or {}
        }
        
        # Enviar requisição
        message_json = json.dumps(message)
        client_socket.sendall(message_json.encode('utf-8'))
        
        # Receber resposta
        response_data = b''
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            response_data += chunk
            if len(chunk) < 4096:
                break
        
        # Decodificar resposta
        response = json.loads(response_data.decode('utf-8'))
        
        client_socket.close()
        return response
    except socket.timeout:
        return {'success': False, 'message': 'Timeout na comunicação com o serviço'}
    except Exception as e:
        return {'success': False, 'message': f'Erro na comunicação: {str(e)}'}

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({'status': 'healthy', 'service': 'user_interface'}), 200

@app.route('/users', methods=['POST'])
def create_user():
    """Cria um novo usuário"""
    try:
        data = request.json
        
        # Validar campos obrigatórios
        required_fields = ['name', 'cpf', 'email', 'password', 'role']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Campo obrigatório ausente: {field}'
                }), 400
        
        # Enviar para o serviço
        response = send_to_service('create_user', data)
        
        status_code = 201 if response.get('success') else 400
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar requisição: {str(e)}'
        }), 500

@app.route('/users/authenticate', methods=['POST'])
def authenticate():
    """Autentica um usuário"""
    try:
        data = request.json
        
        if 'email' not in data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'Email e senha são obrigatórios'
            }), 400
        
        response = send_to_service('authenticate', data)
        
        status_code = 200 if response.get('success') else 401
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar requisição: {str(e)}'
        }), 500

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Retorna informações de um usuário"""
    try:
        response = send_to_service('get_user', {'user_id': user_id})
        
        status_code = 200 if response.get('success') else 404
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar requisição: {str(e)}'
        }), 500

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Atualiza informações de um usuário"""
    try:
        data = request.json
        data['user_id'] = user_id
        
        # Verificar token de autenticação
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token de autenticação não fornecido'
            }), 401
        
        # Verificar token
        token_response = send_to_service('verify_token', {'token': token})
        if not token_response.get('success'):
            return jsonify({
                'success': False,
                'message': 'Token inválido ou expirado'
            }), 401
        
        response = send_to_service('update_user', data)
        
        status_code = 200 if response.get('success') else 400
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar requisição: {str(e)}'
        }), 500

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Desativa um usuário"""
    try:
        # Verificar token de autenticação
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token de autenticação não fornecido'
            }), 401
        
        # Verificar token
        token_response = send_to_service('verify_token', {'token': token})
        if not token_response.get('success'):
            return jsonify({
                'success': False,
                'message': 'Token inválido ou expirado'
            }), 401
        
        # Verificar se é admin
        payload = token_response.get('payload', {})
        if payload.get('role') != 'administrador':
            return jsonify({
                'success': False,
                'message': 'Permissão negada. Apenas administradores podem excluir usuários.'
            }), 403
        
        response = send_to_service('delete_user', {'user_id': user_id})
        
        status_code = 200 if response.get('success') else 404
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar requisição: {str(e)}'
        }), 500

@app.route('/users', methods=['GET'])
def list_users():
    """Lista usuários com filtros opcionais"""
    try:
        # Verificar token de autenticação
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token de autenticação não fornecido'
            }), 401
        
        # Verificar token
        token_response = send_to_service('verify_token', {'token': token})
        if not token_response.get('success'):
            return jsonify({
                'success': False,
                'message': 'Token inválido ou expirado'
            }), 401
        
        # Obter filtros da query string
        filters = {}
        if 'role' in request.args:
            filters['role'] = request.args.get('role')
        if 'active' in request.args:
            filters['active'] = int(request.args.get('active'))
        
        response = send_to_service('list_users', {'filters': filters})
        
        status_code = 200 if response.get('success') else 400
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar requisição: {str(e)}'
        }), 500

@app.route('/users/verify-token', methods=['POST'])
def verify_token():
    """Verifica a validade de um token"""
    try:
        data = request.json
        
        if 'token' not in data:
            return jsonify({
                'success': False,
                'message': 'Token não fornecido'
            }), 400
        
        response = send_to_service('verify_token', data)
        
        status_code = 200 if response.get('success') else 401
        return jsonify(response), status_code
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao processar requisição: {str(e)}'
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)