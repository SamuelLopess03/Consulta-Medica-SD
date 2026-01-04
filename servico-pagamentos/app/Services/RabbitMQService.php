<?php

namespace App\Services;

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

class RabbitMQService
{
    private $connection;
    private $channel;

    public function __construct()
    {
        $this->connection = new AMQPStreamConnection(
            env('RABBITMQ_HOST'),
            env('RABBITMQ_PORT'),
            env('RABBITMQ_USER'),
            env('RABBITMQ_PASSWORD'),
            env('RABBITMQ_VHOST')
        );

        $this->channel = $this->connection->channel();
    }

    public function publishToExchange(
        string $exchange,
        string $routingKey,
        array $data
    ) {
        $this->channel->exchange_declare(
            $exchange,
            'topic', // pode ser direct, topic, fanout
            false,
            true,
            false
        );

        $message = new AMQPMessage(
            json_encode($data),
            ['delivery_mode' => AMQPMessage::DELIVERY_MODE_PERSISTENT]
        );

        $this->channel->basic_publish(
            $message,
            $exchange,
            $routingKey
        );
    }

    public function close()
    {
        $this->channel->close();
        $this->connection->close();
    }
}
