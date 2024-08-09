import asyncio  # Importa a biblioteca asyncio para permitir a execução de código assíncrono.
from websockets.server import serve  # Importa a função serve para criar e iniciar um servidor WebSocket.
from database.connections import db_connector  # Importa a classe db_connector para gerenciar a conexão com o banco de dados.
from datetime import datetime  # Importa a classe datetime para manipulação de datas e horas.
import logging  # Importa a biblioteca logging para registrar mensagens de log.

# Configura o logging para exibir mensagens de nível INFO ou superior.
logging.basicConfig(level=logging.INFO)

# Define a classe db_server que gerencia o servidor WebSocket e as conexões com o banco de dados e os clientes.
class db_server:
    def __init__(self, port):
        """
        Construtor da classe db_server.

        :param port: A porta na qual o servidor WebSocket será executado.
        """
        self.db = db_connector()  # Cria uma instância de db_connector para gerenciar a conexão com o banco de dados.
        self.port = port  # Define a porta em que o servidor WebSocket será executado.
        self.connected = set()  # Cria um conjunto para armazenar os clientes conectados, garantindo que não haja duplicatas.

    def fibonacci_sum_recursive(self, n):
        """
        Calcula o enésimo termo da sequência de Fibonacci de forma iterativa.

        :param n: O termo desejado na sequência de Fibonacci.
        :return: O valor do enésimo termo na sequência.
        """
        if n <= 0:
            return 0  # Se n for 0 ou negativo, retorna 0.
        elif n == 1:
            return 1  # Se n for 1, retorna 1, pois é o primeiro número na sequência de Fibonacci.
        
        # Inicializa os dois primeiros números da sequência de Fibonacci.
        num1, num2 = 0, 1
        
        # Calcula o próximo número na sequência até o enésimo termo.
        for _ in range(2, n + 1):
            num1, num2 = num2, num1 + num2
        
        return num2  # Retorna o enésimo número na sequência.

    async def handler(self, websocket):
        """
        Lida com a conexão WebSocket, gerenciando o envio de horário e o processamento de dados.

        :param websocket: O objeto WebSocket conectado ao cliente.
        """
        await asyncio.gather(
            self.enviar_timer(websocket),  # Inicia o envio periódico de horário ao cliente.
            self.processar_dados(websocket)  # Inicia o processamento das mensagens recebidas do cliente.
        )

    async def registrar_nome(self, websocket, message):
        """
        Registra o nome do usuário no banco de dados e adiciona o WebSocket à lista de clientes conectados.

        :param websocket: O objeto WebSocket conectado ao cliente.
        :param message: O nome do usuário a ser registrado.
        """
        logging.info(f"Registrando nome: {message}")  # Registra o nome do usuário no log.
        self.db.add_user(message)  # Adiciona o nome do usuário ao banco de dados.
        self.connected.add(websocket)  # Adiciona o WebSocket à lista de clientes conectados (se ainda não estiver na lista).

    async def enviar_timer(self, websocket):
        """
        Envia o horário atual para o cliente a cada segundo.

        :param websocket: O objeto WebSocket conectado ao cliente.
        """
        while True:
            # Obtém a hora atual no formato ISO, com separador de espaço entre data e hora.
            hour = datetime.now().isoformat(" ", "seconds")
            await websocket.send(hour)  # Envia a hora atual para o cliente via WebSocket.
            await asyncio.sleep(1)  # Aguarda 1 segundo antes de enviar o próximo horário.

    def processar_fibonacci(self, number):
        """
        Processa o cálculo da sequência de Fibonacci e retorna o resultado como string.

        :param number: O enésimo termo da sequência de Fibonacci a ser calculado.
        :return: O valor do enésimo termo na sequência, convertido para string.
        """
        total = self.fibonacci_sum_recursive(number)  # Calcula o enésimo termo da sequência de Fibonacci.
        return str(total)  # Retorna o resultado como string.
    
    async def processar_dados(self, websocket):
        """
        Processa as mensagens recebidas do cliente WebSocket.

        :param websocket: O objeto WebSocket conectado ao cliente.
        """
        async for message in websocket:
            try:
                # Tenta converter a mensagem recebida em um número inteiro.
                value = int(message)
                total = self.processar_fibonacci(value)  # Calcula o enésimo termo da sequência de Fibonacci.
                await websocket.send(total)  # Envia o resultado de volta ao cliente.
            except ValueError:
                # Se a mensagem não for um número, assume que é o nome do usuário e registra-o.
                await self.registrar_nome(websocket, message)
            except Exception as e:
                # Captura e registra qualquer exceção que ocorra durante o processamento.
                logging.error(f"Erro ao processar dados: {e}")

    async def main(self):
        """
        Função principal que inicia o servidor WebSocket.

        O servidor é iniciado na porta especificada e aguarda indefinidamente novas conexões.
        """
        async with serve(self.handler, "localhost", self.port):    
            await asyncio.Future()  # Mantém o servidor rodando indefinidamente.
             
    def run_server(self):
        """
        Executa a função principal que inicia o servidor WebSocket.
        """
        asyncio.run(self.main())  # Executa a função main para iniciar o servidor.
