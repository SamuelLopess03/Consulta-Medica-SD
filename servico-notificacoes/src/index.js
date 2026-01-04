const rabbitmqService = require('./rabbitmq');
const emailService = require('./emailService');
const config = require('./config');

async function startService() {
    console.log('🚀 Iniciando Serviço de Notificações...\n');
    console.log('📋 Configurações:');
    console.log(`   - RabbitMQ URL: ${config.rabbitmq.url}`);
    console.log(`   - Tópico: ${config.rabbitmq.topic}`);
    console.log(`   - Exchange: ${config.rabbitmq.exchange}`);
    console.log(`   - Email Host: ${config.email.host}`);
    console.log(`   - Ambiente: ${config.service.env}\n`);

    try {
        // Verificar conexão com servidor SMTP
        console.log('📧 Verificando conexão com servidor de email...');
        const emailConnected = await emailService.verifyConnection();

        if (!emailConnected) {
            console.warn('⚠️  Aviso: Não foi possível verificar a conexão com o servidor SMTP');
            console.warn('   O serviço continuará, mas emails podem falhar\n');
        }

        // Conectar ao RabbitMQ
        await rabbitmqService.connect();

        console.log('\n✅ Serviço de Notificações iniciado com sucesso!');
        console.log('👂 Aguardando mensagens...\n');

    } catch (error) {
        console.error('❌ Erro ao iniciar serviço:', error.message);
        process.exit(1);
    }
}

// Tratamento de sinais de encerramento
process.on('SIGINT', async () => {
    console.log('\n\n⚠️  Recebido sinal de interrupção (SIGINT)');
    console.log('🛑 Encerrando serviço...');

    await rabbitmqService.close();
    process.exit(0);
});

process.on('SIGTERM', async () => {
    console.log('\n\n⚠️  Recebido sinal de término (SIGTERM)');
    console.log('🛑 Encerrando serviço...');

    await rabbitmqService.close();
    process.exit(0);
});

// Tratamento de erros não capturados
process.on('uncaughtException', (error) => {
    console.error('❌ Erro não capturado:', error);
    process.exit(1);
});

process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Promise rejeitada não tratada:', reason);
    process.exit(1);
});

// Iniciar serviço
startService();
