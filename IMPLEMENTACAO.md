# 🏥 Guia de Integração: Sistema de Consultas Médicas

Este documento orienta os membros do grupo sobre como integrar seus serviços ao sistema distribuído de consultas médicas.

---

## 🏗️ 1. Como Rodar o Sistema Completo

### Pré-requisitos
- Docker e Docker Compose instalados
- Arquivo `.env` configurado na raiz do projeto

### Inicialização

1. **Configure o Ambiente:**
   ```powershell
   # Copie o arquivo de exemplo (se ainda não tiver)
   Copy-Item .env.example .env
   
   # Edite o .env com suas credenciais de e-mail SMTP
   notepad .env
   ```

2. **Suba TODOS os Serviços:**
   ```powershell
   docker compose up -d
   ```
   
   Isso iniciará automaticamente:
   - 🐰 RabbitMQ (Message Broker)
   - 🗄️ MySQL (Banco de Dados)
   - 📧 Serviço de Notificações (Node.js)
   - 💰 Serviço de Pagamentos (Laravel)
   - 📅 Serviço de Agendamento (Java Spring)
   - 👤 Serviço de Usuários (Python)
   - 🌐 Interface REST de Usuários (Flask)

3. **Verifique o Status:**
   ```powershell
   docker compose ps
   ```

4. **Acompanhe os Logs:**
   ```powershell
   # Todos os serviços
   docker compose logs -f
   
   # Serviço específico
   docker compose logs -f notificacoes
   docker compose logs -f pagamentos
   docker compose logs -f agendamento
   docker compose logs -f servico-usuario
   ```

---

## 📨 2. Enviando Notificações (RabbitMQ)

Qualquer serviço pode disparar e-mails enviando mensagens para o RabbitMQ.

### Configuração do RabbitMQ

- **Exchange:** `notificacoes_exchange`
- **Tipo:** `topic`
- **Routing Key:** `sd/notificacoes`
- **Host (Interno Docker):** `rabbitmq` (porta 5672)
- **Credenciais:** admin/admin

### Estrutura do JSON (Payload)

```json
{
  "email": "cliente@exemplo.com",
  "assunto": "Assunto da Mensagem",
  "mensagem": "Conteúdo do e-mail aqui."
}
```

### Exemplos de Integração

#### Python (usando pika)

```python
import pika
import json

# Conectar ao RabbitMQ
credentials = pika.PlainCredentials('admin', 'admin')
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='rabbitmq', credentials=credentials)
)
channel = connection.channel()

# Declarar exchange
channel.exchange_declare(
    exchange='notificacoes_exchange',
    exchange_type='topic',
    durable=True
)

# Publicar notificação
notificacao = {
    'email': 'usuario@exemplo.com',
    'assunto': 'Bem-vindo!',
    'mensagem': 'Sua conta foi criada com sucesso.'
}

channel.basic_publish(
    exchange='notificacoes_exchange',
    routing_key='sd/notificacoes',
    body=json.dumps(notificacao),
    properties=pika.BasicProperties(delivery_mode=2)  # Persistente
)

print('Notificação enviada!')
connection.close()
```

#### PHP (usando php-amqplib)

```php
use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

$connection = new AMQPStreamConnection(
    'rabbitmq',  // host
    5672,        // port
    'admin',     // user
    'admin',     // password
    '/'          // vhost
);

$channel = $connection->channel();

$channel->exchange_declare(
    'notificacoes_exchange',
    'topic',
    false,
    true,
    false
);

$notificacao = [
    'email' => 'usuario@exemplo.com',
    'assunto' => 'Pagamento Confirmado',
    'mensagem' => 'Seu pagamento foi processado com sucesso.'
];

$message = new AMQPMessage(
    json_encode($notificacao),
    ['delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT]
);

$channel->basic_publish(
    $message,
    'notificacoes_exchange',
    'sd/notificacoes'
);

echo 'Notificação enviada!';
$channel->close();
$connection->close();
```

#### Java (usando RabbitMQ Java Client)

```java
import com.rabbitmq.client.Channel;
import com.rabbitmq.client.Connection;
import com.rabbitmq.client.ConnectionFactory;
import com.google.gson.Gson;

ConnectionFactory factory = new ConnectionFactory();
factory.setHost("rabbitmq");
factory.setUsername("admin");
factory.setPassword("admin");

try (Connection connection = factory.newConnection();
     Channel channel = connection.createChannel()) {
    
    channel.exchangeDeclare("notificacoes_exchange", "topic", true);
    
    Map<String, String> notificacao = new HashMap<>();
    notificacao.put("email", "usuario@exemplo.com");
    notificacao.put("assunto", "Consulta Agendada");
    notificacao.put("mensagem", "Sua consulta foi agendada para 05/01/2026.");
    
    String json = new Gson().toJson(notificacao);
    
    channel.basicPublish(
        "notificacoes_exchange",
        "sd/notificacoes",
        MessageProperties.PERSISTENT_TEXT_PLAIN,
        json.getBytes("UTF-8")
    );
    
    System.out.println("Notificação enviada!");
}
```

---

## 💳 3. Integrando com o Serviço de Pagamentos

A API de Pagamentos está disponível em `http://localhost:8000` (ou `http://laravel-api:8000` dentro do Docker).

### Endpoints Disponíveis

