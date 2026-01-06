package com.sd.servico_agendamento.repository;

import com.sd.servico_agendamento.model.Consulta;
import com.sd.servico_agendamento.model.StatusConsulta;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface ConsultaRepository extends JpaRepository<Consulta, Long> {
    List<Consulta> findByPacienteId(Long pacienteId);
    List<Consulta> findByMedicoId(Long medicoId);
    List<Consulta> findByStatus(StatusConsulta status);

    @org.springframework.data.jpa.repository.Query("SELECT COUNT(c) > 0 FROM Consulta c JOIN c.horario h " +
           "WHERE c.medicoId = :medicoId " +
           "AND c.status <> 'CANCELADA' " +
           "AND h.dataHora > :start " +
           "AND h.dataHora < :end")
    boolean existsOverlapping(@org.springframework.data.repository.query.Param("medicoId") Long medicoId, 
                             @org.springframework.data.repository.query.Param("start") java.time.LocalDateTime start, 
                             @org.springframework.data.repository.query.Param("end") java.time.LocalDateTime end);
}
