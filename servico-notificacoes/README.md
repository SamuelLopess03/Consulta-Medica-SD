# Serviço de Notificações - Sistema de Consultas Médicas

Serviço de notificações distribuído usando **RabbitMQ** e **Node.js** para envio automático de emails.

## 📋 Descrição

Este serviço é responsável por:
- Escutar mensagens no tópico `sd/notificacoes` do RabbitMQ
- Processar notificações recebidas de outros serviços do sistema
- Enviar emails automaticamente para os destinatários

## 🏗️ Arquitetura

O serviço utiliza o padrão **Publisher/Subscriber** com RabbitMQ:
- **Exchange**: `notificacoes_exchange` (tipo: topic)
- **Tópico**: `sd/notificacoes`
- **Protocolo**: AMQP

## 🚀 Tecnologias

- **Node.js** 18+
- **RabbitMQ** (AMQP)
- **Nodemailer** (envio de emails)
- **Docker** (containerização)

## 📦 Instalação

### Pré-requisitos

- Node.js 18 ou superior
- RabbitMQ rodando (local ou Docker)
- Servidor SMTP configurado (Gmail, Outlook, etc.)

### Instalação Local

```bash
# Instalar dependências
npm install

# Copiar arquivo de configuração
cp .env.example .env

# Editar .env com suas configurações
nano .env
```

## ⚙️ Configuração

Edite o arquivo `.env` com suas credenciais:

```env
# RabbitMQ
RABBITMQ_URL=amqp://localhost:5672
RABBITMQ_TOPIC=sd/notificacoes

# Email (exemplo com Gmail)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_SECURE=false
EMAIL_USER=seu-email@gmail.com
EMAIL_PASS=sua-senha-de-app

# Remetente
EMAIL_FROM=Sistema de Consultas Médicas <noreply@consultamedica.com>
```

### 📧 Configuração do Gmail

Para usar o Gmail, você precisa:

1. Ativar a verificação em duas etapas na sua conta Google
2. Gerar uma "Senha de App" em: https://myaccount.google.com/apppasswords
3. Usar essa senha no campo `EMAIL_PASS`

## 🎯 Como Rodar o Sistema

### Passo a Passo Completo

#### 1️⃣ Instalar Dependências

```bash
cd servico-notificacoes
npm install
```

#### 2️⃣ Configurar Variáveis de Ambiente

O arquivo `.env` já deve estar configurado. Verifique se contém:

```env
RABBITMQ_URL=amqp://admin:admin@localhost:5672
RABBITMQ_TOPIC=sd/notificacoes
EMAIL_HOST=smtp.hostinger.com
EMAIL_PORT=465
EMAIL_SECURE=true
EMAIL_USER=suporte@smartwebsistemas.online
EMAIL_PASS=sua-senha
EMAIL_FROM=Sistema de Consultas Medicas <suporte@smartwebsistemas.online>
NODE_ENV=development
PORT=3003
```

> ⚠️ **IMPORTANTE:** A URL do RabbitMQ deve incluir as credenciais: `amqp://admin:admin@localhost:5672`

#### 3️⃣ Iniciar o RabbitMQ

Inicie **apenas o RabbitMQ** com Docker:

```bash
docker run -d --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=admin \
  -e RABBITMQ_DEFAULT_PASS=admin \
  rabbitmq:3-management
```

Ou use o Docker Compose para iniciar apenas o RabbitMQ:

```bash
docker-compose up -d rabbitmq
```

**Verificar se o RabbitMQ está rodando:**

```bash
docker ps | findstr rabbitmq
```

**Acessar o painel do RabbitMQ:**
- URL: http://localhost:15672
- Usuário: `admin`
- Senha: `admin`

#### 4️⃣ Iniciar o Serviço de Notificações

```bash
npm start
```

Você verá logs como:

```
🚀 Iniciando Serviço de Notificações...
✅ Conexão com servidor SMTP verificada com sucesso
🔌 Conectando ao RabbitMQ em amqp://admin:admin@localhost:5672...
✅ Conectado ao RabbitMQ
📡 Escutando no tópico: sd/notificacoes
👂 Aguardando mensagens...
```

#### 5️⃣ Testar o Serviço

Em outro terminal, execute o script de teste:

```bash
node test/enviar-teste.js
```

Você verá o email sendo processado nos logs do serviço.

---

### Alternativa: Rodar Tudo com Docker Compose

Se preferir rodar tudo containerizado:

```bash
# Parar o serviço local se estiver rodando (Ctrl+C)

# Iniciar tudo com Docker Compose
docker-compose up -d

# Ver logs do serviço
docker logs -f servico-notificacoes
```

Para parar:

```bash
docker-compose down
```

---

