# Planilha de Mapeamento de Ações - Serviço de Usuários

## 📋 Como Usar Esta Planilha

Esta planilha mapeia todas as ações possíveis no Serviço de Usuários para os scripts correspondentes e como executá-los.

### ⚠️ Pré-requisitos
1. Certifique-se de que o Docker Compose está rodando:
   ```bash
   docker-compose up -d
   ```

2. Instale as dependências do cliente:
   ```bash
   pip install requests
   ```

---

## 🔧 Tabela de Ações

| # | AÇÃO | SCRIPT | COMO EXECUTAR | EXEMPLO PRÁTICO |
|---|------|--------|---------------|-----------------|
| 1 | Verificar status da API | `users_client.py` | `python users_client.py health` | `python users_client.py health` |
| 2 | Criar paciente | `users_client.py` | `python users_client.py create "<nome>" "<cpf>" "<email>" "<senha>" "PATIENT" "<telefone>"` | `python users_client.py create "João Silva" "123.456.789-00" "joao@email.com" "senha123" "PATIENT" "85999999999"` |
| 3 | Criar médico | `users_client.py` | `python users_client.py create "<nome>" "<cpf>" "<email>" "<senha>" "DOCTOR" "<telefone>" "<crm>" "<especialidade>"` | `python users_client.py create "Dra. Maria" "987.654.321-00" "maria@email.com" "senha123" "DOCTOR" "85988888888" "CRM12345" "Cardiologia"` |
| 4 | Criar recepcionista | `users_client.py` | `python users_client.py create "<nome>" "<cpf>" "<email>" "<senha>" "RECEPTIONIST" "<telefone>"` | `python users_client.py create "Ana Costa" "111.222.333-44" "ana@email.com" "senha123" "RECEPTIONIST" "85977777777"` |
| 5 | Criar administrador | `users_client.py` | `python users_client.py create "<nome>" "<cpf>" "<email>" "<senha>" "ADMIN" "<telefone>"` | `python users_client.py create "Carlos Admin" "555.666.777-88" "admin@email.com" "admin123" "ADMIN" "85966666666"` |
| 6 | Autenticar usuário | `users_client.py` | `python users_client.py auth "<email>" "<senha>"` | `python users_client.py auth "joao@email.com" "senha123"` |
| 7 | Buscar usuário por ID | `users_client.py` | `python users_client.py get <user_id>` | `python users_client.py get 1` |
| 8 | Listar todos os usuários | `users_client.py` | `python users_client.py list "<token>"` | `python users_client.py list "eyJ0eXAiOiJKV1QiLCJhbGc..."` |
| 9 | Listar apenas médicos | `users_client.py` | `python users_client.py list "<token>" "DOCTOR"` | `python users_client.py list "eyJ0eXAiOiJKV1QiLCJhbGc..." "DOCTOR"` |
| 10 | Listar apenas pacientes | `users_client.py` | `python users_client.py list "<token>" "PATIENT"` | `python users_client.py list "eyJ0eXAiOiJKV1QiLCJhbGc..." "PATIENT"` |
| 11 | Listar usuários ativos | `users_client.py` | `python users_client.py list "<token>" "" "1"` | `python users_client.py list "eyJ0eXAiOiJKV1QiLCJhbGc..." "" "1"` |
| 12 | Listar usuários inativos | `users_client.py` | `python users_client.py list "<token>" "" "0"` | `python users_client.py list "eyJ0eXAiOiJKV1QiLCJhbGc..." "" "0"` |
| 13 | Atualizar nome do usuário | `users_client.py` | `python users_client.py update <user_id> "<token>" name="<novo_nome>"` | `python users_client.py update 1 "eyJ0eXAiOiJKV1QiLCJhbGc..." name="João da Silva"` |
| 14 | Atualizar telefone | `users_client.py` | `python users_client.py update <user_id> "<token>" phone="<novo_telefone>"` | `python users_client.py update 1 "eyJ0eXAiOiJKV1QiLCJhbGc..." phone="85988888888"` |
| 15 | Atualizar senha | `users_client.py` | `python users_client.py update <user_id> "<token>" password="<nova_senha>"` | `python users_client.py update 1 "eyJ0eXAiOiJKV1QiLCJhbGc..." password="novaSenha123"` |
| 16 | Atualizar múltiplos campos | `users_client.py` | `python users_client.py update <user_id> "<token>" name="<nome>" phone="<tel>" email="<email>"` | `python users_client.py update 1 "eyJ0eXAiOiJKV1QiLCJhbGc..." name="João Silva" phone="85988888888" email="novo@email.com"` |
| 17 | Desativar usuário (admin) | `users_client.py` | `python users_client.py delete <user_id> "<token>"` | `python users_client.py delete 5 "eyJ0eXAiOiJKV1QiLCJhbGc..."` |

---

## 🔑 Observações Importantes

