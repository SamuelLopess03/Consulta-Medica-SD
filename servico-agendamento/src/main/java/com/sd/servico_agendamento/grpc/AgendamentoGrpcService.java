package com.sd.servico_agendamento.grpc;

import com.sd.servico_agendamento.grpc.stubs.*;
import com.sd.servico_agendamento.mapper.AgendamentoMapper;
import com.sd.servico_agendamento.model.StatusConsulta;
import com.sd.servico_agendamento.service.AgendamentoService;
import io.grpc.stub.StreamObserver;
import lombok.RequiredArgsConstructor;
import org.springframework.grpc.server.service.GrpcService;

import java.util.List;
import java.util.stream.Collectors;

@GrpcService
@RequiredArgsConstructor
public class AgendamentoGrpcService extends AgendamentoServiceGrpc.AgendamentoServiceImplBase {

    private final AgendamentoService agendamentoService;
    private final AgendamentoMapper mapper;

    @Override
    public void agendarConsulta(AgendarConsultaRequest request, StreamObserver<ConsultaResponse> responseObserver) {
        try {
            com.sd.servico_agendamento.model.Consulta consulta = agendamentoService.agendar(
                    request.getPacienteId(),
                    request.getMedicoId(),
                    request.getEspecialidade(),
                    request.getDataHora()
            );
            responseObserver.onNext(mapper.toGrpcResponse(consulta));
            responseObserver.onCompleted();
        } catch (Exception e) {
            responseObserver.onError(io.grpc.Status.INTERNAL
                    .withDescription(e.getMessage())
                    .asRuntimeException());
        }
    }

    @Override
    public void consultarStatus(ConsultarStatusRequest request, StreamObserver<ConsultaResponse> responseObserver) {
        agendamentoService.buscarPorId(request.getConsultaId())
                .map(mapper::toGrpcResponse)
                .ifPresentOrElse(
                        responseObserver::onNext,
                        () -> responseObserver.onError(io.grpc.Status.NOT_FOUND.asRuntimeException())
                );
        responseObserver.onCompleted();
    }

    @Override
    public void listarHorariosDisponiveis(ListarHorariosRequest request, StreamObserver<ListarHorariosResponse> responseObserver) {
        List<com.sd.servico_agendamento.model.Horario> disponiveis = agendamentoService.listarDisponiveis(
                request.getMedicoId(),
                request.getEspecialidade()
        );

        ListarHorariosResponse response = ListarHorariosResponse.newBuilder()
                .addAllDisponiveis(disponiveis.stream()
                        .map(mapper::toGrpcHorario)
                        .collect(Collectors.toList()))
                .build();

        responseObserver.onNext(response);
        responseObserver.onCompleted();
    }

    @Override
    public void cancelarConsulta(CancelarConsultaRequest request, StreamObserver<ConsultaResponse> responseObserver) {
        try {
            com.sd.servico_agendamento.model.Consulta consulta = agendamentoService.cancelar(request.getConsultaId());
            responseObserver.onNext(mapper.toGrpcResponse(consulta));
            responseObserver.onCompleted();
        } catch (Exception e) {
            responseObserver.onError(io.grpc.Status.INTERNAL
                    .withDescription(e.getMessage())
                    .asRuntimeException());
        }
    }

    @Override
    public void atualizarStatusConsulta(AtualizarStatusRequest request, StreamObserver<ConsultaResponse> responseObserver) {
        try {
            com.sd.servico_agendamento.model.Consulta consulta = agendamentoService.atualizarStatus(
                    request.getConsultaId(),
                    StatusConsulta.valueOf(request.getNovoStatus())
            );
            responseObserver.onNext(mapper.toGrpcResponse(consulta));
            responseObserver.onCompleted();
        } catch (Exception e) {
            responseObserver.onError(io.grpc.Status.INTERNAL
                    .withDescription(e.getMessage())
                    .asRuntimeException());
        }
    }
}
