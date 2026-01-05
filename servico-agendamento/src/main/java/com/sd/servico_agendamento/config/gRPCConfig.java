package com.sd.servico_agendamento.config;

import com.sd.servico_agendamento.grpc.stubs.AgendamentoServiceGrpc;
import io.grpc.ManagedChannel;
import io.grpc.ManagedChannelBuilder;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class gRPCConfig {

    @Value("${spring.grpc.server.port:9090}")
    private int port;

    @Bean
    public ManagedChannel managedChannel() {
        return ManagedChannelBuilder.forAddress("localhost", port)
                .usePlaintext()
                .build();
    }

    @Bean
    public AgendamentoServiceGrpc.AgendamentoServiceBlockingStub agendamentoServiceBlockingStub(ManagedChannel channel) {
        return AgendamentoServiceGrpc.newBlockingStub(channel);
    }
}
