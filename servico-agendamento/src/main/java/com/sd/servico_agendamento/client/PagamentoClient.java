package com.sd.servico_agendamento.client;

import com.sd.servico_agendamento.dto.PagamentoRequestDTO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestTemplate;

@Component
@RequiredArgsConstructor
@Slf4j
public class PagamentoClient {

    private final RestTemplate restTemplate;

    @Value("${service.pagamentos.url}")
    private String paymentServiceUrl;

    public void solicitarPagamento(PagamentoRequestDTO request) {
        try {
            log.info("Solicitando pagamento para agendamento {}: URL={}", request.getAgendamentoId(), paymentServiceUrl);
            restTemplate.postForEntity(paymentServiceUrl, request, Object.class);
            log.info("Pagamento solicitado com sucesso.");
        } catch (Exception e) {
            log.error("Erro ao solicitar pagamento para agendamento {}: {}", request.getAgendamentoId(), e.getMessage());
        }
    }
}
