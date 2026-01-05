# 🔧 Mudanças Realizadas no Sistema

**Última atualização:** 05/01/2026  
**Versão:** 2.0

---

## 📋 Resumo das Mudanças

Este documento descreve todas as mudanças realizadas no sistema para torná-lo completamente funcional e integrado.

---

## ✅ Estado Atual do Sistema

### Serviços Implementados e Funcionais

| # | Serviço | Tecnologia | Status | Porta(s) | RabbitMQ |
|---|---------|-----------|--------|----------|----------|
| 1 | **RabbitMQ** | Message Broker | ✅ Rodando | 5672, 15672 | - |
| 2 | **MySQL** | Banco de Dados | ✅ Rodando | 3306 | - |
| 3 | **Notificações** | Node.js 18 | ✅ Rodando | - | ✅ Consumer |
| 4 | **Pagamentos** | Laravel 11 (PHP) | ✅ Rodando | 8000 | ✅ Publisher |
| 5 | **Agendamento** | Java Spring Boot | ✅ Rodando | 8080, 9090 | ❌ Não integrado |
| 6 | **Usuários (Service)** | Python 3.11 | ✅ Rodando | 5001 | ✅ Publisher |
| 7 | **Usuários (Interface)** | Python Flask | ✅ Rodando | 5000 | - |

---

## 🆕 Mudanças Principais

### 1. Integração do Serviço de Usuários

**Data:** 05/01/2026

#### Problema Original
- Serviço não iniciava (erro nos Dockerfiles)
- Não estava integrado com RabbitMQ
- Conflito de tabela com Laravel

#### Soluções Implementadas

**a) Dockerfiles Corrigidos**
- ❌ **Antes:** Sintaxe `COPY <<EOF` não funcionava
- ✅ **Depois:** Scripts separados (`start-service.sh`, `start-interface.sh`)

**Arquivos modificados:**
- [`servico-usuario/Dockerfile.service`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/Dockerfile.service)
- [`servico-usuario/Dockerfile.interface`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/Dockerfile.interface)

**Arquivos criados:**
- [`servico-usuario/start-service.sh`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/start-service.sh)
- [`servico-usuario/start-interface.sh`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/start-interface.sh)

**b) Suporte a MySQL**
- ❌ **Antes:** Configurado para PostgreSQL
- ✅ **Depois:** Migrado para MySQL (banco compartilhado)

**Mudanças em [`servico-usuario/database.py`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/database.py):**
```python
# Adicionado
import pymysql
pymysql.install_as_MySQLdb()

# Mudado de PostgreSQL para MySQL
DATABASE_URL = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
```

**Mudanças em [`servico-usuario/requirements.txt`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/requirements.txt):**
```diff
- psycopg2-binary==2.9.9
+ pymysql==1.1.0
+ pika==1.3.2
```

**c) Integração RabbitMQ**
- ❌ **Antes:** Código existia mas não era usado
- ✅ **Depois:** Totalmente integrado

**Mudanças em [`servico-usuario/rabbitmq_publisher.py`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/rabbitmq_publisher.py):**
```python
# Adicionado suporte a credenciais
credentials = pika.PlainCredentials(self.user, self.password)
self.connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=self.host, credentials=credentials)
)

# Adicionado método simplificado
def publish_notification(self, email, assunto, mensagem):
    payload = {
        'email': email,
        'assunto': assunto,
        'mensagem': mensagem
    }
    # ... publicação
```

**Mudanças em [`servico-usuario/user_service.py`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/user_service.py):**
```python
# Adicionado import
from rabbitmq_publisher import publisher

# Adicionado no __init__
def __init__(self):
    self.secret_key = SECRET_KEY
    publisher.connect()  # ← NOVO

# Adicionado em create_user()
publisher.publish_notification(
    email=user.email,
    assunto='Bem-vindo ao Sistema de Consultas Médicas',
    mensagem=f'Olá {user.name}! Sua conta foi criada com sucesso.'
)

# Adicionado em update_user()
publisher.publish_notification(
    email=user.email,
    assunto='Dados Atualizados',
    mensagem=f'Olá {user.name}! Seus dados foram atualizados.'
)

# Adicionado em delete_user()
publisher.publish_notification(
    email=user_email,
    assunto='Conta Desativada',
    mensagem=f'Olá {user_name}! Sua conta foi desativada.'
)
```

