package com.sd.servico_agendamento.service;

import com.sd.servico_agendamento.client.PagamentoClient;
import com.sd.servico_agendamento.dto.PagamentoRequestDTO;
import com.sd.servico_agendamento.messaging.NotificationProducer;
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
    private final NotificationProducer notificationProducer;
    private final PagamentoClient pagamentoClient;
    private static final DateTimeFormatter formatter = DateTimeFormatter.ISO_LOCAL_DATE_TIME;
    private static final int DURACAO_CONSULTA_MINUTOS = 60;

    @Transactional
    public Consulta agendar(Long pacienteId, String pacienteEmail, Long medicoId, String medicoEmail,
            String especialidade, String dataHoraStr) {
        LocalDateTime dataHora = LocalDateTime.parse(dataHoraStr, formatter);

        // Validação de Sobreposição: Não permitir consultas no intervalo da duração
        LocalDateTime inicioIntervalo = dataHora.minusMinutes(DURACAO_CONSULTA_MINUTOS - 1);
        LocalDateTime fimIntervalo = dataHora.plusMinutes(DURACAO_CONSULTA_MINUTOS - 1);
        
        if (consultaRepository.existsOverlapping(medicoId, inicioIntervalo, fimIntervalo)) {
            throw new RuntimeException("O médico já possui uma consulta agendada em um horário próximo a este.");
        }

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
                .pacienteEmail(pacienteEmail)
                .medicoId(medicoId)
                .especialidade(especialidade)
                .horario(horario)
                .status(StatusConsulta.PENDENTE_VALIDACAO)
                .build();

        horario.setDisponivel(false);
        horarioRepository.save(horario);

        Consulta salva = consultaRepository.save(consulta);

        // Integração RabbitMQ: Notificar Agendamento (Paciente)
        notificationProducer.enviarNotificacao(
                pacienteEmail,
                "Consulta Criada",
                String.format("Olá! Sua consulta de %s foi criada para %s. Para confirmar o agendamento, realize o pagamento via o link/método enviado.", especialidade, dataHoraStr));

        // Integração RabbitMQ: Notificar Agendamento (Médico)
        if (medicoEmail != null && !medicoEmail.isEmpty()) {
            notificationProducer.enviarNotificacao(
                    medicoEmail,
                    "Nova Consulta Criada (Aguardando Pagamento)",
                    String.format("Olá Doutor(a)! Uma nova solicitação de consulta de %s foi criada para %s. O agendamento será confirmado após o pagamento do paciente.", especialidade,
                            dataHoraStr));
        }

        // Integração Pagamentos: Solicitar Pagamento
        pagamentoClient.solicitarPagamento(PagamentoRequestDTO.builder()
                .agendamentoId(salva.getId())
                .total(150.0) // Valor fixo simulado
                .paymentMethod("pix")
                .customerEmail(pacienteEmail)
                .build());

        return salva;
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

        Consulta salva = consultaRepository.save(consulta);

        // Integração RabbitMQ: Notificar Cancelamento
        notificationProducer.enviarNotificacao(
                salva.getPacienteEmail(),
                "Consulta Cancelada",
                String.format("Sua consulta de %s para o dia %s foi cancelada.",
                        salva.getEspecialidade(), salva.getHorario().getDataHora().format(formatter)));

        return salva;
    }

    @Transactional
    public Consulta atualizarStatus(Long id, StatusConsulta novoStatus) {
        Consulta consulta = consultaRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Consulta não encontrada."));

        consulta.setStatus(novoStatus);
        Consulta salva = consultaRepository.save(consulta);

        // Integração RabbitMQ: Notificar Mudança de Status
        notificationProducer.enviarNotificacao(
                salva.getPacienteEmail(),
                "Atualização de Consulta",
                String.format("O status da sua consulta de %s foi atualizado para: %s.",
                        salva.getEspecialidade(), novoStatus));

        return salva;
    }

}
