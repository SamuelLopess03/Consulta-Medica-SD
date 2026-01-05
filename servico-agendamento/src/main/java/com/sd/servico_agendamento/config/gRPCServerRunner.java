package com.sd.servico_agendamento.config;

import com.sd.servico_agendamento.grpc.AgendamentoGrpcService;
import io.grpc.Server;
import io.grpc.ServerBuilder;
import jakarta.annotation.PostConstruct;
import jakarta.annotation.PreDestroy;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
@RequiredArgsConstructor
@Slf4j
public class gRPCServerRunner {

    private final AgendamentoGrpcService agendamentoGrpcService;

    @Value("${spring.grpc.server.port:9090}")
    private int port;

    private Server server;

    @PostConstruct
    public void start() throws IOException {
        this.server = ServerBuilder.forPort(port)
                .addService(agendamentoGrpcService)
                .build()
                .start();
        log.info("Servidor gRPC iniciado na porta: {}", port);
    }

    @PreDestroy
    public void stop() {
        if (server != null) {
            server.shutdown();
        }
    }
}
