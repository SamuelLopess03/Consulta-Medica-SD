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
}
