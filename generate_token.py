import jwt
from datetime import datetime, timedelta

SECRET_KEY = 'sua_chave_secreta_aqui_mude_em_producao'

# Simular usuário ID 2 (Rodolfo)
payload = {
    'user_id': 2,
    'role': 'paciente',
    'exp': datetime.utcnow() + timedelta(hours=24)
}

token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
# Se jwt.encode retornar bytes, decodificar. Em versões novas do PyJWT retorna string.
if isinstance(token, bytes):
    token = token.decode('utf-8')

print(token)
