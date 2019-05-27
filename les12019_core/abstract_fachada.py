"""Módulo contendo a classe abstractFachada que define a interface para implementação da fachada
"""
import abc
from les12019_core.aplicacao import Resultado


class AbstractFachada(abc.ABC):

    @abc.abstractmethod
    def salvar(self, entidade) -> Resultado:
        """Salva no bando de dados a entidade envia por parâmetro retornando um objeto Resultado.
        """

    @abc.abstractmethod
    def atualizar(self, entidade) -> Resultado:
        """Altera no bando de dados a entidade envia por parâmetro retornando um objeto Resultado.
        """

    @abc.abstractmethod
    def consultar(self, entidade) -> Resultado:
        """Consulta no banco de dados a entidade envia por parâmetro e retorna um Objeto Resultado.
        """
    
    @abc.abstractmethod
    def consultarPorId(self, entidade) -> Resultado:
        """Consulta no banco de dados a entidade envia por parâmetro e retorna um Objeto Resultado.
        """
    
    @abc.abstractmethod
    def consultarPorParametro(self, entidade) -> Resultado:
        """Consulta no banco de dados a entidade envia por parâmetro e retorna um Objeto Resultado.
        """

    @abc.abstractmethod
    def listar(self, entidade) -> Resultado:
        """Lista todos as entidades contidas no banco de dados do mesmo tipo da entidade passada 
        por parâmetro retornando um objeto Resultado.
        """

    @abc.abstractmethod
    def excluir(self, entidade) -> Resultado:
        """Exclui do bando de dados a entidade envia por parâmetro e retorna um objeto Resultado.
        """

