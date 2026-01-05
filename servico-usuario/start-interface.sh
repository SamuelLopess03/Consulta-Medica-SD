#!/bin/bash
echo "🔄 Aguardando serviço de usuários..."
while ! nc -z servico-usuario 5001; do
  sleep 1
done
echo "✅ Serviço de usuários pronto!"
echo "🚀 Iniciando Interface REST..."
python user_interface.py
