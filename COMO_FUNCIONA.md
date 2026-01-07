# 🏥 Sistema Distribuído de Consultas Médicas

Este projeto é um sistema distribuído composto por microsserviços para gerenciamento de usuários, agendamentos, pagamentos e notificações.

---

## 🏗️ Arquitetura

O sistema utiliza **Docker** para orquestrar os seguintes serviços:

| Serviço | Tecnologia | Porta | Descrição |
|---------|------------|-------|-----------|
| **servico-usuario** | Python (Socket TCP) | 5001 | Lógica de negócios de usuários |
| **servico-usuario-interface** | Flask (Python) | 5000 | API REST Gateway para usuários |
| **servico-agendamento** | Java Sprint Boot | 8080 | API de Agendamentos e Agenda Médica |
| **pagamentos** | PHP (Laravel) | 8000 | API de Pagamentos e Webhooks |
| **notificacoes** | Node.js | - | Consumidor de filas para envio de e-mails |
| **app-scripts** | Python (Container) | - | Ambiente de scripts utilitários |
| **rabbitmq** | Message Broker | 15672 | Mensageria entre serviços |
| **db** | MySQL | 3306 | Banco de dados compartilhado |

---

## 🚀 Como Iniciar

1. **Subir o ambiente:**
   ```bash
   docker compose up -d --build
   ```
   *Isso irá construir as imagens, iniciar os serviços e popular o banco de dados inicial.*

2. **Verificar status:**
   ```bash
   docker compose ps
   ```

---

## 🛠️ Scripts e Ferramentas (`app-scripts`)

O sistema conta com um container de utilitários chamado `app-scripts` que já vem com Python configurado.

### Como usar:

Você pode executar scripts diretamente dentro do container:

```bash
# Sinta-se um Hacker 🕶️
docker compose exec -it app-scripts python cadastrar_agendamento.py
```

### Principais Scripts:

- **`listar_usuarios.py`**: Vê quem está cadastrado.
- **`cadastrar_agendamento.py`**: Marca uma consulta interagindo com APIs.
- **`pagar_agendamento.py`**: Simula pagamento.
- **`init_system.py`**: Roda automaticamente no boot para criar dados.

---

## 🔄 Fluxo Completo de Teste

1. **Cadastro**: O sistema já cria usuários padrão (Admin, Médico, Paciente) no boot.
2. **Agendamento**: Use `cadastrar_agendamento.py` para criar uma consulta.
3. **Pagamento**: Use o ID gerado para pagar com `pagar_agendamento.py`.
4. **Notificação**: Verifique os logs do serviço de notificações:
   ```bash
   docker compose logs -f notificacoes
   ```

---

## 📚 Documentação Técnica

- **Scripts**: Veja `scripts/README.md`
- **Implementação**: Veja `IMPLEMENTACAO.md`
