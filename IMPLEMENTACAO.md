# Guia de Integração: Serviço de Notificações

Este documento descreve como outros módulos do sistema (como Usuários, Agendamento ou Pagamentos) devem se conectar e enviar mensagens para o **Serviço de Notificações**.

---

## 1. Configurações de Conexão (RabbitMQ)

Para se comunicar com o broker de mensagens, utilize as seguintes credenciais:

*   **Protocolo:** AMQP
*   **Host:** `localhost` (ou o IP/Hostname do container `rabbitmq`)
*   **Porta:** `5672`
*   **Usuário:** `admin`
*   **Senha:** `admin`

## 2. Parâmetros de Roteamento

O serviço de notificações utiliza o modelo **Publisher/Subscriber** com roteamento por tópicos:

*   **Exchange:** `notificacoes_exchange`
*   **Tipo da Exchange:** `topic`
*   **Routing Key (Tópico):** `sd/notificacoes`

## 3. Estrutura da Mensagem (Payload)

As mensagens devem ser enviadas em formato **JSON**. O serviço é flexível e aceita campos tanto em português quanto em inglês:

```json
{
  "email": "destinatario@exemplo.com",
  "assunto": "Confirmação de Consulta",
  "mensagem": "Olá! Sua consulta foi agendada para o dia 10/01 às 14:00."
}
```

### Campos Aceitos:
| Campo (PT) | Campo (EN) | Obrigatório | Descrição |
| :--- | :--- | :--- | :--- |
| `email` | `email` | Sim | E-mail do destinatário. |
| `assunto` | `subject` | Sim | Assunto que aparecerá no e-mail. |
| `mensagem` | `message` | Sim | Conteúdo principal da notificação. |

---

## 4. Fluxo de Execução

1.  **Agente Emissor:** Um serviço (ex: Agendamento) detecta um evento que exige notificação.
2.  **Publicação:** O serviço conecta ao RabbitMQ e envia o JSON para a `notificacoes_exchange` com a chave `sd/notificacoes`.
3.  **Consumo:** O **Serviço de Notificações** (Node.js) captura essa mensagem automaticamente.
4.  **Processamento:** O serviço valida o JSON e utiliza o **Nodemailer** para enviar o e-mail via SMTP.
5.  **Confirmação (ACK):** Após o envio bem-sucedido, o serviço avisa o RabbitMQ que a mensagem foi processada e pode ser removida da fila.
