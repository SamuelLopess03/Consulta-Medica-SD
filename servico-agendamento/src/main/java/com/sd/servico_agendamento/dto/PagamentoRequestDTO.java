package com.sd.servico_agendamento.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
public class PagamentoRequestDTO {
    @JsonProperty("agendamento_id")
    private Long agendamentoId;
    
    private Double total;
    
    @JsonProperty("payment_method")
    private String paymentMethod;
    
    @JsonProperty("customer_email")
    private String customerEmail;
}
