# Projeto de Teste para Desenvolvedor Backend

Este projeto foi desenvolvido como parte do teste para Desenvolvedor Backend PL. O objetivo do desafio era criar um sistema com conexão via WebSocket, gerenciar clientes conectados, processar comandos específicos e utilizar Docker para o ambiente de desenvolvimento.

## 🛠 Funcionalidades Implementadas

1. **Conexão via WebSocket**
   - Implementação de um servidor WebSocket que permite a conexão de clientes.
   - Desenvolvimento de um client WebSocket simples para teste de conexão.

2. **Envio de Data Atual**
   - O servidor envia a data e hora atuais a cada segundo para todos os clientes conectados.

3. **Gestão de Usuários Conectados**
   - Todos os usuários conectados ao sistema são salvos em um banco de dados.

4. **Processamento de Comandos**
   - O sistema recebe comandos via WebSocket para processar o algoritmo de Fibonacci. O cliente envia um valor `n` e o servidor retorna o resultado de `Fibonacci(n)` exclusivamente para o cliente que fez a solicitação.

## 🚀 Tecnologias Utilizadas

- **Linguagem**: Python 
- **Banco de Dados**: MySQL
- **Programação Assíncrona**: Utilização de bibliotecas/frameworks que suportam operações assíncronas.
- **Docker**: 
  - Utilizado para criar o ambiente de desenvolvimento e execução do sistema.
  - Contém um `Dockerfile` para construir a imagem do sistema.
  - Contém um `docker-compose.yml` para orquestrar múltiplos serviços. 
