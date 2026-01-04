// Importa o serviço de gerenciamento do RabbitMQ
const rabbitmqService = require('./rabbitmq');
// Importa o serviço de envio de e-mails
const emailService = require('./emailService');
// Importa as configurações centrais do sistema
const config = require('./config');

/**
 * Função assíncrona que coordena a inicialização de todos os componentes do serviço.
 */
async function startService() {
    console.log('🚀 Inicializando o Serviço de Notificações...\n');

    // Lista os parâmetros carregados para conferência visual no console
    console.log('📋 Parâmetros de Configuração:');
    console.log(`   - URL RabbitMQ: ${config.rabbitmq.url}`);
    console.log(`   - Tópico: ${config.rabbitmq.topic}`);
    console.log(`   - Exchange: ${config.rabbitmq.exchange}`);
    console.log(`   - Host SMTP: ${config.email.host}`);
    console.log(`   - Ambiente: ${config.service.env}\n`);

    try {
        // Passo 1: Verificar se a conexão com o servidor SMTP (e-mail) está operando
        console.log('📧 Verificando conectividade com o servidor de e-mail...');
        const emailConnected = await emailService.verifyConnection();

        if (!emailConnected) {
            // Caso falhe, apenas emite um aviso mas permite que o serviço continue rodando
            console.warn('⚠️  Aviso: Não foi possível estabelecer conexão com o servidor SMTP.');
            console.warn('   O serviço permanecerá ativo, contudo, o envio de e-mails poderá falhar.\n');
        }

        // Passo 2: Estabelecer conexão com o broker de mensagens RabbitMQ
        // Internamente, este método também configura a exchange e inicia o consumo (listen)
        await rabbitmqService.connect();

        console.log('\n✅ Serviço de Notificações inicializado com sucesso.');
        console.log('👂 Monitorando fila de mensagens...\n');

    } catch (error) {
        // Qualquer erro crítico durante a subida do serviço forçará o encerramento da aplicação
        console.error('❌ Erro crítico na inicialização do serviço:', error.message);
        process.exit(1); // Encerra o processo com código de erro 1
    }
}

/**
 * Tratamento do sinal SIGINT (geralmente gerado por Ctrl+C no terminal).
 */
process.on('SIGINT', async () => {
    console.log('\n\n⚠️  Sinal de interrupção recebido (SIGINT).');
    console.log('🛑 Finalizando processos e encerrando o serviço...');

    // Tenta fechar a conexão com o RabbitMQ de forma limpa antes de fechar
    await rabbitmqService.close();
    process.exit(0); // Sucesso
});

/**
 * Tratamento do sinal SIGTERM (enviado por sistemas de orquestração como Docker ou Kubernetes).
 */
process.on('SIGTERM', async () => {
    console.log('\n\n⚠️  Sinal de término recebido (SIGTERM).');
    console.log('🛑 Encerrando o serviço de forma controlada...');

    await rabbitmqService.close();
    process.exit(0);
});

/**
 * Captura erros globais que não foram devidamente tratados com try/catch (Exceções Síncronas).
 */
process.on('uncaughtException', (error) => {
    console.error('❌ Erro não capturado:', error);
    process.exit(1);
});

/**
 * Captura rejeições de Promises que não possuem um catch associado (Exceções Assíncronas).
 */
process.on('unhandledRejection', (reason, promise) => {
    console.error('❌ Promise rejeitada não tratada:', reason);
    process.exit(1);
});

// Executa a função principal para iniciar o serviço
startService();
