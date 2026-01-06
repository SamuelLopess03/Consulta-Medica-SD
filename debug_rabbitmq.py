
import pika
import json
import os

HOST = 'rabbitmq'
USER = 'admin'
PASS = 'admin'

credentials = pika.PlainCredentials(USER, PASS)
connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, credentials=credentials))
channel = connection.channel()

channel.exchange_declare(exchange='notificacoes_exchange', exchange_type='topic', durable=True)

msg = {
    'email': 'roddanadao@gmail.com',
    'assunto': 'Teste Manual de Debug',
    'mensagem': 'Se chegou isso aqui, o RabbitMQ e o Node estao funcionando.'
}

channel.basic_publish(
    exchange='notificacoes_exchange',
    routing_key='sd/notificacoes',
    body=json.dumps(msg)
)

print("Enviado!")
connection.close()
