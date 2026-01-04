require('dotenv').config();

module.exports = {
  // RabbitMQ
  rabbitmq: {
    url: process.env.RABBITMQ_URL || 'amqp://localhost:5672',
    topic: process.env.RABBITMQ_TOPIC || 'sd/notificacoes',
    exchange: 'notificacoes_exchange',
    exchangeType: 'topic'
  },
  // SMTP Email
  email: {
    host: process.env.EMAIL_HOST || 'smtp.gmail.com',
    port: parseInt(process.env.EMAIL_PORT) || 587,
    secure: process.env.EMAIL_SECURE === 'true',
    auth: {
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASS
    },
    from: process.env.EMAIL_FROM || 'Sistema de Consultas Médicas <noreply@consultamedica.com>'
  },
  // General
  service: {
    port: parseInt(process.env.PORT) || 3003,
    env: process.env.NODE_ENV || 'development'
  }
};

