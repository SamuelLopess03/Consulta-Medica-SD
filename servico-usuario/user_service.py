"""
Serviço de Usuários - Servidor Socket TCP
Gerencia todas as operações relacionadas aos usuários
"""
import socket
import json
import threading
import bcrypt
from datetime import datetime, timedelta
import jwt
from models import User, UserRole
from database import get_db, init_db, close_db
from rabbitmq_publisher import publisher

# Configurações
HOST = '0.0.0.0'
PORT = 5001
SECRET_KEY = 'sua_chave_secreta_aqui_mude_em_producao'

class UserService:
    """Serviço de gerenciamento de usuários"""
    
    def __init__(self):
        self.secret_key = SECRET_KEY
        # Conectar ao RabbitMQ
        print("🔄 Conectando ao RabbitMQ...")
        publisher.connect()
    
    def hash_password(self, password):
        """Gera hash da senha"""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password, password_hash):
        """Verifica se a senha está correta"""
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def generate_token(self, user_id, role):
        """Gera token JWT"""
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')
    
    def verify_token(self, token):
        """Verifica token JWT"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def create_user(self, data):
        """Cria um novo usuário"""
        db = get_db()
        try:
            # Verificar se CPF ou email já existem
            existing_user = db.query(User).filter(
                (User.cpf == data['cpf']) | (User.email == data['email'])
            ).first()
            
            if existing_user:
                return {'success': False, 'message': 'CPF ou email já cadastrados'}
            
            # Criar novo usuário
            password_hash = self.hash_password(data['password'])
            
            user = User(
                name=data['name'],
                cpf=data['cpf'],
                email=data['email'],
                password_hash=password_hash,
                role=UserRole[data['role'].upper()],
                phone=data.get('phone'),
                crm=data.get('crm'),
                specialty=data.get('specialty')
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            # Publicar notificação de boas-vindas
            try:
                publisher.publish_notification(
                    email=user.email,
                    assunto='Bem-vindo ao Sistema de Consultas Médicas',
                    mensagem=f'Olá {user.name}! Sua conta foi criada com sucesso. '
                            f'Você está cadastrado como {user.role.value}.'
                )
            except Exception as e:
                print(f"⚠️  Erro ao publicar notificação: {e}")
            
            return {
                'success': True,
                'message': 'Usuário criado com sucesso',
                'user': user.to_dict()
            }
        except Exception as e:
            db.rollback()
            return {'success': False, 'message': f'Erro ao criar usuário: {str(e)}'}
        finally:
            db.close()
    
    def authenticate(self, data):
        """Autentica um usuário"""
        db = get_db()
        try:
            user = db.query(User).filter(User.email == data['email']).first()
            
            if not user:
                return {'success': False, 'message': 'Credenciais inválidas'}
            
            if not user.active:
                return {'success': False, 'message': 'Usuário inativo'}
            
            if not self.verify_password(data['password'], user.password_hash):
                return {'success': False, 'message': 'Credenciais inválidas'}
            
            token = self.generate_token(user.id, user.role.value)
            
            return {
                'success': True,
                'message': 'Autenticação realizada com sucesso',
                'token': token,
                'user': user.to_dict()
            }
        except Exception as e:
            return {'success': False, 'message': f'Erro na autenticação: {str(e)}'}
        finally:
            db.close()
    
    def get_user(self, user_id):
        """Retorna informações de um usuário"""
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {'success': False, 'message': 'Usuário não encontrado'}
            
            return {
                'success': True,
                'user': user.to_dict()
            }
        except Exception as e:
            return {'success': False, 'message': f'Erro ao buscar usuário: {str(e)}'}
        finally:
            db.close()
    
    def update_user(self, user_id, data):
        """Atualiza informações de um usuário"""
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {'success': False, 'message': 'Usuário não encontrado'}
            
            # Atualizar campos permitidos
            if 'name' in data:
                user.name = data['name']
            if 'email' in data:
                # Verificar se email já existe
                existing = db.query(User).filter(
                    User.email == data['email'],
                    User.id != user_id
                ).first()
                if existing:
                    return {'success': False, 'message': 'Email já cadastrado'}
                user.email = data['email']
            if 'phone' in data:
                user.phone = data['phone']
            if 'password' in data:
                user.password_hash = self.hash_password(data['password'])
            if 'crm' in data:
                user.crm = data['crm']
            if 'specialty' in data:
                user.specialty = data['specialty']
            
            user.updated_at = datetime.utcnow()
            
            db.commit()
            db.refresh(user)
            
            # Publicar notificação de atualização
            try:
                publisher.publish_notification(
                    email=user.email,
                    assunto='Dados Atualizados',
                    mensagem=f'Olá {user.name}! Seus dados foram atualizados com sucesso.'
                )
            except Exception as e:
                print(f"⚠️  Erro ao publicar notificação: {e}")
            
            return {
                'success': True,
                'message': 'Usuário atualizado com sucesso',
                'user': user.to_dict()
            }
        except Exception as e:
            db.rollback()
            return {'success': False, 'message': f'Erro ao atualizar usuário: {str(e)}'}
        finally:
            db.close()
    
    def delete_user(self, user_id):
        """Desativa um usuário (soft delete)"""
        db = get_db()
        try:
            user = db.query(User).filter(User.id == user_id).first()
            
            if not user:
                return {'success': False, 'message': 'Usuário não encontrado'}
            
            # Salvar email antes de desativar
            user_email = user.email
            user_name = user.name
            
            user.active = 0
            db.commit()
            
            # Publicar notificação de desativação
            try:
                publisher.publish_notification(
                    email=user_email,
                    assunto='Conta Desativada',
                    mensagem=f'Olá {user_name}! Sua conta foi desativada. '
                            f'Entre em contato com o suporte se precisar de ajuda.'
                )
            except Exception as e:
                print(f"⚠️  Erro ao publicar notificação: {e}")
            
            return {
                'success': True,
                'message': 'Usuário desativado com sucesso'
            }
        except Exception as e:
            db.rollback()
            return {'success': False, 'message': f'Erro ao desativar usuário: {str(e)}'}
        finally:
            db.close()
    
    def list_users(self, filters=None):
        """Lista usuários com filtros opcionais"""
        db = get_db()
        try:
            query = db.query(User)
            
            if filters:
                if 'role' in filters:
                    query = query.filter(User.role == UserRole[filters['role'].upper()])
                if 'active' in filters:
                    query = query.filter(User.active == filters['active'])
            
            users = query.all()
            
            return {
                'success': True,
                'users': [user.to_dict() for user in users],
                'count': len(users)
            }
        except Exception as e:
            return {'success': False, 'message': f'Erro ao listar usuários: {str(e)}'}
        finally:
            db.close()
    
    def handle_request(self, request_data):
        """Processa requisição recebida"""
        action = request_data.get('action')
        data = request_data.get('data', {})
        
        if action == 'create_user':
            return self.create_user(data)
        elif action == 'authenticate':
            return self.authenticate(data)
        elif action == 'get_user':
            return self.get_user(data.get('user_id'))
        elif action == 'update_user':
            return self.update_user(data.get('user_id'), data)
        elif action == 'delete_user':
            return self.delete_user(data.get('user_id'))
        elif action == 'list_users':
            return self.list_users(data.get('filters'))
        elif action == 'verify_token':
            payload = self.verify_token(data.get('token'))
            if payload:
                return {'success': True, 'payload': payload}
            return {'success': False, 'message': 'Token inválido ou expirado'}
        else:
            return {'success': False, 'message': 'Ação não reconhecida'}

def handle_client(client_socket, address, service):
    """Gerencia conexão com um cliente"""
    print(f"Nova conexão de {address}")
    try:
        # Receber dados do cliente
        data = b''
        while True:
            chunk = client_socket.recv(4096)
            if not chunk:
                break
            data += chunk
            if len(chunk) < 4096:
                break
        
        if data:
            # Decodificar mensagem
            message = data.decode('utf-8')
            request_data = json.loads(message)
            
            print(f"Requisição recebida: {request_data.get('action')}")
            
            # Processar requisição
            response = service.handle_request(request_data)
            
            # Enviar resposta
            response_json = json.dumps(response)
            client_socket.sendall(response_json.encode('utf-8'))
            print(f"Resposta enviada para {address}")
    except Exception as e:
        print(f"Erro ao processar requisição de {address}: {e}")
        error_response = json.dumps({'success': False, 'message': str(e)})
        client_socket.sendall(error_response.encode('utf-8'))
    finally:
        client_socket.close()

def start_server():
    """Inicia o servidor socket"""
    print("Inicializando banco de dados...")
    init_db()
    
    print(f"Iniciando Serviço de Usuários em {HOST}:{PORT}")
    service = UserService()
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    
    print(f"Servidor rodando em {HOST}:{PORT}")
    print("Aguardando conexões...")
    
    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address, service)
            )
            client_thread.daemon = True
            client_thread.start()
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
    finally:
        server_socket.close()
        close_db()

if __name__ == '__main__':
    start_server()