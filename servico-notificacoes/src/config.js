// Carrega as variáveis de ambiente do arquivo .env para o objeto process.env
require('dotenv').config();

// Exporta um objeto contendo as configurações organizadas por categorias
module.exports = {
  // Configurações relacionadas ao RabbitMQ
  rabbitmq: {
    // URL de conexão com o RabbitMQ, obtida da variável de ambiente ou usando o padrão 'amqp://localhost:5672'
    url: process.env.RABBITMQ_URL || 'amqp://localhost:5672',
    // Tópico/Fila que o serviço irá escutar, padrão 'sd/notificacoes'
    topic: process.env.RABBITMQ_TOPIC || 'sd/notificacoes',
    // Nome da exchange utilizada para mensagens baseadas em tópicos
    exchange: 'notificacoes_exchange',
    // Tipo de exchange (topic permite roteamento via chaves de roteamento com curingas)
    exchangeType: 'topic'
  },
  // Configurações relacionadas ao envio de e-mails via SMTP
  email: {
    // Endereço do servidor SMTP, padrão Google (Gmail)
    host: process.env.EMAIL_HOST || 'smtp.gmail.com',
    // Porta do servidor SMTP, padrão 587 (comum para TLS/STARTTLS)
    port: parseInt(process.env.EMAIL_PORT) || 587,
    // Define se deve usar conexão segura (SSL) no nível da conexão (geralmente porta 465)
    secure: process.env.EMAIL_SECURE === 'true',
    // Credenciais de autenticação do servidor de e-mail
    auth: {
      user: process.env.EMAIL_USER, // Nome de usuário/E-mail de envio
      pass: process.env.EMAIL_PASS  // Senha ou senha de aplicativo para autenticação
    },
    // Remetente padrão que aparecerá nos e-mails enviados
    from: process.env.EMAIL_FROM || 'Sistema de Consultas Médicas <noreply@consultamedica.com>'
  },
  // Configurações gerais do serviço
  service: {
    // Porta em que o serviço será executado, convertida para inteiro ou padrão 3003
    port: parseInt(process.env.PORT) || 3003,
    // Ambiente de execução (ex: development, production), padrão development
    env: process.env.NODE_ENV || 'development'
  }
};
