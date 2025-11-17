import grpc
import argparse

import fenrir_pb2
import fenrir_pb2_grpc

def run(args):
    address = f'{args.ip}:{args.port}'
    print(f"Conectando em {address}")

    with grpc.insecure_channel(address) as channel:

        stub = fenrir_pb2_grpc.GerenciadorTarefasStub(channel)
        
        if args.command == "criar":
            print(f"Criando a tarefa!")
            nova_tarefa = stub.Criar(fenrir_pb2.CriarRequest(
                titulo = args.titulo,
                descricao = args.descricao,
                data = args.data,
                responsavel = args.responsavel
            ))
            print(f"Tarefa criada com sucesso!")

        elif args.command == "listar":
            print("Listando tarefas atuais...\n")
            
            resposta_lista = stub.Listar(fenrir_pb2.ListarRequest())
            
            for tarefa in resposta_lista.tarefas:
                status_str = fenrir_pb2.Status_Tarefa.Name(tarefa.status)
                print(f"- ID: {tarefa.id}\n")
                print(f"  Título: {tarefa.titulo}\n")
                print(f"  Descrição: {tarefa.descricao}\n")
                print(f"  Status: {status_str}\n")
                print(f"  Data-limite: {tarefa.data}\n")
                print(f"  Responsável: {tarefa.responsavel}\n\n")
                
        elif args.command == "atualizar":
                print(f"Atualizando a tarefa: {args.id}\n")
                # Para atualizar, primeiro buscamos a tarefa
                tarefa_obj = None
                resposta_lista = stub.Listar(fenrir_pb2.ListarRequest())
                for t in resposta_lista.tarefas:
                    if t.id == args.id:
                        tarefa_obj = t
                        break
                
                if not tarefa_obj:
                    print(f"Erro: Tarefa com ID {args.id} não encontrada.")
                    return

                tarefa_obj.titulo = args.titulo if args.titulo is not None else tarefa_obj.titulo
                tarefa_obj.descricao = args.descricao if args.descricao is not None else tarefa_obj.descricao
                tarefa_obj.data = args.data if args.data is not None else tarefa_obj.data

                # Por ser uma repeated string, não é possivel apenas trocar a lista de responsáveis
                # A antiga lista deve ser apagada e os novos elementos adicionados
                if args.responsavel:
                    del tarefa_obj.responsavel[:] 
                    tarefa_obj.responsavel.extend(args.responsavel)
                
                # Atualiza o status (convertendo string para o enum)
                if args.status:
                    if args.status.upper() in fenrir_pb2.Status_Tarefa.keys():
                        tarefa_obj.status = fenrir_pb2.Status_Tarefa.Value(args.status.upper())
                    else:
                        print("Status inválido! Use PENDENTE, EM_ANDAMENTO ou CONCLUIDA")
                        return
                    
                resposta_att = stub.Atualizar(tarefa_obj)
                print(f"Tarefa atualizada com sucesso!\n")
            
            
        elif args.command == "deletar":
            print(f"Deletando a tarefa: {args.id}\n")
            resposta_delete = stub.Deletar(fenrir_pb2.DeletarRequest(id=args.id))
            print(f"Mensagem do servidor: '{resposta_delete.mensagem}'\n")
             

if __name__ == '__main__':
    # Parser principal
    parser = argparse.ArgumentParser(description = 'FenrirMandou: Cliente gRPC para Gerenciador de Tarefas')
    parser.add_argument('--ip', type = str, default = 'localhost', help = 'IP do servidor')
    parser.add_argument('--port', type = str, default = '50051', help = 'Porta do servidor')

    # Sub-parsers para os comandos 
    subparsers = parser.add_subparsers(dest = 'command', required = True)

    # Comando 'criar'
    parser_criar = subparsers.add_parser('criar', help = 'Cria uma nova tarefa')
    parser_criar.add_argument('--titulo', type = str, required = True, help='Título da tarefa')
    parser_criar.add_argument('--descricao', type = str, default = "", help='Descrição da tarefa')
    parser_criar.add_argument('--data', type = str, default = "", help = 'Data limite')
    parser_criar.add_argument('--responsavel', type = str, nargs = '+', default = [], help='Lista de responsáveis (ex: --responsavel Ana Bruno)')

    # Comando 'listar'
    subparsers.add_parser('listar', help = 'Lista todas as tarefas')

    # Comando 'atualizar'
    parser_atualizar = subparsers.add_parser('atualizar', help = 'Atualiza uma tarefa existente')
    parser_atualizar.add_argument('--id', type = str, required = True, help = 'ID da tarefa a ser atualizada')
    parser_atualizar.add_argument('--titulo', type = str, help = 'Novo título')
    parser_atualizar.add_argument('--descricao', type = str, help = 'Nova descrição')
    parser_atualizar.add_argument('--status', type = str, help = 'Novo status (PENDENTE, EM_ANDAMENTO, CONCLUIDA)')
    parser_atualizar.add_argument('--data', type = str, default = None, help = 'Nova data limite')
    parser_atualizar.add_argument('--responsavel', type = str, nargs = '+', default = [], help = 'Novo responsável')
    
    # Comando 'deletar'
    parser_deletar = subparsers.add_parser('deletar', help = 'Deleta uma tarefa.')
    parser_deletar.add_argument('--id', type = str, required = True, help = 'ID da tarefa a ser deletada')

    args = parser.parse_args()
    run(args)