### Modo Desenvolvimento (com Hot Reload)

```bash
npm run dev
```

## 📨 Formato das Mensagens

Os outros serviços devem publicar mensagens no formato JSON:

```json
{
  "email": "paciente@example.com",
  "assunto": "Confirmação de Consulta",
  "mensagem": "Sua consulta foi agendada para 05/01/2026 às 14:00"
}
```

Campos aceitos (português ou inglês):
- `email` (obrigatório)
- `assunto` ou `subject` (obrigatório)
- `mensagem` ou `message` (obrigatório)

## 🔧 Exemplo de Publicação

### Com Node.js (amqplib)

```javascript
const amqp = require('amqplib');

async function enviarNotificacao() {
  const connection = await amqp.connect('amqp://localhost:5672');
  const channel = await connection.createChannel();
  
  await channel.assertExchange('notificacoes_exchange', 'topic', { durable: true });
  
  const notificacao = {
    email: 'paciente@example.com',
    assunto: 'Confirmação de Consulta',
    mensagem: 'Sua consulta foi agendada com sucesso!'
  };
  
  channel.publish(
    'notificacoes_exchange',
    'sd/notificacoes',
    Buffer.from(JSON.stringify(notificacao))
  );
  
  console.log('Notificação enviada!');
  
  await channel.close();
  await connection.close();
}
```

### Com Python (pika)

```python
import pika
import json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='notificacoes_exchange', exchange_type='topic', durable=True)

notificacao = {
    'email': 'paciente@example.com',
    'assunto': 'Confirmação de Consulta',
    'mensagem': 'Sua consulta foi agendada com sucesso!'
}

channel.basic_publish(
    exchange='notificacoes_exchange',
    routing_key='sd/notificacoes',
    body=json.dumps(notificacao)
)

print('Notificação enviada!')
connection.close()
```

## 📊 Logs

O serviço exibe logs coloridos e informativos:

```
🚀 Iniciando Serviço de Notificações...
✅ Conectado ao RabbitMQ
📡 Escutando no tópico: sd/notificacoes
👂 Aguardando mensagens...

📨 Nova mensagem recebida no tópico sd/notificacoes:
📧 Enviando email para: paciente@example.com
✅ Email enviado: <message-id>
✅ Mensagem processada com sucesso
```

## 🐛 Troubleshooting

### Erro: ACCESS_REFUSED - Login was refused

Se você ver este erro:
```
❌ Erro ao conectar ao RabbitMQ: Handshake terminated by server: 403 (ACCESS-REFUSED)
```

**Causa:** A URL do RabbitMQ no `.env` não inclui as credenciais.

**Solução:** Certifique-se de que o `.env` contém:
```env
RABBITMQ_URL=amqp://admin:admin@localhost:5672
```

Note o `admin:admin@` antes de `localhost`.

### RabbitMQ não conecta

```bash
# Verificar se RabbitMQ está rodando
docker ps | findstr rabbitmq

# Se não estiver, iniciar RabbitMQ
docker run -d --name rabbitmq \
  -p 5672:5672 \
  -p 15672:15672 \
  -e RABBITMQ_DEFAULT_USER=admin \
  -e RABBITMQ_DEFAULT_PASS=admin \
  rabbitmq:3-management
```

### Emails não são enviados

1. Verifique as credenciais SMTP no `.env`
2. Para Gmail, certifique-se de usar "Senha de App"
3. Para Hostinger, use porta 465 com `EMAIL_SECURE=true`
4. Verifique os logs do serviço para erros específicos

### Mensagens não são recebidas

1. Verifique se o tópico está correto: `sd/notificacoes`
2. Verifique se o exchange foi criado: `notificacoes_exchange`
3. Acesse o painel do RabbitMQ: http://localhost:15672
4. Verifique se o serviço está conectado e escutando

## 📁 Estrutura do Projeto

```
servico-notificacoes/
├── src/
│   ├── index.js          # Arquivo principal
│   ├── config.js         # Configurações
│   ├── rabbitmq.js       # Serviço RabbitMQ
│   └── emailService.js   # Serviço de email
├── .env.example          # Exemplo de configuração
├── .gitignore
├── .dockerignore
├── Dockerfile
├── package.json
└── README.md
```

## 🤝 Integração com Outros Serviços

Este serviço foi projetado para receber notificações de:
- **Serviço de Usuários** (cadastros, alterações)
- **Serviço de Agendamento** (confirmações, cancelamentos)
- **Serviço de Pagamentos** (confirmações, cobranças)

Todos devem publicar no tópico `sd/notificacoes` do RabbitMQ.

## 📝 Licença

ISC

## 👥 Autor

Desenvolvido para a disciplina de Sistemas Distribuídos - UFC Crateús
