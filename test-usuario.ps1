# ====================================================================
# Script de Teste - Serviço de Usuários
# Sistema de Consultas Médicas - Sistemas Distribuídos
# ====================================================================

Write-Host "👤 Teste do Serviço de Usuários" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Gray
Write-Host ""

# Configurações
$baseUrl = "http://localhost:5000/users"
$email = "teste.usuario@gmail.com"  # ALTERE AQUI para seu e-mail

# ====================================================================
# TESTE 1: Criar um novo usuário
# ====================================================================
Write-Host "📝 TESTE 1: Criando novo usuário..." -ForegroundColor Yellow
Write-Host ""

$body = @{
    name     = "João da Silva Teste"
    cpf      = "123.456.789-00"
    email    = $email
    password = "senha123"
    role     = "PATIENT"
    phone    = "85999999999"
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
    
    Write-Host "✅ Usuário criado com sucesso!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Resposta:" -ForegroundColor Gray
    $response | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor White
    Write-Host ""
    
    $userId = $response.user.id
    
    # ====================================================================
    # TESTE 2: Autenticar o usuário
    # ====================================================================
    Write-Host ""
    Write-Host "🔐 TESTE 2: Autenticando usuário..." -ForegroundColor Yellow
    Write-Host ""
    
    Start-Sleep -Seconds 2
    
    $authBody = @{
        email    = $email
        password = "senha123"
    } | ConvertTo-Json
    
    $authResponse = Invoke-RestMethod `
        -Uri "$baseUrl/authenticate" `
        -Method POST `
        -ContentType "application/json" `
        -Body $authBody
    
    Write-Host "✅ Autenticação realizada!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Token JWT:" -ForegroundColor Gray
    Write-Host $authResponse.token -ForegroundColor White
    Write-Host ""
    
    # ====================================================================
    # TESTE 3: Buscar usuário
    # ====================================================================
    Write-Host ""
    Write-Host "🔍 TESTE 3: Buscando usuário ID: $userId..." -ForegroundColor Yellow
    Write-Host ""
    
    Start-Sleep -Seconds 2
    
    $getResponse = Invoke-RestMethod `
        -Uri "$baseUrl/$userId" `
        -Method GET
    
    Write-Host "✅ Usuário encontrado!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Detalhes:" -ForegroundColor Gray
    $getResponse | ConvertTo-Json -Depth 3 | Write-Host -ForegroundColor White
    Write-Host ""
    
    # ====================================================================
    # Resumo
    # ====================================================================
    Write-Host ""
    Write-Host "=" * 60 -ForegroundColor Gray
    Write-Host "📊 RESUMO DOS TESTES" -ForegroundColor Cyan
    Write-Host "=" * 60 -ForegroundColor Gray
    Write-Host ""
    Write-Host "✅ Usuário criado: ID $userId" -ForegroundColor Green
    Write-Host "✅ Autenticação realizada com sucesso" -ForegroundColor Green
    Write-Host "✅ Usuário consultado com sucesso" -ForegroundColor Green
    Write-Host ""
    Write-Host "📧 Verifique seu e-mail: $email" -ForegroundColor Yellow
    Write-Host "   Você deve ter recebido:" -ForegroundColor Gray
    Write-Host "   • Bem-vindo ao Sistema de Consultas Médicas" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📋 Verifique os logs:" -ForegroundColor Yellow
    Write-Host "   docker logs servico-usuario" -ForegroundColor White
    Write-Host "   docker logs servico-notificacoes" -ForegroundColor White
    Write-Host ""
    
}
catch {
    Write-Host "❌ Erro ao executar teste!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Detalhes do erro:" -ForegroundColor Gray
    Write-Host $_.Exception.Message -ForegroundColor Red
    Write-Host ""
    Write-Host "Possíveis causas:" -ForegroundColor Yellow
    Write-Host "  • O serviço de usuários não está rodando" -ForegroundColor Gray
    Write-Host "  • Execute: docker compose up -d" -ForegroundColor White
    Write-Host "  • Verifique os logs: docker logs servico-usuario-interface" -ForegroundColor White
    Write-Host ""
}

Write-Host "=" * 60 -ForegroundColor Gray
