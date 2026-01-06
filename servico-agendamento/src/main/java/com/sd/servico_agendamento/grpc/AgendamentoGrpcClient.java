package com.sd.servico_agendamento.grpc;

import com.sd.servico_agendamento.grpc.stubs.*;
import lombok.RequiredArgsConstructor;

import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class AgendamentoGrpcClient {

    private final AgendamentoServiceGrpc.AgendamentoServiceBlockingStub stub;

    public ConsultaResponse agendar(Long pacienteId, String pacienteEmail, Long medicoId, String medicoEmail,
            String especialidade, String dataHora) {
        AgendarConsultaRequest request = AgendarConsultaRequest.newBuilder()
                .setPacienteId(pacienteId)
                .setPacienteEmail(pacienteEmail)
                .setMedicoId(medicoId)
                .setMedicoEmail(medicoEmail)
                .setEspecialidade(especialidade)
                .setDataHora(dataHora)
                .build();
        return stub.agendarConsulta(request);
    }

    public ConsultaResponse consultarStatus(Long consultaId) {
        ConsultarStatusRequest request = ConsultarStatusRequest.newBuilder()
                .setConsultaId(consultaId)
                .build();
        return stub.consultarStatus(request);
    }

    public List<Horario> listarHorarios(Long medicoId, String especialidade) {
        ListarHorariosRequest request = ListarHorariosRequest.newBuilder()
                .setMedicoId(medicoId)
                .setEspecialidade(especialidade)
                .build();
        return stub.listarHorariosDisponiveis(request).getDisponiveisList();
    }

    public ConsultaResponse cancelar(Long consultaId) {
        CancelarConsultaRequest request = CancelarConsultaRequest.newBuilder()
                .setConsultaId(consultaId)
                .build();
        return stub.cancelarConsulta(request);
    }

    public ConsultaResponse atualizarStatus(Long consultaId, String novoStatus) {
        AtualizarStatusRequest request = AtualizarStatusRequest.newBuilder()
                .setConsultaId(consultaId)
                .setNovoStatus(novoStatus)
                .build();
        return stub.atualizarStatusConsulta(request);
    }
}
