from les12019_core.abstract_dao import AbstractDAO
from les12019_core import utils
from app.bp_ponto.models import Ponto, StatusPonto
from app.bp_funcionario.models import Funcionario
from app.bp_frequencia.models import EspelhoDiario
from app import db
from flask import flash
import datetime

class PontoDAO(AbstractDAO):

    def salvar(self, entidade: Ponto):

        contador_msg = 0
        ponto: Ponto = entidade

        funcionario = Funcionario.query.filter_by(id=entidade.funcionario.id).first()
        espelho_diario = EspelhoDiario.query.filter_by(id=entidade.espelho_diario.id).first()
        status = StatusPonto.query.filter_by(id=entidade.status.id).first()

        if all([funcionario, espelho_diario, status]):
            del ponto.funcionario
            del ponto.espelho_diario
            del ponto.status            
            ponto.funcionario = funcionario
            ponto.espelho_diario = espelho_diario
            ponto.status = status
            ponto.relogio = 'manual'            
            ponto.responsavel_cadastro = 'mcsilva'
            ponto.data_cadastro = datetime.datetime.now()
        else:
            if funcionario is None:
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Funcionario"'))
                contador_msg += 1
                
            if espelho_diario is None:
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Espelho Diário"'))
                contador_msg += 1
                
            if status is None:
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Status do Ponto"'))
                contador_msg += 1
        
        if contador_msg != 0:
            return 'Um ou mais objetos não foram encontrados no banco de dados'
        
        try:
            db.session.add(ponto)
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_SALVAR_ENTIDADE_BD.format('"ponto"')
        else:
            flash(utils.SUCESSO_SALVAR_ENTIDADE_BD.format(f'"Ponto" das {ponto.hora_formatada}'))
            return ponto

    def listar(self, entidade: Ponto):
        pass

    def alterar(self, entidade: Ponto):
        contador_msg = 0
        ponto: Ponto = Ponto.query.filter_by(id=entidade.id).first()
        status = StatusPonto.query.filter_by(id=entidade.status.id).first()
        if all([ponto, status]):
            ponto.data_hora = entidade.data_hora
            ponto.incluir = entidade.incluir
            ponto.observacao = entidade.observacao
            ponto.status = status
        else:
            if ponto is None:
                contador_msg += 1
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Ponto"'))
            if status is None:
                contador_msg += 1
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Status de ponto"'))

        if contador_msg != 0:
            return 'Um ou mais objetos não foram encontrados no banco de dados'

        try:
            del entidade.status
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_ATUALIZAR_ENTIDADE_BD.format('"Ponto"')
        else:
            flash(utils.SUCESSO_ATUALIZAR_ENTIDADE_BD.format(f'"Ponto" das {ponto.hora_formatada}'))
            return ponto




    def consultarPorId(self, entidade: Ponto):
        ponto = super().consultarPorId(entidade)
        return ponto

    def consultarPorParametro(self, entidade: Ponto):
        pass

    def consultar(self, entidade: Ponto):
        pass

    def excluir(self, entidade: Ponto):

        ponto: Ponto = super().consultarPorId(entidade)
        
        if ponto is not None:
            entidade.espelho_diario.id = ponto.espelho_diario.id
            hora_ponto = ponto.hora_formatada
            foi_excluido = super().excluir(ponto)
            if foi_excluido:
                flash(utils.SUCESSO_EXCLUIR_ENTIDADE.format(f'Ponto {hora_ponto}'))
                return foi_excluido
            else:
                flash(utils.ERRO_EXCLUIR_ENTIDADE.format(f'Ponto {hora_ponto}'))
                return foi_excluido
        else:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format(f'Ponto {hora_ponto}')
