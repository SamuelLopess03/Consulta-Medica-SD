package com.sd.servico_agendamento.controller;

import com.sd.servico_agendamento.grpc.AgendamentoGrpcClient;
import com.sd.servico_agendamento.dto.ConsultaDTO;
import com.sd.servico_agendamento.dto.HorarioDTO;
import com.sd.servico_agendamento.mapper.AgendamentoMapper;
import com.sd.servico_agendamento.grpc.stubs.ConsultaResponse;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/agendamentos")
@RequiredArgsConstructor
public class AgendamentoController {

    private final AgendamentoGrpcClient grpcClient;
    private final AgendamentoMapper mapper;

    @PostMapping
    public ResponseEntity<ConsultaDTO> agendar(@RequestBody ConsultaRequest request) {
        ConsultaResponse response = grpcClient.agendar(
                request.getPacienteId(),
                request.getPacienteEmail(),
                request.getMedicoId(),
                request.getMedicoEmail(),
                request.getEspecialidade(),
                request.getDataHora());
        return ResponseEntity.ok(mapper.toDTO(response));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ConsultaDTO> consultarStatus(@PathVariable Long id) {
        try {
            ConsultaResponse response = grpcClient.consultarStatus(id);
            return ResponseEntity.ok(mapper.toDTO(response));
        } catch (Exception e) {
            return ResponseEntity.notFound().build();
        }
    }

    @GetMapping("/horarios")
    public ResponseEntity<List<HorarioDTO>> listarHorarios(
            @RequestParam Long medicoId,
            @RequestParam String especialidade) {

        List<HorarioDTO> dtos = grpcClient.listarHorarios(medicoId, especialidade)
                .stream()
                .map(mapper::toDTO)
                .collect(Collectors.toList());

        return ResponseEntity.ok(dtos);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ConsultaDTO> cancelar(@PathVariable Long id) {
        com.sd.servico_agendamento.grpc.stubs.ConsultaResponse response = grpcClient.cancelar(id);
        return ResponseEntity.ok(mapper.toDTO(response));
    }

    @PutMapping("/{id}/status")
    public ResponseEntity<ConsultaDTO> atualizarStatus(
            @PathVariable Long id,
            @RequestParam String status) {
        com.sd.servico_agendamento.grpc.stubs.ConsultaResponse response = grpcClient.atualizarStatus(id, status);
        return ResponseEntity.ok(mapper.toDTO(response));
    }

    @lombok.Data
    public static class ConsultaRequest {
        private Long pacienteId;
        private String pacienteEmail;
        private Long medicoId;
        private String medicoEmail;
        private String especialidade;
        private String dataHora;
    }
}
