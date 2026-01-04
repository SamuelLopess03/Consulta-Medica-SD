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
            console.log(`🔌 Iniciando conexão com o RabbitMQ em ${config.rabbitmq.url}...`);

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

            console.log(`✅ Conexão estabelecida com o RabbitMQ.`);
            console.log(`📡 Escutando no tópico: ${config.rabbitmq.topic}`);

            this.isConnected = true;

            // Configurar consumidor
            await this.startConsuming(queue.queue);

            // Tratar fechamento da conexão
            this.connection.on('close', () => {
                console.warn('⚠️  Conexão com o RabbitMQ encerrada.');
                this.isConnected = false;
                this.reconnect();
            });

            this.connection.on('error', (err) => {
                console.error('❌ Erro na conexão com o RabbitMQ:', err.message);
                this.isConnected = false;
            });

        } catch (error) {
            console.error('❌ Falha ao conectar ao RabbitMQ:', error.message);
            this.isConnected = false;
            await this.reconnect();
        }
    }

    async startConsuming(queueName) {
        try {
            console.log(`👂 Iniciando consumo de mensagens na fila: ${queueName}`);

            await this.channel.consume(queueName, async (msg) => {
                if (msg !== null) {
                    try {
                        const content = msg.content.toString();
                        console.log(`\n📨 Mensagem recebida no tópico ${config.rabbitmq.topic}:`);
                        console.log(content);

                        // Parse da mensagem
                        const notification = JSON.parse(content);

                        // Processar notificação
                        await this.processNotification(notification);

                        // Confirmar processamento da mensagem
                        this.channel.ack(msg);
                        console.log('✅ Mensagem processada com sucesso.\n');

                    } catch (error) {
                        console.error('❌ Erro ao processar mensagem recebida:', error.message);
                        // Rejeitar mensagem e não recolocar na fila
                        this.channel.nack(msg, false, false);
                    }
                }
            }, { noAck: false });

        } catch (error) {
            console.error('❌ Falha ao iniciar o consumo de mensagens:', error.message);
        }
    }

    async processNotification(notification) {
        try {
            // Validar campos obrigatórios
            if (!notification.email) {
                throw new Error('Campo "email" do destinatário ausente.');
            }

            if (!notification.subject && !notification.assunto) {
                throw new Error('Campo de "assunto" ausente.');
            }

            if (!notification.message && !notification.mensagem) {
                throw new Error('Campo de "mensagem" ausente.');
            }

            // Suportar tanto português quanto inglês nos campos
            const email = notification.email;
            const subject = notification.subject || notification.assunto;
            const message = notification.message || notification.mensagem;

            console.log(`📧 Processando envio de e-mail para: ${email}`);
            console.log(`📋 Assunto: ${subject}`);

            // Enviar email
            const result = await emailService.sendEmail(email, subject, message);

            if (result.success) {
                console.log(`✅ Notificação enviada com sucesso para ${email}.`);
            } else {
                console.error(`❌ Falha no envio da notificação: ${result.error}`);
            }

        } catch (error) {
            console.error('❌ Erro no processamento da notificação:', error.message);
            throw error;
        }
    }

    async reconnect() {
        console.log('🔄 Tentando reconexão em 5 segundos...');
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
            console.log('👋 Conexões com o RabbitMQ encerradas corretamente.');
        } catch (error) {
            console.error('❌ Erro ao encerrar conexões:', error.message);
        }
    }
}

module.exports = new RabbitMQService();
