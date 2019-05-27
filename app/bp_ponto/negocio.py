from les12019_core.abstract_strategy import AbstractStrategy
from les12019_core import utils
from app.bp_ponto.models import Ponto, StatusPonto
from app.bp_funcionario.models import Funcionario
from app.bp_frequencia.models import EspelhoDiario
from flask import flash
from sqlalchemy import and_
from app import db

import datetime


class ApensadorPreOperacaoSalvarPonto(AbstractStrategy):
    
    def processar(self, entidade: Ponto):
        
        if isinstance(entidade, Ponto):

            ponto: Ponto = entidade
            
            espelho_dia = EspelhoDiario.query.filter_by(id=ponto.espelho_diario.id).first()
            funcionario = Funcionario.query.filter_by(id=espelho_dia.funcionario.id).first()
            
            if ponto.status.nome is None:
                status = StatusPonto.query.filter_by(id=1).first()
            else:
                status = StatusPonto.query.filter_by(id=ponto.status.id).first()
                        
            if all([funcionario, status, espelho_dia]):
                ponto.funcionario = funcionario
                ponto.espelho_diario = espelho_dia
                ponto.status = status
            else:
                if funcionario is None:
                    flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Funcionario"'))
                if espelho_dia is None:
                    flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Espelho Diário"'))


            lista_status = StatusPonto.query.all()

            if len(lista_status) == 0:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Status de ponto"'))

            ponto._lista_status = lista_status


class ComplentadorDadosCadastroPonto(AbstractStrategy):

    def processar(self, entidade: Ponto):
        if isinstance(entidade, Ponto):
            ponto: Ponto = entidade
            ponto.data_cadastro = datetime.datetime.utcnow()
            ponto.responsavel_cadastro = 'mcsilva'
        else:
            return 'Não foi possivel salvar devido a instância ser um objeto Ponto!'
        
        return None


class ValidadorDadosObrigatoriosPonto(AbstractStrategy):

    def processar(self, entidade: Ponto):        
        if isinstance(entidade, Ponto):

            ponto: Ponto = Ponto.query.filter_by(id=entidade.id).first()
            qtde_pontos_ativo = Ponto.query.filter(and_(Ponto.espelho_diario_id==entidade.espelho_diario.id, Ponto.incluir==True)).count()
            
            if not all([entidade.hora_formatada, entidade.status.id, entidade.observacao]):
                return utils.ERRO_SALVAR_ENTIDADE_RNS.format('Os campos com (*) devem ser devidamente preenchidos!')
            if len(entidade.observacao) < 20:
                return 'O texto da observação deve conter no mínimo 20 caracteres!'

            if qtde_pontos_ativo < 4 and (ponto.status.id == '1' or ponto.status.id == '2'):
                entidade.incluir = True
                entidade.status = StatusPonto.query.filter_by(id=1).first()

            else:
                entidade.incluir = False
                ponto.status = StatusPonto.query.filter_by(id=2).first()
        else:
            return 'Não foi possivel salvar devido a instância ser um objeto Ponto!'

        return None

            
class ValidadorOpcaoIncluirPonto(AbstractStrategy):

    def processar(self, entidade: Ponto):
        if isinstance(entidade, Ponto):
            
            ponto: Ponto = Ponto.query.filter_by(id=entidade.id).first()

            if ponto is not None:                
                qtde_pontos_ativo = Ponto.query.filter(
                    and_(Ponto.espelho_diario_id==ponto.espelho_diario.id, Ponto.incluir==True, Ponto.id!=ponto.id)).count()

                if ponto.incluir:
                    ponto.incluir = False
                    ponto.status = StatusPonto.query.filter_by(id=2).first()
                else:
                    if qtde_pontos_ativo < 4 and (ponto.status.id == 1 or ponto.status.id == 2):
                        ponto.incluir = True
                        ponto.status = StatusPonto.query.filter_by(id=1).first()
                    else:
                        entidade.status = ponto.status
                        entidade.espelho_diario = ponto.espelho_diario
                        entidade.funcionario = ponto.funcionario
                        return 'O "ponto" não pode ser incluido, pois são permitidos no máximo 4 pontos com status aprovado para a escala de trabalho cadastrada.'
                
            else:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Ponto"')
            
            db.session.commit()
            entidade.status = ponto.status
            entidade.espelho_diario = ponto.espelho_diario
            entidade.funcionario = ponto.funcionario
        else:
            return 'Não foi possivel salvar devido a instância ser um objeto Ponto!'

        return None


class VerificadorExistenciaExcluir(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Ponto):

            ponto: Ponto = Ponto.query.filter_by(id=entidade.id).first()

            if ponto is None:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Ponto"')
            
        else:
            return 'Não foi possivel salvar devido a instância ser um objeto Ponto!'

        return None
