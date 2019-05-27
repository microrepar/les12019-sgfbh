"""Módulo contendo a classe DAO Abstrata e as classes concretas
"""

import abc
from app import db
from sqlalchemy import and_

from typing import List
from les12019_dominio.abstract_models import EntidadeDominio

list_entidade = List[EntidadeDominio]


class AbstractDAO(abc.ABC):

    @abc.abstractmethod
    def salvar(self, entidade):
        """Recebe uma entidade como parâmetro para persistir no banco de dados
        """
        db.session.add(entidade)
        db.session.commit()
        return entidade

    @abc.abstractmethod
    def listar(self, entidade) -> list_entidade:
        """Recebe uma entidade como Parametro para ser listado todas as instancias salvas no banco de dados
        """
        _repositorio = entidade.__class__
        entidades = _repositorio.query.order_by(_repositorio.id.asc()).all()
        return entidades
       
    @abc.abstractmethod
    def alterar(self, entidade):
        """Recebe a entidade que será alterada no banco de dados
        """
    
    @abc.abstractmethod
    def consultar(self, entidade) -> list_entidade:
        """Recebe uma entidade como parâmetro para ser buscado no banco de dados
        """

    @abc.abstractmethod
    def consultarPorId(self, entidade):
        """Recebe uma entidade como parâmetro para ser buscado no banco de dados
        """
        _repositorio = entidade.__class__
        _entidade = _repositorio.query.filter(_repositorio.id==entidade.id).first()
        return _entidade
        
    
    @abc.abstractmethod
    def consultarPorParametro(self, entidade) -> list_entidade:
        """Recebe uma entidade como parâmetro para ser buscado no banco de dados
        """

    @abc.abstractmethod
    def excluir(self, entidade):
        """Recebe um entidade como parâmetro para que ser excluido.
        """
        _repositorio = entidade.__class__
        _entidade = _repositorio.query.filter_by(id=entidade.id).first()
        try:
            db.session.delete(_entidade)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return False
        else:
            return True




########################### Classe Concreta - DAO de Base para implementar##################################
class _DAO(AbstractDAO):

    def salvar(self, entidade):
        pass

    def listar(self, entidade):
        pass

    def alterar(self, entidade):
        pass

    def consultarPorId(self, entidade):
        pass

    def consultarPorParametro(self, entidade):
        pass

    def consultar(self, entidade):
        pass

    def excluir(self, entidade):
        pass
