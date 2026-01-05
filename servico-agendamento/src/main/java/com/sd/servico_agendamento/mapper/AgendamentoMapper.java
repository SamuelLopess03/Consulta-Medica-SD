package com.sd.servico_agendamento.mapper;

import com.sd.servico_agendamento.dto.ConsultaDTO;
import com.sd.servico_agendamento.grpc.stubs.ConsultaResponse;
import com.sd.servico_agendamento.model.Consulta;
import com.sd.servico_agendamento.model.Horario;
import org.springframework.stereotype.Component;

import java.time.format.DateTimeFormatter;

@Component
public class AgendamentoMapper {

    private static final DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

    public ConsultaDTO toDTO(Consulta consulta) {
        return ConsultaDTO.builder()
                .id(consulta.getId())
                .pacienteId(consulta.getPacienteId())
                .medicoId(consulta.getMedicoId())
                .especialidade(consulta.getEspecialidade())
                .dataHora(consulta.getHorario().getDataHora().format(formatter))
                .status(consulta.getStatus().name())
                .build();
    }

    public ConsultaResponse toGrpcResponse(Consulta consulta) {
        return ConsultaResponse.newBuilder()
                .setId(consulta.getId())
                .setPacienteId(consulta.getPacienteId())
                .setMedicoId(consulta.getMedicoId())
                .setEspecialidade(consulta.getEspecialidade())
                .setDataHora(consulta.getHorario().getDataHora().format(formatter))
                .setStatus(consulta.getStatus().name())
                .build();
    }

    public com.sd.servico_agendamento.grpc.stubs.Horario toGrpcHorario(Horario horario) {
        return com.sd.servico_agendamento.grpc.stubs.Horario.newBuilder()
                .setId(horario.getId())
                .setMedicoId(horario.getMedicoId())
                .setDataHora(horario.getDataHora().format(formatter))
                .setDisponivel(horario.isDisponivel())
                .build();
    }
}
