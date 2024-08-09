import asyncio  # Importa a biblioteca asyncio para a execução de código assíncrono.
from websockets.sync.client import connect  # Importa a função connect para estabelecer uma conexão websocket síncrona.
import websocket  # Importa a biblioteca websocket para facilitar a comunicação em tempo real via websockets.
import json  # Importa a biblioteca json para manipulação de dados em formato JSON.
import user  # Importa o módulo user, possivelmente contendo a definição de uma classe ou funções relacionadas ao usuário.
from user import user  # Importa a classe ou função user diretamente do módulo user.
import keyboard  # Importa a biblioteca keyboard para detectar pressionamentos de teclas.
from datetime import datetime  # Importa a classe datetime para manipulação de datas e horas.

# O cliente precisa permanecer "online" para receber a data e hora a cada segundo.
# Criar um booleano para identificar se o cliente está online ou offline.
# Transformar a chave "nome" em uma chave candidata (potencialmente única) no banco de dados.
# O cliente precisa receber de forma isolada o retorno da sequência de Fibonacci se enviar um número como requisição.
# Criar uma condição (if) para verificar se o nome (único) já existe e, caso não exista, criar no banco de dados.

# Função que identifica se a string recebida é uma data e hora no formato esperado.
def is_datetime(message):
    test_str = message  # Inicializa a string a partir da mensagem recebida.
    format = "%Y-%m-%d %H:%M:%S"  # Define o formato esperado da data e hora.

    resultado = True  # Inicializa a variável que armazenará o resultado.

    # Usa try-except para verificar se a string corresponde ao formato esperado.
    try:
        resultado = bool(datetime.strptime(test_str, format))
    except ValueError:
        resultado = False  # Se ocorrer um erro de valor, a string não corresponde ao formato.
    
    return resultado  # Retorna o resultado.

# Função assíncrona que recebe mensagens do websocket.
async def hello(websocket):
    while(True):
        message = websocket.recv()  # Recebe uma mensagem do websocket.
        # Verifica se a mensagem não é uma data ou se a tecla "ctrl" está pressionada.
        if (not is_datetime(message)) or (keyboard.is_pressed("ctrl")):
            print(f"Received: {message}")  # Imprime a mensagem recebida.

# Função que coordena as tarefas assíncronas.
async def gather_handler(websocket):
    with connect("ws://localhost:6687") as websocket:  # Conecta ao websocket na URL especificada.
        await asyncio.gather(
            input_handler(websocket),  # Lida com a entrada do usuário.
            hello(websocket)  # Lida com as mensagens recebidas.
        )

# Função que lida com a entrada do usuário e envia dados pelo websocket.
async def input_handler(websocket):
    print("Para visualizar o Date_Time mantenha pressionado ctrl")
    name = input("Insira seu nome ")  # Solicita o nome do usuário.

    x = user(name)  # Cria um objeto da classe "user" com o nome fornecido.
    y = json.dumps(x.__dict__)  # Converte o objeto em uma string JSON.
    print(y)  # Imprime a representação JSON do objeto.

    websocket.send(x.nome)  # Envia o nome do usuário pelo websocket.
    escrita = " "
    while(escrita != "x"):
        escrita = input()  # Continuamente solicita entrada do usuário.
        if escrita == "x":
            continue  # Se o usuário digitar "x", o loop continua sem enviar a mensagem.
        websocket.send(escrita)  # Envia a entrada do usuário pelo websocket.

# Função principal que inicia a execução do programa.
async def main():
    await gather_handler(websocket)  # Inicia o gerenciamento de tarefas assíncronas.
    # await asyncio.Future()  # Código comentado que, se ativado, faria o programa rodar indefinidamente.

# Inicia a execução do programa.
asyncio.run(main())
