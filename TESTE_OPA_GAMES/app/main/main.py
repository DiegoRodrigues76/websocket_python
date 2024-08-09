# Importa a classe db_server do módulo server que está localizado no pacote db.
from database.server import db_server

# Cria uma instância da classe db_server, passando 6687 como a porta em que o servidor irá rodar.
x = db_server(3306)

# Chama o método run_server da instância x para iniciar o servidor.
x.run_server()
