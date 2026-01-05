# 🏥 Guia de Integração: Sistema de Consultas Médicas

Este documento orienta os membros do grupo sobre como integrar seus serviços (Usuários, Agendamento, etc.) com os módulos de **Pagamento** e **Notificações**.

---

## 🏗️ 1. Como Rodar o Sistema (Docker)

Para que todos os serviços se comuniquem, utilize o orquestrador na raiz do projeto:

1.  **Configure o Ambiente:** Copie o arquivo `.env.example` para `.env` na raiz e preencha as credenciais de e-mail (SMTP).
2.  **Suba os Serviços:**
    ```powershell
    docker compose up -d
    ```
3.  **Acompanhe os Logs:**
    ```powershell
    docker compose logs -f notificacoes
    ```

---

## 📨 2. Enviando Notificações (RabbitMQ)

Qualquer serviço pode disparar e-mails enviando uma mensagem para o Broker:

*   **Exchange:** `notificacoes_exchange`
*   **Tipo:** `topic`
*   **Routing Key:** `sd/notificacoes`
*   **Host (Interno Docker):** `rabbitmq` (porta 5672)

### Estrutura do JSON (Payload):
```json
{
  "email": "cliente@exemplo.com",
  "assunto": "Assunto da Mensagem",
  "mensagem": "Conteúdo do e-mail aqui."
}
```

---

## 💳 3. Integrando com o Serviço de Pagamentos

A API de Pagamentos está disponível em `http://localhost:8000`.

### Criar um Pagamento (Gera notificação automática):
Envie um **POST** para `/api/payloads`.

---

## 🧪 4. Como Testar a Integração

Para validar se os serviços estão conversando, use o comando abaixo no PowerShell. Ele criará um pagamento que, por sua vez, enviará uma mensagem ao RabbitMQ para que o serviço de notificações dispare o e-mail.

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

### Verificação de Sucesso:
1.  **Resposta da API:** Você receberá um JSON com o `id` do pagamento e status `pending`.
2.  **Logs de Notificação:** No terminal do Docker, aparecerá: `📨 Nova mensagem recebida no tópico sd/notificacoes`.
3.  **E-mail Real:** O destinatário receberá o e-mail formatado.

---

## 🛠️ 5. FAQ de Integração

*   **P: Meu serviço não conecta no RabbitMQ.**
    *   R: Se estiver rodando via Docker, use o host `rabbitmq`. Se estiver rodando local (fora do Docker), use `localhost`.
*   **P: Onde vejo as mensagens trafegando?**
    *   R: Acesse o painel do RabbitMQ em `http://localhost:15672` (admin/admin).
