# Define uma classe chamada 'user'.
class user:
    # Método construtor que é chamado automaticamente ao criar uma instância da classe.
    def __init__(self, nome):
        self.nome = nome  # Atribui o valor passado como argumento 'nome' ao atributo da instância 'nome'.
        print(nome)  # Exibe o nome no console para fins de verificação.
