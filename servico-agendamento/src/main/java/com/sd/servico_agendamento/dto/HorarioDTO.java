package com.sd.servico_agendamento.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class HorarioDTO {
    private Long id;
    private Long medicoId;
    private String dataHora;
    private boolean disponivel;
}
