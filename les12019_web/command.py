"""Módulo command - contém a AbstractCommand com as classes concretas de command
"""
import abc
from les12019_core.fachada import Fachada
from les12019_core.aplicacao import Resultado



class AbstractCommand(abc.ABC):

    def __init__(self):
        self.fachada = Fachada()

    @abc.abstractmethod
    def execute(self, entidade) -> Resultado:
        """Recebe uma entidade como parâmetro e passa para o método da Fachada corresponde
        a ação requisistada, retornando um Objeto Resultado como resposta da operação realizada. 
        """


class SalvarCommand(AbstractCommand):

    def execute(self, entidade):
        return self.fachada.salvar(entidade)


class AtualizarCommand(AbstractCommand):

    def execute(self, entidade):
        return self.fachada.atualizar(entidade)


class ConsultarCommand(AbstractCommand):

    def execute(self, entidade):
        return self.fachada.consultar(entidade)


class ListarCommand(AbstractCommand):
    
    def execute(self, entidade):
        return self.fachada.listar(entidade)


class NoneCommand(AbstractCommand):

    def execute(self, entidade):
        listar = ListarCommand()
        return listar.execute(entidade)


class ExcluirCommand(AbstractCommand):

    def execute(self, entidade):
        return self.fachada.excluir(entidade)


class PreOperacaoCommand(AbstractCommand):

    def execute(self, entidade):
        return self.fachada.preOperacao(entidade)


class ConsultarPorIdCommand(AbstractCommand):

    def execute(self, entidade):
        return self.fachada.consultarPorId(entidade)


class ConsultarPorParametro(AbstractCommand):

    def execute(self, entidade):
        return self.fachada.consultarPorParametro(entidade)


class ClonarCommand(AbstractCommand):

    def execute(self, entidade):      
        return self.fachada.clonar(entidade)


class IncluirCommand(AbstractCommand):

    def execute(self, entidade):      
        return self.fachada.incluir(entidade)