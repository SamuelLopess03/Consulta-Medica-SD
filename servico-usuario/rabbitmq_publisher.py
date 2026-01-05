import pika
import json
import os
import time

class RabbitMQPublisher:
    def __init__(self):
        self.host = os.getenv('RABBITMQ_HOST', 'rabbitmq')
        self.user = os.getenv('RABBITMQ_USER', 'admin')
        self.password = os.getenv('RABBITMQ_PASSWORD', 'admin')
        self.exchange = 'notificacoes_exchange'
        self.routing_key = 'sd/notificacoes'
        self.connection = None
        self.channel = None

    def connect(self):
        retries = 5
        while retries > 0:
            try:
                print(f"Conectando ao RabbitMQ em {self.host}...", flush=True)
                credentials = pika.PlainCredentials(self.user, self.password)
                self.connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host=self.host,
                        credentials=credentials
                    )
                )
                self.channel = self.connection.channel()
                self.channel.exchange_declare(exchange=self.exchange, exchange_type='topic', durable=True)
                print("✅ Conectado ao RabbitMQ com sucesso!", flush=True)
                return True
            except Exception as e:
                print(f"⚠️  Erro ao conectar ao RabbitMQ ({self.host}): {e}. Tentando novamente em 5s...", flush=True)
                retries -= 1
                time.sleep(5)
        print("❌ Não foi possível conectar ao RabbitMQ após várias tentativas.", flush=True)
        return False

    def publish_notification(self, email, assunto, mensagem):
        """
        Publica uma notificação no formato esperado pelo serviço de notificações.
        Formato: {"email": "...", "assunto": "...", "mensagem": "..."}
        """
        if not self.channel or self.channel.is_closed:
            if not self.connect():
                print("❌ Não foi possível conectar ao RabbitMQ para publicar notificação.")
                return False

        payload = {
            'email': email,
            'assunto': assunto,
            'mensagem': mensagem
        }

        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=json.dumps(payload),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistente
                )
            )
            print(f"📨 Notificação publicada: {assunto} para {email}", flush=True)
            return True
        except Exception as e:
            print(f"❌ Erro ao publicar notificação: {e}", flush=True)
            return False

    def publish_event(self, event_type, data):
        """Método legado para compatibilidade"""
        if not self.channel or self.channel.is_closed:
            if not self.connect():
                print("Não foi possível conectar ao RabbitMQ para publicar o evento.")
                return

        payload = {
            'event': event_type,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'data': data
        }

        try:
            self.channel.basic_publish(
                exchange=self.exchange,
                routing_key=self.routing_key,
                body=json.dumps(payload),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # persistente
                )
            )
            print(f"Evento {event_type} publicado com sucesso.")
        except Exception as e:
            print(f"Erro ao publicar evento: {e}")

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()

# Singleton instance
publisher = RabbitMQPublisher()
