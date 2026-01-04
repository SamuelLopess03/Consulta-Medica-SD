// Importa a biblioteca amqplib para lidar com o protocolo AMQP (RabbitMQ)
const amqp = require('amqplib');
// Importa as configurações do sistema
const config = require('./config');
// Importa o serviço de e-mail para processar os envios
const emailService = require('./emailService');

/**
 * Classe responsável pela comunicação com o RabbitMQ, lidando com filas e tópicos.
 */
class RabbitMQService {
    constructor() {
        this.connection = null; // Armazena a conexão com o broker
        this.channel = null;    // Armazena o canal de comunicação aberto na conexão
        this.isConnected = false; // Flag para indicar o estado da conexão
    }

    /**
     * Estabelece a conexão inicial com o RabbitMQ e configura o ambiente de mensagens.
     */
    async connect() {
        try {
            console.log(`🔌 Iniciando conexão com o RabbitMQ em ${config.rabbitmq.url}...`);

            // 1. Criar a conexão física com o servidor RabbitMQ
            this.connection = await amqp.connect(config.rabbitmq.url);

            // 2. Criar um canal virtual dentro da conexão
            this.channel = await this.connection.createChannel();

            // 3. Garantir que a Exchange (Central de Distribuição) exista no servidor
            // Tipo 'topic' permite roteamento de mensagens baseado em chaves (ex: sd.notificacoes.email)
            await this.channel.assertExchange(
                config.rabbitmq.exchange,
                config.rabbitmq.exchangeType,
                { durable: true } // durable: true garante que a exchange sobreviva a reinícios do broker
            );

            // 4. Criar uma fila que será exclusiva para este processo do serviço
            // exclusive: true indica que a fila será deletada quando a conexão fechar
            const queue = await this.channel.assertQueue('', { exclusive: true });

            // 5. Vincular a fila à exchange para que ela receba mensagens do tópico configurado
            await this.channel.bindQueue(
                queue.queue,
                config.rabbitmq.exchange,
                config.rabbitmq.topic
            );

            console.log(`✅ Conexão estabelecida com o RabbitMQ.`);
            console.log(`📡 Escutando no tópico: ${config.rabbitmq.topic}`);

            this.isConnected = true;

            // 6. Iniciar o processo de escuta (consumo) de mensagens enviadas para a fila
            await this.startConsuming(queue.queue);

            // Eventos para tratar quedas de conexão de forma resiliente
            this.connection.on('close', () => {
                console.warn('⚠️  Conexão com o RabbitMQ encerrada.');
                this.isConnected = false;
                this.reconnect(); // Tenta reconectar automaticamente
            });

            this.connection.on('error', (err) => {
                console.error('❌ Erro na conexão com o RabbitMQ:', err.message);
                this.isConnected = false;
            });

        } catch (error) {
            console.error('❌ Falha ao conectar ao RabbitMQ:', error.message);
            this.isConnected = false;
            // Tenta reconectar se a conexão falhar logo no início
            await this.reconnect();
        }
    }

    /**
     * Inicia a captura de mensagens da fila e define como processá-las.
     * @param {string} queueName - Nome da fila a ser monitorada
     */
    async startConsuming(queueName) {
        try {
            console.log(`👂 Iniciando consumo de mensagens na fila: ${queueName}`);

            // Inicia o consumo no canal
            await this.channel.consume(queueName, async (msg) => {
                if (msg !== null) {
                    try {
                        // Converte o buffer da mensagem em string
                        const content = msg.content.toString();
                        console.log(`\n📨 Mensagem recebida no tópico ${config.rabbitmq.topic}:`);
                        console.log(content);

                        // Transforma a string JSON em objeto JavaScript
                        const notification = JSON.parse(content);

                        // Chama o processamento lógico da notificação
                        await this.processNotification(notification);

                        // Confirma para o RabbitMQ que a mensagem foi processada com sucesso (Acknowledge)
                        this.channel.ack(msg);
                        console.log('✅ Mensagem processada com sucesso.\n');

                    } catch (error) {
                        console.error('❌ Erro ao processar mensagem recebida:', error.message);
                        // Rejeita a mensagem (Negative Acknowledge)
                        // false, false: não reinserir na fila para evitar loops infinitos de erro
                        this.channel.nack(msg, false, false);
                    }
                }
            }, {
                // noAck: false obriga o envio manual do 'ack' após o processamento
                noAck: false
            });

        } catch (error) {
            console.error('❌ Falha ao iniciar o consumo de mensagens:', error.message);
        }
    }

    /**
     * Contém a lógica de negócio para interpretar a notificação e disparar o e-mail.
     * @param {Object} notification - Objeto contendo dados do e-mail
     */
    async processNotification(notification) {
        try {
            // Valida se os dados necessários para o envio existem no objeto
            if (!notification.email) {
                throw new Error('Campo "email" do destinatário ausente.');
            }

            if (!notification.subject && !notification.assunto) {
                throw new Error('Campo de "assunto" ausente.');
            }

            if (!notification.message && !notification.mensagem) {
                throw new Error('Campo de "mensagem" ausente.');
            }

            // Suporta propriedades tanto em inglês quanto em português (flexibilidade)
            const email = notification.email;
            const subject = notification.subject || notification.assunto;
            const message = notification.message || notification.mensagem;

            console.log(`📧 Processando envio de e-mail para: ${email}`);
            console.log(`📋 Assunto: ${subject}`);

            // Delega o envio real para o emailService
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

    /**
     * Gerencia a tentativa de reconexão após um intervalo de 5 segundos.
     */
    async reconnect() {
        console.log('🔄 Tentando reconexão em 5 segundos...');
        setTimeout(() => {
            this.connect();
        }, 5000);
    }

    /**
     * Fecha as conexões e canais de forma segura durante o encerramento do app.
     */
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

// Exporta uma única instância do serviço (Singleton)
module.exports = new RabbitMQService();
