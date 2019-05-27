from les12019_core.abstract_dao import AbstractDAO
from app.bp_frequencia.models import EspelhoMensal, EspelhoDiario, StatusEspelho
from sqlalchemy import and_
from app import db


########################### Classe Concreta - DAO de Base para implementar##################################
class EspelhoMensalDAO(AbstractDAO):

    def salvar(self, entidade: EspelhoMensal):
        pass

    def listar(self, entidade: EspelhoMensal):
        pass

    def alterar(self, entidade: EspelhoMensal):
        pass

    def consultarPorId(self, entidade: EspelhoMensal):
        espelho_mensal = super().consultarPorId(entidade)
        return espelho_mensal

    def consultarPorParametro(self, entidade: EspelhoMensal):
        espelhos_mensais = EspelhoMensal.query.filter(
            and_(EspelhoMensal.funcionario_id==entidade.funcionario.id, EspelhoMensal.status_id != 3)).all()
        
        return espelhos_mensais

    def consultar(self, entidade: EspelhoMensal):
        espelhos_mensais = EspelhoMensal.query.filter(EspelhoMensal.status_id != 3).all()
        return espelhos_mensais

    def excluir(self, entidade: EspelhoMensal):
        pass


########################### Classe Concreta - DAO de EspelhoDiario ##################################
class EspelhoDiarioDAO(AbstractDAO):

    def salvar(self, entidade: EspelhoDiario):
        pass

    def listar(self, entidade: EspelhoDiario):
        pass

    def alterar(self, entidade: EspelhoDiario):
        pass

    def consultarPorId(self, entidade: EspelhoDiario):
        espelho_dia = super().consultarPorId(entidade)
        return espelho_dia

    def consultarPorParametro(self, entidade: EspelhoDiario):
        pass

    def consultar(self, entidade: EspelhoDiario):
        pass

    def excluir(self, entidade: EspelhoDiario):
        pass



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

