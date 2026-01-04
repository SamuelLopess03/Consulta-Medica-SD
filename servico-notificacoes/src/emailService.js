const nodemailer = require('nodemailer');
const config = require('./config');

class EmailService {
  constructor() {
    this.transporter = null;
    this.initializeTransporter();
  }

  initializeTransporter() {
    try {
      this.transporter = nodemailer.createTransport({
        host: config.email.host,
        port: config.email.port,
        secure: config.email.secure,
        auth: config.email.auth
      });

      console.log('✅ Transportador de e-mail inicializado com sucesso.');
    } catch (error) {
      console.error('❌ Falha ao inicializar o transportador de e-mail:', error.message);
    }
  }

  async sendEmail(to, subject, message) {
    try {
      if (!this.transporter) {
        throw new Error('Transportador de e-mail não configurado.');
      }

      const mailOptions = {
        from: config.email.from,
        to: to,
        subject: subject,
        html: this.formatEmailTemplate(subject, message)
      };

      const info = await this.transporter.sendMail(mailOptions);
      console.log(`📧 E-mail enviado com sucesso para ${to}. ID: ${info.messageId}`);
      return { success: true, messageId: info.messageId };
    } catch (error) {
      console.error(`❌ Erro no envio de e-mail para ${to}:`, error.message);
      return { success: false, error: error.message };
    }
  }


  //Pra deixar o email mais bonito
  formatEmailTemplate(subject, message) {
    return `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
          }
          .header {
            background-color: #4CAF50;
            color: white;
            padding: 20px;
            text-align: center;
            border-radius: 5px 5px 0 0;
          }
          .content {
            background-color: #f9f9f9;
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 0 0 5px 5px;
          }
          .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 12px;
            color: #777;
          }
        </style>
      </head>
      <body>
        <div class="header">
          <h2>Sistema de Consultas Médicas</h2>
        </div>
        <div class="content">
          <h3>${subject}</h3>
          <p>${message}</p>
        </div>
        <div class="footer">
          <p>Esta é uma mensagem automática. Por favor, não responda este email.</p>
        </div>
      </body>
      </html>
    `;
  }

  async verifyConnection() {
    try {
      if (!this.transporter) {
        throw new Error('Transportador de e-mail não disponível.');
      }
      await this.transporter.verify();
      console.log('✅ Conexão com o servidor SMTP validada com sucesso.');
      return true;
    } catch (error) {
      console.error('❌ Falha na validação da conexão SMTP:', error.message);
      return false;
    }
  }
}

module.exports = new EmailService();
