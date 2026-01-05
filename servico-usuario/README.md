# Serviço de Usuários - Sistema de Gerenciamento de Consultas Médicas

## 📋 Descrição

Módulo do **Serviço de Usuários** para o sistema de gerenciamento de consultas médicas. Este serviço é responsável por gerenciar todas as operações relacionadas aos usuários, incluindo cadastro, autenticação, autorização e perfis.

## 🏗️ Arquitetura

O módulo é composto por:

1. **Serviço de Usuários** (`user_service.py`) - Socket Server TCP
   - Implementa a lógica de negócio
   - Gerencia operações CRUD de usuários
   - Autentica e autoriza usuários
   - Porta: 5001

2. **Interface REST** (`user_interface.py`) - Socket Client
   - Expõe endpoints REST para o cliente
   - Comunica-se com o serviço via Sockets TCP
   - Porta: 5000

3. **Banco de Dados** (PostgreSQL)
   - Persiste informações dos usuários
   - Porta: 5432

### Comunicação

- **Cliente ↔ Interface REST**: HTTP/REST
- **Interface REST ↔ Serviço**: Sockets TCP (conforme especificação do trabalho)

## 📁 Estrutura de Arquivos

```
user_service/
├── models.py                 # Modelos de dados (SQLAlchemy)
├── database.py              # Configuração do banco de dados
├── user_service.py          # Serviço principal (Socket Server)
├── user_interface.py        # Interface REST (Socket Client)
├── requirements.txt         # Dependências Python
├── Dockerfile.service       # Container do serviço
├── Dockerfile.interface     # Container da interface
├── docker-compose.yml       # Orquestração
└── README.md               # Esta documentação
```

## 🚀 Como Executar

### Pré-requisitos

- Docker e Docker Compose instalados
- Porta 5000, 5001 e 5432 disponíveis

### Inicialização

1. **Clone ou extraia os arquivos do projeto**

2. **Navegue até o diretório do serviço:**
   ```bash
   cd user_service
   ```

3. **Inicie os containers com Docker Compose:**
   ```bash
   docker-compose up --build
   ```

4. **Aguarde os serviços subirem:**
   - O banco de dados será inicializado
   - O serviço de usuários conectará ao banco
   - A interface REST estará disponível

5. **Verifique o status:**
   ```bash
   curl http://localhost:5000/health
   ```

### Parar os Serviços

```bash
docker-compose down
```

Para remover os volumes (dados do banco):
```bash
docker-compose down -v
```

## 📡 Endpoints da API REST

### Health Check
```http
GET /health
```

### Criar Usuário
```http
POST /users
Content-Type: application/json

{
  "name": "João Silva",
  "cpf": "123.456.789-00",
  "email": "joao@email.com",
  "password": "senha123",
  "role": "PATIENT",
  "phone": "85999999999"
}
```

**Roles disponíveis:** `PATIENT`, `DOCTOR`, `RECEPTIONIST`, `ADMIN`

**Campos adicionais para médicos:**
- `crm`: Número do CRM
- `specialty`: Especialidade médica

### Autenticar
```http
POST /users/authenticate
Content-Type: application/json

{
  "email": "joao@email.com",
  "password": "senha123"
}
```

**Resposta:**
```json
{
  "success": true,
  "message": "Autenticação realizada com sucesso",
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

### Buscar Usuário
```http
GET /users/{user_id}
```

### Atualizar Usuário
```http
PUT /users/{user_id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "João da Silva",
  "phone": "85988888888"
}
```

### Desativar Usuário
```http
DELETE /users/{user_id}
Authorization: Bearer {token}
```
⚠️ Apenas administradores podem desativar usuários

### Listar Usuários
```http
GET /users?role=DOCTOR&active=1
Authorization: Bearer {token}
```

**Query Parameters:**
- `role`: Filtrar por tipo (PATIENT, DOCTOR, RECEPTIONIST, ADMIN)
- `active`: Filtrar por status (0 = inativo, 1 = ativo)

### Verificar Token
```http
POST /users/verify-token
Content-Type: application/json