### Sobre Tokens
- **Obtenção**: Use a ação #6 (autenticar) para obter um token
- **Validade**: Tokens expiram em 24 horas
- **Uso**: Copie o token retornado e use nos comandos que requerem autenticação
- **Formato**: O token tem o formato `eyJ0eXAiOiJKV1QiLCJhbGc...` (muito longo)

### Sobre Roles (Tipos de Usuário)
- **PATIENT**: Paciente
- **DOCTOR**: Médico (requer CRM e especialidade)
- **RECEPTIONIST**: Recepcionista
- **ADMIN**: Administrador (pode desativar usuários)

### Sobre Permissões
- Criar usuário: Qualquer pessoa (sem autenticação)
- Buscar usuário específico: Qualquer pessoa (sem autenticação)
- Listar usuários: Requer autenticação (qualquer role)
- Atualizar usuário: Requer autenticação (próprio usuário ou admin)
- Desativar usuário: Requer autenticação (apenas ADMIN)

---

## 🎯 Fluxo de Teste Sugerido

### 1️⃣ Teste Básico (5 minutos)
```bash
# 1. Verificar se está funcionando
python users_client.py health

# 2. Criar um administrador
python users_client.py create "Admin Sistema" "000.000.000-00" "admin@sistema.com" "admin123" "ADMIN" "85900000000"

# 3. Autenticar (salve o token!)
python users_client.py auth "admin@sistema.com" "admin123"

# 4. Criar um paciente
python users_client.py create "Maria Paciente" "111.111.111-11" "maria@email.com" "senha123" "PATIENT" "85911111111"

# 5. Listar todos os usuários (use o token do passo 3)
python users_client.py list "SEU_TOKEN_AQUI"
```

### 2️⃣ Teste Completo (15 minutos)
```bash
# 1. Health check
python users_client.py health

# 2. Criar usuários de todos os tipos
python users_client.py create "Admin Sistema" "000.000.000-00" "admin@sistema.com" "admin123" "ADMIN"
python users_client.py create "Dr. João" "111.111.111-11" "drjoao@email.com" "senha123" "DOCTOR" "85911111111" "CRM11111" "Cardiologia"
python users_client.py create "Dra. Maria" "222.222.222-22" "drmaria@email.com" "senha123" "DOCTOR" "85922222222" "CRM22222" "Pediatria"
python users_client.py create "Ana Recepção" "333.333.333-33" "ana@email.com" "senha123" "RECEPTIONIST"
python users_client.py create "Carlos Paciente" "444.444.444-44" "carlos@email.com" "senha123" "PATIENT"
python users_client.py create "Julia Paciente" "555.555.555-55" "julia@email.com" "senha123" "PATIENT"

# 3. Autenticar como admin
python users_client.py auth "admin@sistema.com" "admin123"
# [Salve o token retornado como TOKEN_ADMIN]

# 4. Autenticar como paciente
python users_client.py auth "carlos@email.com" "senha123"
# [Salve o token retornado como TOKEN_PACIENTE]

# 5. Listar todos os usuários
python users_client.py list "TOKEN_ADMIN"

# 6. Listar apenas médicos
python users_client.py list "TOKEN_ADMIN" "DOCTOR"

# 7. Listar apenas pacientes
python users_client.py list "TOKEN_ADMIN" "PATIENT"

# 8. Buscar usuário específico
python users_client.py get 1

# 9. Atualizar dados do paciente
python users_client.py update 5 "TOKEN_PACIENTE" name="Carlos Silva" phone="85999999999"

# 10. Desativar usuário (como admin)
python users_client.py delete 6 "TOKEN_ADMIN"

# 11. Verificar que o usuário foi desativado
python users_client.py list "TOKEN_ADMIN" "" "0"
```

---

## 🐳 Comandos Docker Úteis

### Verificar status dos containers
```bash
docker-compose ps
```

### Ver logs em tempo real
```bash
docker-compose logs -f
```

### Ver logs apenas do serviço
```bash
docker-compose logs -f user_service
```

### Ver logs apenas da interface
```bash
docker-compose logs -f user_interface
```

### Reiniciar serviços
```bash
docker-compose restart
```

### Parar e remover tudo
```bash
docker-compose down -v
```

---

## 📞 Contato para Suporte

Em caso de dúvidas:
1. Verifique os logs: `docker-compose logs -f`
2. Consulte o README.md
3. Entre em contato com a equipe

---

## ✅ Checklist de Validação

Antes de entregar, verifique:

- [ ] Docker Compose sobe sem erros
- [ ] Health check retorna status 200
- [ ] Consegue criar usuários de todos os tipos
- [ ] Autenticação funciona e retorna token
- [ ] Token permite listar usuários
- [ ] Atualização de usuário funciona
- [ ] Apenas admin pode desativar usuários
- [ ] Logs estão claros e informativos
- [ ] README.md está completo
- [ ] Scripts cliente funcionam como esperado