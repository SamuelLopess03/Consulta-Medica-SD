package com.sd.servico_agendamento.repository;

import com.sd.servico_agendamento.model.Horario;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Repository
public interface HorarioRepository extends JpaRepository<Horario, Long> {
    List<Horario> findByMedicoIdAndEspecialidadeAndDisponivelTrue(Long medicoId, String especialidade);
    List<Horario> findByMedicoIdAndDataHoraBetweenAndDisponivelTrue(Long medicoId, LocalDateTime start, LocalDateTime end);
    Optional<Horario> findByMedicoIdAndDataHora(Long medicoId, LocalDateTime dataHora);
}
