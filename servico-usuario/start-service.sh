#!/bin/bash
echo "🔄 Aguardando banco de dados MySQL..."
while ! nc -z db 3306; do
  sleep 1
done
echo "✅ Banco de dados MySQL pronto!"
echo "🚀 Iniciando Serviço de Usuários..."
python user_service.py