**d) Conflito de Tabela Resolvido**
- ❌ **Antes:** Usava tabela `users` (conflito com Laravel)
- ✅ **Depois:** Usa tabela `app_users`

**Mudança em [`servico-usuario/models.py`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/models.py):**
```python
class User(Base):
    __tablename__ = 'app_users'  # ← Era 'users'
```

**e) Docker Compose Atualizado**

**Mudanças em [`docker-compose.yml`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/docker-compose.yml):**
```yaml
# Adicionado serviço usuario-service
usuario-service:
  build:
    context: ./servico-usuario
    dockerfile: Dockerfile.service
  container_name: servico-usuario
  environment:
    DATABASE_URL: mysql://user:userpassword@db:3306/consultamedica
    DB_HOST: db
    DB_PORT: 3306
    DB_NAME: consultamedica
    DB_USER: user
    DB_PASSWORD: userpassword
    RABBITMQ_HOST: rabbitmq  # ← NOVO
  depends_on:
    db:
      condition: service_healthy
    rabbitmq:
      condition: service_healthy  # ← NOVO
  ports:
    - "5001:5001"
  networks:
    - consulta-medica-network
  restart: unless-stopped

# Adicionado serviço usuario-interface
usuario-interface:
  build:
    context: ./servico-usuario
    dockerfile: Dockerfile.interface
  container_name: servico-usuario-interface
  environment:
    USER_SERVICE_HOST: servico-usuario
    USER_SERVICE_PORT: 5001
  depends_on:
    - usuario-service
  ports:
    - "5000:5000"
  networks:
    - consulta-medica-network
  restart: unless-stopped
```

---

## 🔄 Fluxo de Comunicação Atual

### Pagamentos → RabbitMQ → Notificações ✅

```
Cliente → Laravel API → MySQL
                     ↓
                 RabbitMQ → Node.js → SMTP → E-mail
```

**Eventos publicados:**
- Pagamento criado
- Pagamento confirmado
- Pagamento atualizado
- Pagamento cancelado

### Usuários → RabbitMQ → Notificações ✅

```
Cliente → Flask API → Python Service → MySQL
                                     ↓
                                 RabbitMQ → Node.js → SMTP → E-mail
```

**Eventos publicados:**
- Usuário criado (boas-vindas)
- Usuário atualizado
- Usuário desativado

### Agendamento → MySQL ⚠️

```
Cliente → Spring Boot → MySQL
```

**Nota:** Agendamento ainda não publica eventos no RabbitMQ (pode ser adicionado futuramente).

---

## 📁 Arquivos Criados

### Scripts de Teste

1. [`test-pagamento.ps1`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/test-pagamento.ps1)
   - Testa criação, consulta e confirmação de pagamento
   - Verifica integração com notificações

2. [`test-usuario.ps1`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/test-usuario.ps1)
   - Testa criação, autenticação e consulta de usuário
   - Verifica integração com notificações

3. [`iniciar-sistema.ps1`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/iniciar-sistema.ps1)
   - Script automatizado para iniciar todo o sistema
   - Exibe informações úteis e URLs

### Scripts de Inicialização

1. [`servico-usuario/start-service.sh`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/start-service.sh)
   - Aguarda MySQL estar pronto
   - Inicia o serviço de usuários

2. [`servico-usuario/start-interface.sh`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/servico-usuario/start-interface.sh)
   - Aguarda serviço de usuários estar pronto
   - Inicia a interface REST

---

## 🗄️ Estrutura do Banco de Dados

### Tabelas Atuais

