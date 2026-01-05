package com.sd.servico_agendamento.controller;

import com.sd.servico_agendamento.dto.ConsultaDTO;
import com.sd.servico_agendamento.dto.HorarioDTO;
import com.sd.servico_agendamento.model.Consulta;
import com.sd.servico_agendamento.model.StatusConsulta;
import com.sd.servico_agendamento.service.AgendamentoService;
import com.sd.servico_agendamento.mapper.AgendamentoMapper;
import lombok.RequiredArgsConstructor;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/agendamentos")
@RequiredArgsConstructor
public class AgendamentoController {

    private final AgendamentoService agendamentoService;
    private final AgendamentoMapper mapper;

    @PostMapping
    public ResponseEntity<ConsultaDTO> agendar(@RequestBody ConsultaRequest request) {
        Consulta consulta = agendamentoService.agendar(
                request.getPacienteId(),
                request.getMedicoId(),
                request.getEspecialidade(),
                request.getDataHora()
        );
        return ResponseEntity.ok(mapper.toDTO(consulta));
    }

    @GetMapping("/{id}")
    public ResponseEntity<ConsultaDTO> consultarStatus(@PathVariable Long id) {
        return agendamentoService.buscarPorId(id)
                .map(mapper::toDTO)
                .map(ResponseEntity::ok)
                .orElse(ResponseEntity.notFound().build());
    }

    @GetMapping("/horarios")
    public ResponseEntity<List<HorarioDTO>> listarHorarios(
            @RequestParam Long medicoId,
            @RequestParam String especialidade) {
        
        List<HorarioDTO> dtos = agendamentoService.listarDisponiveis(medicoId, especialidade)
                .stream()
                .map(h -> HorarioDTO.builder()
                        .id(h.getId())
                        .medicoId(h.getMedicoId())
                        .dataHora(h.getDataHora().toString())
                        .disponivel(h.isDisponivel())
                        .build())
                .collect(Collectors.toList());
        
        return ResponseEntity.ok(dtos);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<ConsultaDTO> cancelar(@PathVariable Long id) {
        Consulta consulta = agendamentoService.cancelar(id);
        return ResponseEntity.ok(mapper.toDTO(consulta));
    }

    @PutMapping("/{id}/status")
    public ResponseEntity<ConsultaDTO> atualizarStatus(
            @PathVariable Long id,
            @RequestParam String status) {
        Consulta consulta = agendamentoService.atualizarStatus(id, StatusConsulta.valueOf(status));
        return ResponseEntity.ok(mapper.toDTO(consulta));
    }

    @lombok.Data
    public static class ConsultaRequest {
        private Long pacienteId;
        private Long medicoId;
        private String especialidade;
        private String dataHora;
    }
}
