from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union


class Funcionario(Base):
    __tablename__ = 'funcionario'

    id = Column("pk_funcionario", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    venda = Column(Float)
    porcentagem = Column(Integer)
    comissao = Column(Float)


    def __init__(self, nome:str, porcentagem:int, venda:float, comissao:float):
        """
        Cria um Funcionario

        Arguments:
            nome: nome do funcionario.
            porcentagem: porcentagem que se espera comprar daquele funcionario
            venda: venda esperado para o funcionario
            data_insercao: data de quando o funcionario foi inserido à base
        """
        self.nome = nome
        self.porcentagem = porcentagem
        self.venda = venda
        self.comissao = comissao

