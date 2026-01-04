const rabbitmqService = require('./rabbitmq');
const emailService = require('./emailService');
const config = require('./config');

async function startService() {
    console.log('🚀 Inicializando o Serviço de Notificações...\n');
    console.log('📋 Parâmetros de Configuração:');
    console.log(`   - URL RabbitMQ: ${config.rabbitmq.url}`);
    console.log(`   - Tópico: ${config.rabbitmq.topic}`);
    console.log(`   - Exchange: ${config.rabbitmq.exchange}`);
    console.log(`   - Host SMTP: ${config.email.host}`);
    console.log(`   - Ambiente: ${config.service.env}\n`);

    try {
        // Verificar conexão com servidor SMTP
        console.log('📧 Verificando conectividade com o servidor de e-mail...');
        const emailConnected = await emailService.verifyConnection();

        if (!emailConnected) {
            console.warn('⚠️  Aviso: Não foi possível estabelecer conexão com o servidor SMTP.');
            console.warn('   O serviço permanecerá ativo, contudo, o envio de e-mails poderá falhar.\n');
        }

        // Conectar ao RabbitMQ
        await rabbitmqService.connect();

        console.log('\n✅ Serviço de Notificações inicializado com sucesso.');
        console.log('👂 Monitorando fila de mensagens...\n');

    } catch (error) {
        console.error('❌ Erro crítico na inicialização do serviço:', error.message);
        process.exit(1);
    }
}

// Tratamento de sinais de encerramento
process.on('SIGINT', async () => {
    console.log('\n\n⚠️  Sinal de interrupção recebido (SIGINT).');
    console.log('🛑 Finalizando processos e encerrando o serviço...');

    await rabbitmqService.close();
    process.exit(0);
});

process.on('SIGTERM', async () => {
    console.log('\n\n⚠️  Sinal de término recebido (SIGTERM).');
    console.log('🛑 Encerrando o serviço de forma controlada...');

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
