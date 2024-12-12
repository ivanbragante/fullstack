from pydantic import BaseModel
from typing import Optional, List
from model.funcionario import Funcionario

# from schemas import ComentarioSchema


class FuncionarioSchema(BaseModel):
    """ Define como um novo funcionario a ser inserido deve ser representado
    """
    nome: str = "Fulano de tal"
    porcentagem: Optional[int] = 10
    venda: float = 10000.5
    comissao: float = 1000.05


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
            "porcentagem": funcionario.porcentagem,
            "venda": funcionario.venda,
            "comissao": funcionario.comissao,
        })

    return {"funcionarios": result}


class FuncionarioViewSchema(BaseModel):
    """ Define como um funcionario será retornado: funcionario.
    """
    id: int = 1
    nome: str = "Banana Prata"
    porcentagem: Optional[int] = 10
    venda: float = 10000.5
    comissao: float = 1000.05
    
    # comentarios:List[ComentarioSchema]


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
        "porcentagem": funcionario.porcentagem,
        "venda": funcionario.venda,
        "comissao": funcionario.comissao
    
    }
