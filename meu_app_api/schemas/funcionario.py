from pydantic import BaseModel
from typing import Optional, List
from model.funcionario import Funcionario

from schemas import ComentarioSchema


class FuncionarioSchema(BaseModel):
    """ Define como um novo funcionario a ser inserido deve ser representado
    """
    nome: str = "Banana Prata"
    quantidade: Optional[int] = 12
    valor: float = 12.50


class FuncionarioBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do funcionario.
    """
    nome: str = "Teste"


class ListagemFuncionariosSchema(BaseModel):
    """ Define como uma listagem de funcionarios será retornada.
    """
    funcionarios:List[FuncionarioSchema]


def apresenta_funcionarios(funcionarios: List[Funcionario]):
    """ Retorna uma representação do funcionario seguindo o schema definido em
        FuncionarioViewSchema.
    """
    result = []
    for funcionario in funcionarios:
        result.append({
            "nome": funcionario.nome,
            "quantidade": funcionario.quantidade,
            "valor": funcionario.valor,
        })

    return {"funcionarios": result}


class FuncionarioViewSchema(BaseModel):
    """ Define como um funcionario será retornado: funcionario + comentários.
    """
    id: int = 1
    nome: str = "Banana Prata"
    quantidade: Optional[int] = 12
    valor: float = 12.50
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class FuncionarioDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    nome: str

def apresenta_funcionario(funcionario: Funcionario):
    """ Retorna uma representação do funcionario seguindo o schema definido em
        FuncionarioViewSchema.
    """
    return {
        "id": funcionario.id,
        "nome": funcionario.nome,
        "quantidade": funcionario.quantidade,
        "valor": funcionario.valor,
        "total_cometarios": len(funcionario.comentarios),
        "comentarios": [{"texto": c.texto} for c in funcionario.comentarios]
    }
