// Importa o módulo nodemailer para envio de e-mails
const nodemailer = require('nodemailer');
// Importa as configurações do sistema
const config = require('./config');

/**
 * Classe responsável por gerenciar o envio de e-mails do sistema.
 */
class EmailService {
  constructor() {
    // Inicializa o transportador como nulo
    this.transporter = null;
    // Chama o método para inicializar o transportador SMTP
    this.initializeTransporter();
  }

  /**
   * Configura o transportador do nodemailer usando as credenciais definidas no arquivo de configuração.
   */
  initializeTransporter() {
    try {
      // Cria o objeto transportador com os dados do host, porta e autenticação
      this.transporter = nodemailer.createTransport({
        host: config.email.host,
        port: config.email.port,
        secure: config.email.secure, // true para porta 465, false para outras
        auth: config.email.auth
      });

      console.log('✅ Transportador de e-mail inicializado com sucesso.');
    } catch (error) {
      // Registra erro caso a inicialização do transportador falhe
      console.error('❌ Falha ao inicializar o transportador de e-mail:', error.message);
    }
  }

  /**
   * Envia um e-mail formatado.
   * @param {string} to - Destinatário do e-mail
   * @param {string} subject - Assunto do e-mail
   * @param {string} message - Conteúdo da mensagem
   */
  async sendEmail(to, subject, message) {
    try {
      // Verifica se o transportador foi inicializado
      if (!this.transporter) {
        throw new Error('Transportador de e-mail não configurado.');
      }

      // Define as opções do e-mail
      const mailOptions = {
        from: config.email.from, // Remetente
        to: to,                  // Destinatário
        subject: subject,        // Assunto
        // Usa um template HTML para formatar o corpo do e-mail
        html: this.formatEmailTemplate(subject, message)
      };

      // Realiza o envio do e-mail de forma assíncrona
      const info = await this.transporter.sendMail(mailOptions);
      console.log(`📧 E-mail enviado com sucesso para ${to}. ID: ${info.messageId}`);
      return { success: true, messageId: info.messageId };
    } catch (error) {
      // Registra e retorna erro se o envio falhar
      console.error(`❌ Erro no envio de e-mail para ${to}:`, error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * Formata o conteúdo do e-mail usando um template HTML básico para melhorar a aparência.
   * @param {string} subject - Título que aparecerá no corpo do e-mail
   * @param {string} message - Mensagem principal
   */
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

  /**
   * Verifica se a conexão com o servidor SMTP está funcionando corretamente.
   */
  async verifyConnection() {
    try {
      if (!this.transporter) {
        throw new Error('Transportador de e-mail não disponível.');
      }
      // O método verify do nodemailer testa a autenticação e conexão
      await this.transporter.verify();
      console.log('✅ Conexão com o servidor SMTP validada com sucesso.');
      return true;
    } catch (error) {
      console.error('❌ Falha na validação da conexão SMTP:', error.message);
      return false;
    }
  }
}

// Exporta uma única instância da classe para ser usada em todo o sistema (Singleton)
module.exports = new EmailService();
