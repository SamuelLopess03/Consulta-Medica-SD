const amqp = require('amqplib');
const config = require('./config');
const emailService = require('./emailService');

class RabbitMQService {
    constructor() {
        this.connection = null;
        this.channel = null;
        this.isConnected = false;
    }

    async connect() {
        try {
            console.log(`🔌 Conectando ao RabbitMQ em ${config.rabbitmq.url}...`);

            this.connection = await amqp.connect(config.rabbitmq.url);
            this.channel = await this.connection.createChannel();

            // Criar exchange do tipo 'topic'
            await this.channel.assertExchange(
                config.rabbitmq.exchange,
                config.rabbitmq.exchangeType,
                { durable: true }
            );

            // Criar fila exclusiva para este consumidor
            const queue = await this.channel.assertQueue('', { exclusive: true });

            // Fazer bind da fila ao exchange com o tópico
            await this.channel.bindQueue(
                queue.queue,
                config.rabbitmq.exchange,
                config.rabbitmq.topic
            );

            console.log(`✅ Conectado ao RabbitMQ`);
            console.log(`📡 Escutando no tópico: ${config.rabbitmq.topic}`);

            this.isConnected = true;

            // Configurar consumidor
            await this.startConsuming(queue.queue);

            // Tratar fechamento da conexão
            this.connection.on('close', () => {
                console.log('⚠️  Conexão com RabbitMQ fechada');
                this.isConnected = false;
                this.reconnect();
            });

            this.connection.on('error', (err) => {
                console.error('❌ Erro na conexão com RabbitMQ:', err.message);
                this.isConnected = false;
            });

        } catch (error) {
            console.error('❌ Erro ao conectar ao RabbitMQ:', error.message);
            this.isConnected = false;
            await this.reconnect();
        }
    }

    async startConsuming(queueName) {
        try {
            console.log(`👂 Iniciando consumo de mensagens da fila: ${queueName}`);

            await this.channel.consume(queueName, async (msg) => {
                if (msg !== null) {
                    try {
                        const content = msg.content.toString();
                        console.log(`\n📨 Nova mensagem recebida no tópico ${config.rabbitmq.topic}:`);
                        console.log(content);

                        // Parse da mensagem
                        const notification = JSON.parse(content);

                        // Processar notificação
                        await this.processNotification(notification);

                        // Confirmar processamento da mensagem
                        this.channel.ack(msg);
                        console.log('✅ Mensagem processada com sucesso\n');

                    } catch (error) {
                        console.error('❌ Erro ao processar mensagem:', error.message);
                        // Rejeitar mensagem e não recolocar na fila
                        this.channel.nack(msg, false, false);
                    }
                }
            }, { noAck: false });

        } catch (error) {
            console.error('❌ Erro ao iniciar consumo:', error.message);
        }
    }

    async processNotification(notification) {
        try {
            // Validar campos obrigatórios
            if (!notification.email) {
                throw new Error('Email do destinatário não fornecido');
            }

            if (!notification.subject && !notification.assunto) {
                throw new Error('Assunto da mensagem não fornecido');
            }

            if (!notification.message && !notification.mensagem) {
                throw new Error('Mensagem não fornecida');
            }

            // Suportar tanto português quanto inglês nos campos
            const email = notification.email;
            const subject = notification.subject || notification.assunto;
            const message = notification.message || notification.mensagem;

            console.log(`📧 Enviando email para: ${email}`);
            console.log(`📋 Assunto: ${subject}`);

            // Enviar email
            const result = await emailService.sendEmail(email, subject, message);

            if (result.success) {
                console.log(`✅ Notificação enviada com sucesso para ${email}`);
            } else {
                console.error(`❌ Falha ao enviar notificação: ${result.error}`);
            }

        } catch (error) {
            console.error('❌ Erro ao processar notificação:', error.message);
            throw error;
        }
    }

    async reconnect() {
        console.log('🔄 Tentando reconectar em 5 segundos...');
        setTimeout(() => {
            this.connect();
        }, 5000);
    }

    async close() {
        try {
            if (this.channel) {
                await this.channel.close();
            }
            if (this.connection) {
                await this.connection.close();
            }
            console.log('👋 Conexão com RabbitMQ fechada');
        } catch (error) {
            console.error('❌ Erro ao fechar conexão:', error.message);
        }
    }
}

module.exports = new RabbitMQService();
