import mysql.connector  # Importa a biblioteca mysql.connector para conectar e interagir com o banco de dados MySQL.
from mysql.connector import Error  # Importa a classe Error para tratar exceções relacionadas ao MySQL.

# Define a classe db_connector para gerenciar a conexão e operações com o banco de dados MySQL.
class db_connector:
        def connect(self):
                # Conecta ao banco de dados MySQL usando as credenciais fornecidas.
                self.connection = mysql.connector.connect(
                        host='localhost',
                        database='banco_clientes',
                        user='root',
                        password='root')
                
                # Verifica se a conexão foi bem-sucedida.
                if self.connection.is_connected():
                        print("Conectado ao MySQL Server")
                        # Cria um cursor com buffer para executar comandos SQL.
                        self.cursor = self.connection.cursor(buffered=True)
                        
        def disconnect(self):
                # Confirma as alterações no banco de dados e fecha a conexão.
                self.connection.commit()
                self.cursor.close()
                self.connection.close()                        
                        
        def __init__(self):
                # Método construtor que é executado ao criar uma instância da classe.
                self.connect()  # Conecta ao banco de dados.
                
                # Apaga a tabela 'users' se ela já existir.
                self.cursor.execute('''DROP TABLE IF EXISTS users;''')   

                # Cria a tabela 'users' com uma coluna 'id' auto-incrementável e 'name' com valores únicos.
                self.cursor.execute('''CREATE TABLE users (
                        id int AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255) UNIQUE NOT NULL)''')        
                
                self.disconnect()  # Desconecta do banco de dados após criar a tabela.
        
        def __del__(self):
                # Método destrutor que é executado quando a instância da classe é destruída.
                self.connection.close()  # Fecha a conexão com o banco de dados.
                self.cursor.close()  # Fecha o cursor.

        def add_user(self, username):
                # Método para adicionar um usuário ao banco de dados.
                self.connect()  # Conecta ao banco de dados.

                # Consulta para verificar se o nome de usuário já existe na tabela 'users'.
                comando = "SELECT count(*) from users WHERE name = (%s); "
                self.cursor.execute(comando, [username])
                qtd_users = self.cursor.fetchone()[0]  # Obtém o resultado da consulta.
                
                # Se o nome já existir, o método retorna sem adicionar o usuário.
                if (qtd_users != 0):
                         return
                
                # Se o nome não existir, insere o novo usuário na tabela 'users'.
                comando = "INSERT INTO users (name) VALUES (%s);"
                print(comando)

                print("Adicionando na tabela")
                self.cursor.execute(comando, [username])
                
                self.disconnect()  # Desconecta do banco de dados após a operação.