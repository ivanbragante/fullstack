from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Funcionario, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
funcionario_tag = Tag(name="Funcionario", description="Adição, visualização e remoção de funcionarios à base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário à um funcionarios cadastrado na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/funcionario', tags=[funcionario_tag],
          responses={"200": FuncionarioViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_funcionario(form: FuncionarioSchema):
    """Adiciona um novo Funcionario à base de dados

    Retorna uma representação dos funcionarios e comentários associados.
    """
    funcionario = Funcionario(
        nome=form.nome,
        quantidade=form.quantidade,
        valor=form.valor)
    logger.debug(f"Adicionando funcionario de nome: '{funcionario.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando funcionario
        session.add(funcionario)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado funcionario de nome: '{funcionario.nome}'")
        return apresenta_funcionario(funcionario), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Funcionario de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar funcionario '{funcionario.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar funcionario '{funcionario.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/funcionarios', tags=[funcionario_tag],
         responses={"200": ListagemFuncionariosSchema, "404": ErrorSchema})
def get_funcionarios():
    """Faz a busca por todos os Funcionario cadastrados

    Retorna uma representação da listagem de funcionarios.
    """
    logger.debug(f"Coletando funcionarios ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    funcionarios = session.query(Funcionario).all()

    if not funcionarios:
        # se não há funcionarios cadastrados
        return {"funcionarios": []}, 200
    else:
        logger.debug(f"%d rodutos econtrados" % len(funcionarios))
        # retorna a representação de funcionario
        print(funcionarios)
        return apresenta_funcionarios(funcionarios), 200


@app.get('/funcionario', tags=[funcionario_tag],
         responses={"200": FuncionarioViewSchema, "404": ErrorSchema})
def get_funcionario(query: FuncionarioBuscaSchema):
    """Faz a busca por um Funcionario a partir do id do funcionario

    Retorna uma representação dos funcionarios e comentários associados.
    """
    funcionario_nome = query.nome
    logger.debug(f"Coletando dados sobre funcionario #{funcionario_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    funcionario = session.query(Funcionario).filter(Funcionario.nome == funcionario_nome).first()

    if not funcionario:
        # se o funcionario não foi encontrado
        error_msg = "Funcionario não encontrado na base :/"
        logger.warning(f"Erro ao buscar funcionario '{funcionario_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Funcionario econtrado: '{funcionario.nome}'")
        # retorna a representação de funcionario
        return apresenta_funcionario(funcionario), 200


@app.delete('/funcionario', tags=[funcionario_tag],
            responses={"200": FuncionarioDelSchema, "404": ErrorSchema})
def del_funcionario(query: FuncionarioBuscaSchema):
    """Deleta um Funcionario a partir do nome de funcionario informado

    Retorna uma mensagem de confirmação da remoção.
    """
    funcionario_nome = unquote(unquote(query.nome))
    print(funcionario_nome)
    logger.debug(f"Deletando dados sobre funcionario #{funcionario_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Funcionario).filter(Funcionario.nome == funcionario_nome).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado funcionario #{funcionario_nome}")
        return {"mesage": "Funcionario removido", "id": funcionario_nome}
    else:
        # se o funcionario não foi encontrado
        error_msg = "Funcionario não encontrado na base :/"
        logger.warning(f"Erro ao deletar funcionario #'{funcionario_nome}', {error_msg}")
        return {"mesage": error_msg}, 404


@app.post('/cometario', tags=[comentario_tag],
          responses={"200": FuncionarioViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adiciona de um novo comentário à um funcionarios cadastrado na base identificado pelo id

    Retorna uma representação dos funcionarios e comentários associados.
    """
    funcionario_id  = form.funcionario_id
    logger.debug(f"Adicionando comentários ao funcionario #{funcionario_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca pelo funcionario
    funcionario = session.query(Funcionario).filter(Funcionario.id == funcionario_id).first()

    if not funcionario:
        # se funcionario não encontrado
        error_msg = "Funcionario não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao funcionario '{funcionario_id}', {error_msg}")
        return {"mesage": error_msg}, 404

    # criando o comentário
    texto = form.texto
    comentario = Comentario(texto)

    # adicionando o comentário ao funcionario
    funcionario.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao funcionario #{funcionario_id}")

    # retorna a representação de funcionario
    return apresenta_funcionario(funcionario), 200
