# ====================================================================
# Script de Teste - Serviço de Pagamentos
# Sistema de Consultas Médicas - Sistemas Distribuídos
# ====================================================================

Write-Host "🏥 Teste do Serviço de Pagamentos" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray
Write-Host ""

# Configurações
$baseUrl = "http://localhost:8000/api/payloads"
$email = "seu-email@gmail.com"  # ALTERE AQUI para seu e-mail

# ====================================================================
# TESTE 1: Criar um novo pagamento
# ====================================================================
Write-Host "📝 TESTE 1: Criando novo pagamento..." -ForegroundColor Yellow
Write-Host ""

$body = @{
    agendamento_id = 1
    total = 150.00
    payment_method = "pix"
    customer_email = $email
} | ConvertTo-Json

Write-Host "Dados enviados:" -ForegroundColor Gray
Write-Host $body -ForegroundColor White
Write-Host ""

try {
    $response = Invoke-RestMethod `
        -Uri $baseUrl `
        -Method POST `
        -ContentType "application/json" `
        -Body $body
    
    Write-Host "✅ Pagamento criado com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Resposta:" -ForegroundColor Gray
    $response | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor White
    Write-Host ""
    
    $paymentId = $response.id
    
    # ====================================================================
    # TESTE 2: Consultar o pagamento criado
    # ====================================================================
    Write-Host ""
    Write-Host "🔍 TESTE 2: Consultando pagamento ID: $paymentId..." -ForegroundColor Yellow
    Write-Host ""
    
    Start-Sleep -Seconds 2
    
    $getResponse = Invoke-RestMethod `
        -Uri "$baseUrl/$paymentId" `
        -Method GET
    
    Write-Host "✅ Pagamento encontrado!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Detalhes:" -ForegroundColor Gray
    $getResponse | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor White
    Write-Host ""
    
    # ====================================================================
    # TESTE 3: Confirmar o pagamento
    # ====================================================================
    Write-Host ""
    Write-Host "💰 TESTE 3: Confirmando pagamento ID: $paymentId..." -ForegroundColor Yellow
    Write-Host ""
    
    Start-Sleep -Seconds 2
    
    $payResponse = Invoke-RestMethod `
        -Uri "$baseUrl/$paymentId/pay" `
        -Method POST
    
    Write-Host "✅ Pagamento confirmado!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Resposta:" -ForegroundColor Gray
    $payResponse | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor White
    Write-Host ""
    
    # ====================================================================
    # Resumo
    # ====================================================================
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Gray
    Write-Host "📊 RESUMO DOS TESTES" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Gray
    Write-Host ""
    Write-Host "✅ Pagamento criado: ID $paymentId" -ForegroundColor Green
    Write-Host "✅ Pagamento consultado com sucesso" -ForegroundColor Green
    Write-Host "✅ Pagamento confirmado (status: paid)" -ForegroundColor Green
    Write-Host ""
    Write-Host "📧 Verifique seu e-mail: $email" -ForegroundColor Yellow
    Write-Host "   Você deve ter recebido 2 e-mails:" -ForegroundColor Gray
    Write-Host "   1. Pagamento em Aberto" -ForegroundColor Gray
    Write-Host "   2. Confirmação de Pagamento" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📋 Verifique os logs do serviço de notificações:" -ForegroundColor Yellow
    Write-Host "   docker logs -f servico-notificacoes" -ForegroundColor White
    Write-Host ""
    
} catch {
    Write-Host "❌ Erro ao executar teste!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Detalhes do erro:" -ForegroundColor Gray
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "  • O serviço de pagamentos não está rodando" -ForegroundColor Gray
    Write-Host "  • Execute: docker compose up -d" -ForegroundColor White
    Write-Host "  • Verifique os logs: docker compose logs pagamentos" -ForegroundColor White
    Write-Host ""
}

Write-Host "=" * 60 -ForegroundColor Gray
