from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Status_Tarefa(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PENDENTE: _ClassVar[Status_Tarefa]
    EM_ANDAMENTO: _ClassVar[Status_Tarefa]
    CONCLUIDA: _ClassVar[Status_Tarefa]
PENDENTE: Status_Tarefa
EM_ANDAMENTO: Status_Tarefa
CONCLUIDA: Status_Tarefa

class Tarefa(_message.Message):
    __slots__ = ("id", "titulo", "descricao", "status", "data", "responsavel")
    ID_FIELD_NUMBER: _ClassVar[int]
    TITULO_FIELD_NUMBER: _ClassVar[int]
    DESCRICAO_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    RESPONSAVEL_FIELD_NUMBER: _ClassVar[int]
    id: str
    titulo: str
    descricao: str
    status: Status_Tarefa
    data: str
    responsavel: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, id: _Optional[str] = ..., titulo: _Optional[str] = ..., descricao: _Optional[str] = ..., status: _Optional[_Union[Status_Tarefa, str]] = ..., data: _Optional[str] = ..., responsavel: _Optional[_Iterable[str]] = ...) -> None: ...

class CriarRequest(_message.Message):
    __slots__ = ("titulo", "descricao", "data", "responsavel")
    TITULO_FIELD_NUMBER: _ClassVar[int]
    DESCRICAO_FIELD_NUMBER: _ClassVar[int]
    DATA_FIELD_NUMBER: _ClassVar[int]
    RESPONSAVEL_FIELD_NUMBER: _ClassVar[int]
    titulo: str
    descricao: str
    data: str
    responsavel: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, titulo: _Optional[str] = ..., descricao: _Optional[str] = ..., data: _Optional[str] = ..., responsavel: _Optional[_Iterable[str]] = ...) -> None: ...

class ListarRequest(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class ListarResponse(_message.Message):
    __slots__ = ("tarefas",)
    TAREFAS_FIELD_NUMBER: _ClassVar[int]
    tarefas: _containers.RepeatedCompositeFieldContainer[Tarefa]
    def __init__(self, tarefas: _Optional[_Iterable[_Union[Tarefa, _Mapping]]] = ...) -> None: ...

class DeletarRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class DeletarResponse(_message.Message):
    __slots__ = ("mensagem",)
    MENSAGEM_FIELD_NUMBER: _ClassVar[int]
    mensagem: str
    def __init__(self, mensagem: _Optional[str] = ...) -> None: ...
