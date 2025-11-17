# FenrirMandou - Gerenciador de Tarefas com gRPC

Este projeto é uma atividade prática para a disciplina de Sistemas Distribuídos I, que implementa um sistema de gerenciamento de tarefas no modelo cliente-servidor. A comunicação entre o cliente e o servidor é feita inteiramente com gRPC, e a estrutura dos dados é definida com Protocol Buffers.

## Funcionalidades

O servidor gRPC (em `fenrir_servidor.py`) expõe 4 métodos que o cliente pode consumir:

* Criar: Adiciona uma nova tarefa ao sistema.
* Listar: Retorna todas as tarefas existentes.
* Atualizar: Modifica uma tarefa existente.
* Deletar: Remove uma tarefa pelo seu ID.

## Conceitos Teóricos

Esta seção explica a "arquitetura" do projeto, focando em por que o gRPC e o Protocol Buffers foram usados.

### 1. Protocol Buffers

A parte principal do gRPC é o arquivo `.proto`, que define quais são as estruturas de dados e quais são os "endpoints" do serviço.

O arquivo `fenrir.proto` define:

1.  As Mensagens: Como o objeto `Tarefa` é estruturado.
2.  O Enum: Para garantir que o `status` só possa ter valores válidos.
3.  O Serviço: Quais funções o servidor expõe.


```proto
// Arquivo: fenrir.proto

syntax = "proto3";

package fenrirMandou;

// O serviço
service GerenciadorTarefas{
    rpc Criar(CriarRequest) returns (Tarefa) {}
    rpc Listar(ListarRequest) returns (ListarResponse) {}
    rpc Atualizar(Tarefa) returns (Tarefa) {}
    rpc Deletar(DeletarRequest) returns (DeletarResponse) {}
}

// A estrutura de dados central
message Tarefa{
    string id = 1;
    string titulo = 2;
    string descricao = 3;
    Status_Tarefa status = 4;
    string data = 5;
    repeated string responsavel = 6;
}

// Um enum para travar os tipos de status
enum Status_Tarefa {
  PENDENTE = 0;
  EM_ANDAMENTO = 1;
  CONCLUIDA = 2;
}

// Mensagens específicas para cada "endpoint"
message CriarRequest{
    string titulo = 1;
    string descricao = 2;
    string data = 3;
    repeated string responsavel = 4;
}
// ... (outras mensagens como ListarResponse, DeletarRequest, etc.)
```


### 2. Vantagens do gRPC

O gRPC usa Protocol Buffers para serialização, que basicamente, converte um objeto em memória em um fluxo de bytes para ser enviado pela rede. Sendo assim, o gRPC se torna mais eficiente que as abordagens mais comuns (como APIs REST com JSON).Dessa forma, o gRPC se torna ideal para comunicação interna de microsserviços, onde se é priorizado a performance e confiabilidade.

## Como Executar

### Comandos para o `fenrir_cliente.py`:

* *--ip*: endereço ip do servidor. Padrão: localhost. 
* *--port*: porta do servidor. Padrão 50051.
* *--criar*: cria uma nova tarefa, podendo receber os subcomandos:
    ** *--titulo*: titulo da tarefa;
    ** *--descricao*: descricao da tarefa;
    ** *--data*: data da tarefa;
    ** *--responsavel*: responsavel (ou responsáveis) da tarefa;
    ** Obs.: O ID é gerado automaticamente e o status é automanticamente "PENDENTE".
* *--listar*: lista todas as tarefas.
* *--atualizar*: atualiza as informações da tarefas. Subcomandos:
    ** *--id*: ID para localizar a tarefa;
    ** *--status*: status da tarefas. Só podem ser: "PENDENTE", "EM_ANDAMENTO" e "FINALIZADO";
    ** Todos os subcomandos de *--criar*.
* *--deletar*: deleta a tarefa a partir do ID. Subcomando:
    ** *--id*: ID para localizar a tarefa;

Obs.: Em caso de dúvida, também pode ser utilizado o helper "-h" ou "-help" na linha de comando.

Existem duas formas de executar este projeto:

### Pré-requisitos 

1.  Clone este repositório.

### Opção 1: Executando com Docker

Este método simula 3 máquinas (1 servidor, 2 clientes) usando contêineres.

**Pré-requisitos:**
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) instalado e rodando.

**Passos:**

1.  **Construa as Imagens:**
    No terminal, na raiz do projeto, rode:
    ```bash
    docker-compose build
    ```

2.  **Inicie os Contêineres:**
    Isso iniciará o servidor e os dois clientes em "background" (`-d`).
    ```bash
    docker-compose up -d
    ```

3.  **Demonstração (Abrir 2 Terminais):**
    Agora, você pode "entrar" nos contêineres dos clientes para enviar comandos ao servidor.

    * **No Terminal 1 (Cliente 1):**
        ```bash
        # O Cliente 1 cria uma tarefa
        docker-compose exec cliente1 python fenrir_cliente.py --ip servidor criar --titulo "Tarefa do Cliente 1" --responsavel "Ana"
        ```

    * **No Terminal 2 (Cliente 2):**
        ```bash
        # O Cliente 2 lista as tarefas
        docker-compose exec cliente2 python fenrir_cliente.py --ip servidor listar
        ```

    *Note: Foi utilizado `--ip servidor` porque o Docker Compose faz o hostname `servidor` apontar para o IP correto do contêiner do servidor.*

4.  **Para Parar Tudo:**
    Quando terminar, rode:
    ```bash
    docker-compose down
    ```

---

### Opção 2: Executando em Duas Máquinas (Rede Local)

Este método usa dois computadores físicos na mesma rede Wi-Fi.

**Pré-requisitos:**
* Ambas as máquinas na mesma rede Wi-Fi.
* Python e as bibliotecas (`grpcio`, `protobuf`) instalados em ambas.

#### 1. Na Máquina Servidor

1.  **Abra o Firewall:**
    Você precisa permitir que outras máquinas na rede se conectem à porta `50051`.
    * No Windows, vá em "Firewall do Windows Defender" > "Regras de Entrada" > "Nova Regra..."
    * Crie uma regra para a **Porta**, tipo **TCP**, porta específica **50051**, e **Permitir a conexão**.

2.  **Encontre seu IP Local:**
    * Abra o CMD e digite `ipconfig`.
    * Anote o seu "Endereço IPv4" (ex: `192.168.1.10`).

3.  **Execute o Servidor:**
    ```bash
    python fenrir_servidor.py
    ```

#### 2. Na Máquina Cliente 

1.  Abra o terminal e use os comandos do `fenrir_cliente.py` e use o **IP do servidor** que você anotou.

    ```bash
    # Ex: se o IP do servidor for 192.168.1.10

    # Listando
    python fenrir_cliente.py --ip 192.168.1.10 listar

    # Criando
    python fenrir_cliente.py --ip 192.168.1.10 criar --titulo "Tarefa criada pela rede!"
    ```
    Você verá a mensagem "Requisição 'Criar' recebida!" aparecer no terminal do servidor (PC).

## Autor

Victor Gabriel G. Lopes