{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

## 🖥️ Script Cliente Python

O script `users_client.py` facilita a interação com o serviço.

### Instalação de Dependências
```bash
pip install requests
```

### Exemplos de Uso

**1. Verificar status:**
```bash
python users_client.py health
```

**2. Criar paciente:**
```bash
python users_client.py create "Maria Santos" "987.654.321-00" "maria@email.com" "senha123" "PATIENT" "85999999999"
```

**3. Criar médico:**
```bash
python users_client.py create "Dr. Carlos" "111.222.333-44" "carlos@email.com" "senha123" "DOCTOR" "85988888888" "CRM12345" "Cardiologia"
```

**4. Autenticar:**
```bash
python users_client.py auth "maria@email.com" "senha123"
```
*Salve o token retornado para usar nos próximos comandos!*

**5. Buscar usuário:**
```bash
python users_client.py get 1
```

**6. Listar todos os médicos:**
```bash
python users_client.py list "SEU_TOKEN_AQUI" "DOCTOR"
```

**7. Atualizar usuário:**
```bash
python users_client.py update 1 "SEU_TOKEN_AQUI" name="Maria Silva Santos" phone="85977777777"
```

**8. Desativar usuário (apenas admin):**
```bash
python users_client.py delete 1 "SEU_TOKEN_AQUI"
```

## 🔐 Segurança

- **Senhas**: Armazenadas com hash bcrypt
- **Autenticação**: JWT com expiração de 24 horas
- **Autorização**: Controle de acesso baseado em roles
- **Soft Delete**: Usuários são desativados, não excluídos

## 🗄️ Modelo de Dados

### Tabela: users

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | Integer | Chave primária |
| name | String(100) | Nome completo |
| cpf | String(14) | CPF (único) |
| email | String(100) | Email (único) |
| password_hash | String(255) | Hash da senha |
| role | Enum | Tipo de usuário |
| phone | String(15) | Telefone |
| crm | String(20) | CRM (apenas médicos) |
| specialty | String(100) | Especialidade (apenas médicos) |
| active | Integer | Status (0=inativo, 1=ativo) |
| created_at | DateTime | Data de criação |
| updated_at | DateTime | Data de atualização |

## 🐛 Troubleshooting

### Erro: "Port already in use"
```bash
# Verifique processos usando as portas
sudo lsof -i :5000
sudo lsof -i :5001
sudo lsof -i :5432

# Pare o Docker Compose e remova containers
docker-compose down
```

### Erro: "Database connection failed"
```bash
# Verifique se o PostgreSQL está rodando
docker-compose ps

# Veja os logs do banco
docker-compose logs db
```

### Erro: "Service not responding"
```bash
# Verifique logs do serviço
docker-compose logs user_service

# Verifique logs da interface
docker-compose logs user_interface

# Reinicie os serviços
docker-compose restart
```

## 📊 Logs

Ver logs em tempo real:
```bash
# Todos os serviços
docker-compose logs -f

# Apenas o serviço de usuários
docker-compose logs -f user_service

# Apenas a interface
docker-compose logs -f user_interface

# Apenas o banco
docker-compose logs -f db
```

## 🧪 Testes

### Teste Completo do Fluxo

```bash
# 1. Verificar health
curl http://localhost:5000/health

# 2. Criar admin
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Admin System",
    "cpf": "000.000.000-00",
    "email": "admin@sistema.com",
    "password": "admin123",
    "role": "ADMIN"
  }'

# 3. Autenticar
curl -X POST http://localhost:5000/users/authenticate \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@sistema.com",
    "password": "admin123"
  }'

# 4. Listar usuários (use o token da resposta anterior)
curl http://localhost:5000/users \
  -H "Authorization: Bearer SEU_TOKEN_AQUI"
```

## 📝 Notas para o Trabalho

### Tecnologias Utilizadas
- ✅ **Sockets TCP**: Comunicação entre Interface e Serviço
- ✅ **REST**: Comunicação entre Cliente e Interface
- ✅ **Docker**: Containerização completa
- ✅ **Docker Compose**: Orquestração do Lado Servidor

### Checklist de Requisitos
- [x] Serviço de Usuários implementado
- [x] Comunicação via Sockets TCP
- [x] Interface REST para o cliente
- [x] Banco de dados PostgreSQL
- [x] Autenticação e autorização
- [x] CRUD completo de usuários
- [x] Dockerfile para cada componente
- [x] Docker Compose para orquestração
- [x] Scripts cliente em Python
- [x] Documentação completa

### Estrutura para Entrega
```
servidor/
├── user_service/
│   ├── models.py
│   ├── database.py
│   ├── user_service.py
│   ├── user_interface.py
│   ├── requirements.txt
│   ├── Dockerfile.service
│   ├── Dockerfile.interface
│   └── README.md
└── docker-compose.yml

cliente/
└── users_client.py
```