package com.sd.servico_agendamento.service;

import com.sd.servico_agendamento.model.Consulta;
import com.sd.servico_agendamento.model.Horario;
import com.sd.servico_agendamento.model.StatusConsulta;
import com.sd.servico_agendamento.repository.ConsultaRepository;
import com.sd.servico_agendamento.repository.HorarioRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Optional;

@Service
@RequiredArgsConstructor
public class AgendamentoService {

    private final ConsultaRepository consultaRepository;
    private final HorarioRepository horarioRepository;
    private static final DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;

    @Transactional
    public Consulta agendar(Long pacienteId, Long medicoId, String especialidade, String dataHoraStr) {
        LocalDateTime dataHora = LocalDateTime.parse(dataHoraStr, formatter);

        Optional<Horario> horarioOpt = horarioRepository.findByMedicoIdAndDataHora(medicoId, dataHora);
        
        Horario horario;
        if (horarioOpt.isPresent()) {
            horario = horarioOpt.get();
            if (!horario.isDisponivel()) {
                throw new RuntimeException("Horário já está ocupado por outra consulta.");
            }
        } else {
            horario = Horario.builder()
                    .medicoId(medicoId)
                    .especialidade(especialidade)
                    .dataHora(dataHora)
                    .disponivel(true)
                    .build();
            horario = horarioRepository.save(horario);
        }

        Consulta consulta = Consulta.builder()
                .pacienteId(pacienteId)
                .medicoId(medicoId)
                .especialidade(especialidade)
                .horario(horario)
                .status(StatusConsulta.AGENDADA)
                .build();

        horario.setDisponivel(false);
        horarioRepository.save(horario);

        return consultaRepository.save(consulta);
    }

    public Optional<Consulta> buscarPorId(Long id) {
        return consultaRepository.findById(id);
    }

    public List<Horario> listarDisponiveis(Long medicoId, String especialidade) {
        return horarioRepository.findByMedicoIdAndEspecialidadeAndDisponivelTrue(medicoId, especialidade);
    }

    @Transactional
    public Consulta cancelar(Long id) {
        Consulta consulta = consultaRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Consulta não encontrada."));

        if (consulta.getStatus() == StatusConsulta.CANCELADA) {
            return consulta;
        }

        consulta.setStatus(StatusConsulta.CANCELADA);
        
        Horario horario = consulta.getHorario();
        horario.setDisponivel(true);
        horarioRepository.save(horario);

        return consultaRepository.save(consulta);
    }

    @Transactional
    public Consulta atualizarStatus(Long id, StatusConsulta novoStatus) {
        Consulta consulta = consultaRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Consulta não encontrada."));
        
        consulta.setStatus(novoStatus);
        return consultaRepository.save(consulta);
    }
    
}
