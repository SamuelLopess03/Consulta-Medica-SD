const amqp = require('amqplib');
require('dotenv').config();

const config = {
    rabbitmqUrl: process.env.RABBITMQ_URL || 'amqp://admin:admin@localhost:5672',
    exchange: 'notificacoes_exchange',
    topic: 'sd/notificacoes'
};

async function enviarNotificacaoTeste() {
    let connection;
    let channel;

    try {
        console.log('🔌 Conectando ao RabbitMQ...');
        connection = await amqp.connect(config.rabbitmqUrl);
        channel = await connection.createChannel();

        console.log('📡 Configurando Exchange de destino...');
        await channel.assertExchange(config.exchange, 'topic', { durable: true });

        // Mensagem de teste
        const notificacao = {
            email: 'roddanadao@gmail.com',
            assunto: 'Teste de Notificação - Sistema de Consultas Médicas',
            mensagem: 'Esta é uma mensagem de teste do sistema de notificações. Se você recebeu este e-mail, o serviço está operando corretamente!'
        };

        console.log('\n📨 Publicando notificação de teste:');
        console.log(JSON.stringify(notificacao, null, 2));

        channel.publish(
            config.exchange,
            config.topic,
            Buffer.from(JSON.stringify(notificacao)),
            { persistent: true }
        );

        console.log('\n✅ Notificação enviada com sucesso para o Broker.');
        console.log(`   Exchange: ${config.exchange}`);
        console.log(`   Tópico: ${config.topic}`);
        console.log('\n👀 Verifique os logs do serviço de notificações para validar o processamento.');

    } catch (error) {
        console.error('❌ Falha na publicação da notificação de teste:', error.message);
        process.exit(1);
    } finally {
        if (channel) await channel.close();
        if (connection) await connection.close();
    }
}

// Executar teste
enviarNotificacaoTeste();
