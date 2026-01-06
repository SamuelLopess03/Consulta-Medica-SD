package com.sd.servico_agendamento.messaging;

import com.sd.servico_agendamento.dto.NotificacaoDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.amqp.rabbit.core.RabbitTemplate;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
@Slf4j
public class NotificationProducer {

    private final RabbitTemplate rabbitTemplate;

    @Value("${notificacoes.exchange}")
    private String exchange;

    @Value("${notificacoes.routing-key}")
    private String routingKey;

    public void enviarNotificacao(String email, String assunto, String mensagem) {
        NotificacaoDTO notificacao = NotificacaoDTO.builder()
                .email(email)
                .assunto(assunto)
                .mensagem(mensagem)
                .build();

        try {
            log.info("Enviando notificação para RabbitMQ: {}", email);
            rabbitTemplate.convertAndSend(exchange, routingKey, notificacao);
        } catch (Exception e) {
            log.error("Erro ao enviar notificação para RabbitMQ: {}", e.getMessage());
        }
    }
}
