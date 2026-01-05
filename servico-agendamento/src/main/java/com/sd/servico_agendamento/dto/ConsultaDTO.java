package com.sd.servico_agendamento.dto;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class ConsultaDTO {
    private Long id;
    private Long pacienteId;
    private Long medicoId;
    private String especialidade;
    private String dataHora;
    private String status;
    private String mensagem;
}