| Tabela | Serviço | Descrição |
|--------|---------|-----------|
| `app_users` | Usuários | Dados de usuários (pacientes, médicos, etc.) |
| `consultas` | Agendamento | Consultas agendadas |
| `horarios` | Agendamento | Horários disponíveis dos médicos |
| `payloads` | Pagamentos | Registros de pagamentos |
| `users` | Laravel (interno) | Tabela do Laravel (não usar) |

---

## 🌐 URLs e Portas

### Serviços Externos

| Serviço | URL | Descrição |
|---------|-----|-----------|
| RabbitMQ Management | http://localhost:15672 | Painel de gerenciamento (admin/admin) |
| API Pagamentos | http://localhost:8000 | REST API do Laravel |
| API Agendamento | http://localhost:8080 | REST API do Spring Boot |
| gRPC Agendamento | localhost:9090 | Serviço gRPC |
| API Usuários | http://localhost:5000 | REST API do Flask |

### Serviços Internos (Docker)

| Serviço | Host | Porta |
|---------|------|-------|
| RabbitMQ | rabbitmq | 5672 |
| MySQL | db | 3306 |
| Pagamentos | laravel-api | 8000 |
| Agendamento | servico-agendamento | 8080, 9090 |
| Usuários Service | servico-usuario | 5001 |
| Usuários Interface | servico-usuario-interface | 5000 |

---

## 📊 Comparativo: Antes vs Depois

### Serviço de Usuários

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Status** | ❌ Não iniciava | ✅ Rodando |
| **Banco** | PostgreSQL | MySQL |
| **RabbitMQ** | ❌ Não integrado | ✅ Integrado |
| **Notificações** | ❌ Não enviava | ✅ Envia e-mails |
| **Dockerfiles** | ❌ Sintaxe inválida | ✅ Funcionais |
| **Tabela** | `users` (conflito) | `app_users` |

### Sistema Geral

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Serviços rodando** | 5/7 | 7/7 ✅ |
| **Integração RabbitMQ** | 2 serviços | 3 serviços |
| **Notificações funcionais** | Parcial | Total ✅ |
| **Documentação** | Básica | Completa ✅ |
| **Scripts de teste** | 1 | 3 ✅ |

---

## 🚀 Como Usar as Mudanças

### Para Desenvolvedores

1. **Atualize seu repositório:**
   ```powershell
   git pull origin main
   ```

2. **Reconstrua os containers:**
   ```powershell
   docker compose down
   docker compose up -d --build
   ```

3. **Teste a integração:**
   ```powershell
   .\test-usuario.ps1
   .\test-pagamento.ps1
   ```

### Para Integrar Seu Serviço

Siga o guia em [`IMPLEMENTACAO.md`](file:///c:/Users/Rodolfo/Desktop/UFC-CIENCIA-DA-COMPUTACAO/Sistemas%20Distribuidos/Consulta-Medica-SD/IMPLEMENTACAO.md) para:
- Adicionar seu serviço ao `docker-compose.yml`
- Integrar com RabbitMQ para enviar notificações
- Conectar ao banco MySQL compartilhado

---

## 📝 Próximos Passos (Opcional)

### Melhorias Sugeridas

1. **Integrar Agendamento com RabbitMQ**
   - Enviar notificação ao criar consulta
   - Enviar notificação ao cancelar consulta

2. **Adicionar Healthchecks**
   - Endpoint `/health` em todos os serviços
   - Configurar no docker-compose

3. **Documentação de API**
   - Swagger/OpenAPI para REST APIs
   - Documentação gRPC

---

## 🔍 Verificação

Para verificar se tudo está funcionando:

```powershell
# 1. Verificar status
docker compose ps

# 2. Criar um usuário
.\test-usuario.ps1

# 3. Criar um pagamento
.\test-pagamento.ps1

# 4. Verificar logs de notificações
docker logs servico-notificacoes

# 5. Verificar e-mails recebidos
```

Todos os testes devem passar e e-mails devem ser recebidos! ✅

---

**Documento mantido por:** Equipe de Desenvolvimento  
**Última revisão:** 05/01/2026
