"""Módulo viewhelper - contém a classe AbstractViewHelper e as classes concretas
"""
import abc
from les12019_core.aplicacao import Resultado
from flask import flash


# Verificador de msg - adiciona a função flash todas as msg e retorna True se houver ao menos uma e False para nenhuma
# Função para verificar se há mensagens de erro e carrega-las na flash função
def _verificar_msg(resultado: Resultado):
    if resultado.qtde_msg() > 0:
        for msg in resultado.msg:
            flash(msg)
        return True
    return False


############################ ViewHelper Abstract ##################################
class AbstractViewHelper(abc.ABC):

    @abc.abstractmethod
    def getEntidade(self, request):
        """Recebe uma requisição e retorna uma instância do objeto com os dados preenchidos
        """

    @abc.abstractmethod
    def setView(self, resultado, request):
        """Recebe o objeto resultado da requisição e prepara para apresentar na view para o cliente
        """


# modelo para implementação das viewhelpers
class _ViewHelper(AbstractViewHelper):

    def getEntidade(self, request):
        pass

    def setView(self, resultado, request):
        pass