#### Criar Pagamento
```http
POST /api/payloads
Content-Type: application/json

{
  "agendamento_id": 10,
  "total": 150.00,
  "payment_method": "pix",
  "customer_email": "cliente@email.com"
}
```

**Resposta:**
```json
{
  "id": 1,
  "agendamento_id": 10,
  "total": 150.00,
  "payment_method": "pix",
  "customer_email": "cliente@email.com",
  "status": "pending",
  "created_at": "2026-01-05T21:00:00.000000Z",
  "updated_at": "2026-01-05T21:00:00.000000Z"
}
```

> **Nota:** Ao criar um pagamento, uma notificação automática é enviada via RabbitMQ.

#### Confirmar Pagamento
```http
POST /api/payloads/{id}/pay
```

#### Consultar Pagamento
```http
GET /api/payloads/{id}
```

---

## 👤 4. Integrando com o Serviço de Usuários

A API de Usuários está disponível em `http://localhost:5000` (ou `http://servico-usuario-interface:5000` dentro do Docker).

### Endpoints Disponíveis

#### Criar Usuário
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

#### Autenticar
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
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": { ... }
}
```

> **Nota:** Ao criar um usuário, uma notificação de boas-vindas é enviada via RabbitMQ.

---

## 📅 5. Integrando com o Serviço de Agendamento

O serviço de agendamento oferece APIs REST e gRPC.

### REST API
- **URL:** `http://localhost:8080` (ou `http://servico-agendamento:8080`)

### gRPC
- **Host:** `servico-agendamento:9090`

---

## 🧪 6. Como Testar a Integração

### Teste Completo do Fluxo

Execute este comando no PowerShell para criar um pagamento e verificar se a notificação é enviada:

```powershell
Invoke-RestMethod `
  -Uri "http://localhost:8000/api/payloads" `
  -Method POST `
  -ContentType "application/json" `
  -Body '{
    "agendamento_id": 10,
    "total": 150.00,
    "payment_method": "pix",
    "customer_email": "seu-email@gmail.com"
  }'
```

### Verificação de Sucesso

1. **Resposta da API:** JSON com o `id` do pagamento e status `pending`
2. **Logs de Notificação:**
   ```powershell
   docker logs servico-notificacoes
   ```
   Deve aparecer: `📨 Nova mensagem recebida no tópico sd/notificacoes`
3. **E-mail Real:** O destinatário receberá o e-mail

### Scripts de Teste Prontos

- **Teste de Pagamentos:** `.\test-pagamento.ps1`
- **Teste de Usuários:** `.\test-usuario.ps1`

---

## 🗄️ 7. Banco de Dados Compartilhado

Todos os serviços usam o mesmo banco MySQL:

- **Host:** `db` (dentro do Docker) ou `localhost:3306` (externo)
- **Database:** `consultamedica`
- **Usuário:** `user`
- **Senha:** `userpassword`

### Tabelas por Serviço

| Serviço | Tabelas |
|---------|---------|
| Usuários | `app_users` |
| Agendamento | `consultas`, `horarios` |
| Pagamentos | `payloads` |

---

## 🛠️ 8. FAQ de Integração

### P: Meu serviço não conecta no RabbitMQ
**R:** Verifique:
- Se está rodando via Docker, use o host `rabbitmq`
- Se está rodando local (fora do Docker), use `localhost`
- Credenciais: `admin/admin`

### P: Onde vejo as mensagens trafegando?
**R:** Acesse o painel do RabbitMQ em `http://localhost:15672` (admin/admin)

### P: Como adicionar meu serviço ao docker-compose.yml?
**R:** Siga este template:

```yaml
meu-servico:
  build: ./meu-servico
  container_name: meu-servico
  depends_on:
    db:
      condition: service_healthy
    rabbitmq:
      condition: service_healthy
  environment:
    DB_HOST: db
    DB_PORT: 3306
    DB_DATABASE: consultamedica
    DB_USERNAME: user
    DB_PASSWORD: userpassword
    RABBITMQ_HOST: rabbitmq
  ports:
    - "PORTA_EXTERNA:PORTA_INTERNA"
  networks:
    - consulta-medica-network
  restart: unless-stopped
```

### P: Como publicar eventos no RabbitMQ?
**R:** Veja os exemplos na seção 2 deste documento para sua linguagem.

---

## 📚 9. Documentação Adicional

- **Análise Completa:** Veja `analise_completa_projeto.md` no diretório `.gemini`
- **Auditoria do Sistema:** Veja `auditoria_sistema.md` no diretório `.gemini`
- **Mudanças Recentes:** Veja `MUDANCAS.md` na raiz do projeto

---

## 🚀 10. Comandos Úteis

```powershell
# Subir todos os serviços
docker compose up -d

# Parar todos os serviços
docker compose down

# Ver logs de todos os serviços
docker compose logs -f

# Ver logs de um serviço específico
docker compose logs -f [nome-servico]

# Reconstruir e subir um serviço
docker compose up -d --build [nome-servico]

# Ver status dos serviços
docker compose ps

# Acessar shell de um container
docker exec -it [nome-container] bash

# Ver logs do RabbitMQ Management
# Acesse: http://localhost:15672 (admin/admin)
```

---

**Última atualização:** 05/01/2026  
**Versão:** 2.0
