# Consulta-Medica-SD
Um projeto para a disciplina de Sistemas Distribuídos da UFC Crateús. Ele é um sistema distribuído para gerenciamento de consultas médicas em clínicas ou hospitais. Possui lado servidor com módulos de usuários, agendamento, notificações e validação de convênios, além de banco de dados, e lado cliente para interação dinâmica e segura.

Prazo para Entregar: 05/01

dockerhub: https://hub.docker.com/u/pablokauantech


usuários: sockets will
	crud de usuarios com campo role para definir o que é,
		{nome, email, senha, regra}
	função de ver se está autenticado, se existe no banco e devolve o user;
	função de mudar a regra do usuário
	transmiti alterações no mosquitto


Agendamento: grpc samuel
	crud horários disponíveis
	crud de agendamento(sempre que criar ou apagar enviar para o pagamentos o id do agendamento que foi apagado)
	transmiti alterações no mosquitto


Pagamento/Validação: api pablo
	crud de pagamentos
	transmite alterações no mosquitto 


Serviço de Notificações: RabbitMQ Rod
	criar serviço mosquitto
	se conectar nos canais de transmissão de cada máquina e toda vez que receber um aviso, vai e envia um email com a mensagem para o email do cliente


scripts python: sthepany
	realizar scripts de controle do sistema
	criar imagem do sistema subi no docker hub
