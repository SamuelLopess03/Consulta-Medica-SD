# ====================================================================
# GUIA RÁPIDO: Como Subir TODOS os Serviços
# Sistema de Consultas Médicas - Sistemas Distribuídos
# ====================================================================

Write-Host "🏥 Sistema de Consultas Médicas - Guia de Inicialização" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

# ====================================================================
# PASSO 1: Parar serviços antigos (se houver)
# ====================================================================
Write-Host "🛑 PASSO 1: Parando serviços antigos..." -ForegroundColor Yellow
docker compose down
Write-Host "✅ Serviços antigos parados" -ForegroundColor Green
Write-Host ""

# ====================================================================
# PASSO 2: Subir TODOS os serviços
# ====================================================================
Write-Host "🚀 PASSO 2: Subindo TODOS os serviços..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Serviços que serão iniciados:" -ForegroundColor Gray
Write-Host "  1. 🐰 RabbitMQ (Message Broker)" -ForegroundColor White
Write-Host "  2. 🗄️  MySQL (Banco de Dados)" -ForegroundColor White
Write-Host "  3. 📧 Serviço de Notificações (Node.js)" -ForegroundColor White
Write-Host "  4. 💰 Serviço de Pagamentos (Laravel)" -ForegroundColor White
Write-Host "  5. 📅 Serviço de Agendamento (Java Spring)" -ForegroundColor White
Write-Host "  6. 👤 Serviço de Usuários (Python Socket)" -ForegroundColor White
Write-Host "  7. 🌐 Interface REST de Usuários (Python Flask)" -ForegroundColor White
Write-Host ""

docker compose up -d --build

Write-Host ""
Write-Host "⏳ Aguardando serviços iniciarem..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# ====================================================================
# PASSO 3: Verificar status
# ====================================================================
Write-Host ""
Write-Host "📊 PASSO 3: Verificando status dos serviços..." -ForegroundColor Yellow
Write-Host ""
docker compose ps

# ====================================================================
# PASSO 4: Informações úteis
# ====================================================================
Write-Host ""
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "📋 INFORMAÇÕES ÚTEIS" -ForegroundColor Cyan
Write-Host "=" * 70 -ForegroundColor Gray
Write-Host ""

Write-Host "🌐 URLs dos Serviços:" -ForegroundColor Yellow
Write-Host "  • RabbitMQ Management:  http://localhost:15672 (admin/admin)" -ForegroundColor White
Write-Host "  • API Pagamentos:       http://localhost:8000/api/payloads" -ForegroundColor White
Write-Host "  • API Agendamento:      http://localhost:8080" -ForegroundColor White
Write-Host "  • API Usuários (REST):  http://localhost:5000/users" -ForegroundColor White
Write-Host "  • gRPC Agendamento:     localhost:9090" -ForegroundColor White
Write-Host "  • Socket Usuários:      localhost:5001" -ForegroundColor White
Write-Host ""

Write-Host "📝 Comandos Úteis:" -ForegroundColor Yellow
Write-Host "  • Ver todos os logs:           docker compose logs -f" -ForegroundColor White
Write-Host "  • Ver logs de um serviço:      docker compose logs -f [nome-servico]" -ForegroundColor White
Write-Host "  • Parar todos os serviços:     docker compose down" -ForegroundColor White
Write-Host "  • Reiniciar um serviço:        docker compose restart [nome-servico]" -ForegroundColor White
Write-Host ""

Write-Host "🔧 Nomes dos Serviços:" -ForegroundColor Yellow
Write-Host "  • rabbitmq" -ForegroundColor White
Write-Host "  • bd (MySQL)" -ForegroundColor White
Write-Host "  • servico-notificacoes" -ForegroundColor White
Write-Host "  • laravel-api (pagamentos)" -ForegroundColor White
Write-Host "  • servico-agendamento" -ForegroundColor White
Write-Host "  • servico-usuario" -ForegroundColor White
Write-Host "  • servico-usuario-interface" -ForegroundColor White
Write-Host ""

Write-Host "🧪 Testar Integração:" -ForegroundColor Yellow
Write-Host "  • Criar pagamento:  .\test-pagamento.ps1" -ForegroundColor White
Write-Host "  • Ou use:           .\test-pagamento-simples.txt" -ForegroundColor White
Write-Host ""

Write-Host "=" * 70 -ForegroundColor Gray
Write-Host "✅ Sistema pronto para uso!" -ForegroundColor Green
Write-Host "=" * 70 -ForegroundColor Gray
