<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Payload;
use App\Services\RabbitMQService;
use Illuminate\Support\Facades\Http;

class PayloadController extends Controller
{
    public function pay($id, RabbitMQService $rabbitMQ)
    {
        $payload = Payload::findOrFail($id);

        if ($payload->status === 'paid') {
            return response()->json([
                'message' => 'Pagamento já realizado'
            ], 400);
        }

        $payload->update([
            'status' => 'paid'
        ]);

        $rabbitMQ->publishToExchange(
            'notificacoes_exchange',
            'sd/notificacoes',
            [
                'email' => $payload->customer_email,
                'assunto' => 'Confirmação de Pagamento',
                'mensagem' => "Seu pagamento de R$ {$payload->total} foi realizado com sucesso."
            ]
        );

        $response = Http::withQueryParameters([
            'status' => 'AGENDADA'
        ])->put(
            "http://agendamento:8080/api/agendamentos/{$payload->agendamento_id}/status"
        );

        return response()->json([
            'message' => 'Pagamento realizado com sucesso',
            'payload' => $payload
        ]);
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(Request $request, RabbitMQService $rabbitMQ)
    {
        $validated = $request->validate([
            'agendamento_id' => 'required|integer',
            'total' => 'required|numeric',
            'payment_method' => 'required|string',
            'customer_email' => 'required|email',
        ]);

        $payload = Payload::create([
            'agendamento_id' => $validated['agendamento_id'],
            'total' => $validated['total'],
            'payment_method' => $validated['payment_method'],
            'customer_email' => $validated['customer_email'],
            'status' => 'pending',
        ]);

        $rabbitMQ->publishToExchange(
            'notificacoes_exchange',
            'sd/notificacoes',
            [
                'email' => $payload->customer_email,
                'assunto' => 'Pagamento em Aberto',
                'mensagem' => "Seu pagamento de R$ {$payload->total} foi criado e está pendente."
            ]
        );

        return response()->json($payload, 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(string $id)
    {
        $payload = Payload::findOrFail($id);
        return response()->json($payload);
    }


    /**
     * Update the specified resource in storage.
     */
    public function update(Request $request, string $id, RabbitMQService $rabbitMQ)
    {
        $payload = Payload::findOrFail($id);

        $validated = $request->validate([
            'agendamento_id' => 'sometimes|integer',
            'total' => 'sometimes|numeric',
            'status' => 'sometimes|string',
            'payment_method' => 'sometimes|string',
            'customer_email' => 'sometimes|email',
        ]);

        $payload->update($validated);

        $rabbitMQ->publishToExchange(
            'notificacoes_exchange',
            'sd/notificacoes',
            [
                'email' => $payload->customer_email,
                'assunto' => 'Alteração no Pagamento',
                'mensagem' => "Houve uma alteração no seu pagamento."
            ]
        );

        return response()->json($payload);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(string $id, RabbitMQService $rabbitMQ)
    {
        $payload = Payload::findOrFail($id);
        $payload->delete();

        $rabbitMQ->publishToExchange(
            'notificacoes_exchange',
            'sd/notificacoes',
            [
                'email' => $payload->customer_email,
                'assunto' => 'Cancelamento do Pagamento',
                'mensagem' => "Seu pagamento foi cancelado com sucesso."
            ]
        );

        $response = Http::withQueryParameters([
            'status' => 'CANCELADA'
        ])->put(
            "http://agendamento:8080/api/agendamentos/{$payload->agendamento_id}/status"
        );

        return response()->json(null, 204);
    }
}
