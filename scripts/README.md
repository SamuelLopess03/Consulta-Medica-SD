# 📜 Scripts de Controle do Sistema

Scripts Python para interagir com o sistema distribuído de consultas médicas.

## 🔧 Instalação de Dependências

```bash
cd scripts
pip install -r requirements.txt
```

---

## 🚀 Guia de Uso

Todos os scripts agora suportam **Modo Interativo**! Basta executar o script sem argumentos e seguir as instruções na tela.

### 👥 Gerenciamento de Usuários

| Script | Descrição | Requer Auth? |
|--------|-----------|--------------|
| `cadastrar_usuario.py` | Cria novos usuários (Paciente, Médico, etc) | ❌ Não |
| `listar_usuarios.py` | Lista todos os usuários | ✅ Sim |
| `editar_usuario.py` | Edita dados de um usuário | ✅ Sim |
| `excluir_usuario.py` | Desativa um usuário | ✅ Sim (Admin) |
| `obter_token.py` | Obtém token JWT para testes | ❌ Não |

#### Exemplo Rápido:
```bash
python cadastrar_usuario.py
```

### 📅 Gerenciamento de Agendamentos

| Script | Descrição |
|--------|-----------|
| `cadastrar_agendamento.py` | Marca uma nova consulta |
| `consultar_status_agendamento.py` | Verifica status de um agendamento |
| `editar_agendamento.py` | Atualiza status (Confirmar/Cancelar) |
| `excluir_agendamento.py` | Remove um agendamento |

#### Exemplo Rápido:
```bash
python cadastrar_agendamento.py
# O script irá ajudar a encontrar médicos e pacientes!
```

### 👨‍⚕️ Área Médica

| Script | Descrição |
|--------|-----------|
| `cadastrar_horario_doutor.py` | Define horários de atendimento |
| `listar_horarios_disponiveis.py` | Consulta agenda de um médico |

### 💰 Pagamentos

| Script | Descrição |
|--------|-----------|
| `pagar_agendamento.py` | Realiza pagamento (Pix/Cartão) |

---

## 🧪 Teste Completo Automatizado

Para testar todo o fluxo de uma vez:

```bash
python testar-sistema-completo.py
```

Isso irá criar pacientes, médicos, agendamentos e pagamentos automaticamente para verificar a saúde do sistema.

---
**Observação:**
Caso encontre erros de conexão (`Connection refused`), certifique-se que o Docker está rodando:
```bash
docker compose up -d
```
