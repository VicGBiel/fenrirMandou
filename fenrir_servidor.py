from concurrent import futures
import uuid
import os
from google.protobuf import json_format

import grpc
import fenrir_pb2
import fenrir_pb2_grpc

DB_DIR = "tarefas_db"

class GerenciadorTarefasServicer(fenrir_pb2_grpc.GerenciadorTarefasServicer):

    def Criar(self, request, context): 
        print("Requisição 'Criar' recebida!")

        novo_id = str(uuid.uuid4()) # Cria o novo ID da tarefa com UUID

        nova_tarefa = fenrir_pb2.Tarefa( # Cria o objeto tarefa
            id = novo_id,
            titulo = request.titulo,
            descricao = request.descricao,
            status = fenrir_pb2.Status_Tarefa.PENDENTE,
            data = request.data,
            responsavel = request.responsavel
        )

        # Converte a mensagem gRPC para JSON
        tarefa_json = json_format.MessageToJson(nova_tarefa) 
        filepath = os.path.join(DB_DIR, f"{novo_id}.json")

        with open(filepath, 'w') as f:
            f.write(tarefa_json)

        return nova_tarefa
    
    def Listar(self, request, context):
        print("Requisição 'Listar' recebida!")

        lista_tarefas = []

        for filename in os.listdir(DB_DIR):
            if filename.endswith(".json"):
                filepath = os.path.join(DB_DIR, filename)
                    
                # Lê o conteúdo JSON do arquivo
                with open(filepath, 'r') as f:
                    tarefa_json = f.read()
                        
                    # Cria um objeto Tarefa vazio
                    tarefa = fenrir_pb2.Tarefa()
                   
                    # Converte o JSON de volta para o objeto gRPC
                    json_format.Parse(tarefa_json, tarefa)
                        
                    # Adiciona na lista
                    lista_tarefas.append(tarefa)

        return fenrir_pb2.ListarResponse(tarefas = lista_tarefas)
    
    def Atualizar(self, request, context):
        print("Requisição 'Atualizar' recebida!")

        tarefa_id = request.id

        filepath = os.path.join(DB_DIR, f"{tarefa_id}.json")

        tarefa_json = json_format.MessageToJson(request)

        # Sobreescreve a tarefa selecionada
        with open(filepath, 'w') as f:
            f.write(tarefa_json)

        return fenrir_pb2.Tarefa()
    
    def Deletar(self, request, context):
        print("Requisição 'Deletar' recebida!")

        tarefa_id = request.id
        filepath = os.path.join(DB_DIR, f"{tarefa_id}.json")

        os.remove(filepath)

        return fenrir_pb2.DeletarResponse(mensagem = "Tarefa deletada com sucesso!")


def serve():
    if not os.path.exists(DB_DIR): # Cria o diretório, caso ainda nao exista 
        os.makedirs(DB_DIR)

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    fenrir_pb2_grpc.add_GerenciadorTarefasServicer_to_server(
        GerenciadorTarefasServicer(), server
    )
    print("Iniciando servidor na porta 50051")
    server.add_insecure_port('0.0.0.0:50051')
    server.start()
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        print("Parando o servidor...")
        server.stop(0)


if __name__ == "__main__":
    serve()