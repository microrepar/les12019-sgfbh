"""Módulo com classes strategy para aplicação de regra de negócio
"""
import abc


######################################## Classe Abstrata de Strategy ########################################
class AbstractStrategy(abc.ABC):

    @abc.abstractmethod
    def processar(self, entidade) -> str:
        """Aplica as regras de negócio com base na entidade passada por parâmetro e 
        retorna uma mensagem de erro se a regra não for atendida.
        """


##################################### Classe Concreta base para implementar##################################
class _Strategy(AbstractStrategy):
    def processar(self, entidade):
        pass
