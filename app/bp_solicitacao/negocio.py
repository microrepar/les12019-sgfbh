from les12019_core.abstract_strategy import AbstractStrategy
from les12019_core import utils
from app.bp_ocorrencia.models import Ocorrencia
from app.bp_solicitacao.models import Solicitacao, Despacho, Decisao, StatusSolicitacao, StatusDespacho, TipoSolicitacao
from sqlalchemy import and_
from flask_login import current_user
from flask import flash
import datetime


class ApensadorDadosSalvarAtualizarSolicitacao(AbstractStrategy):

    def processar(self, entidade: Solicitacao):
        if isinstance(entidade, Solicitacao):
            solicitacao: Solicitacao = entidade
            
            ocorrencia = Ocorrencia.query.filter_by(id=entidade.ocorrencia.id).first()

            if ocorrencia is None:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Ocorrência"')

            solicitacao.ocorrencia = ocorrencia

            if entidade.tipo.id != '':
                tipo = TipoSolicitacao.query.filter_by(id=entidade.tipo.id).first()
                if tipo is None:
                    flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Tipo de solicitação"'))
                else:
                    solicitacao.tipo = tipo

            if entidade.status.id != '':
                status = StatusSolicitacao.query.filter_by(id=entidade.status.id).first()
                if status is None:
                    flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Status de solicitação"'))
                else:
                    solicitacao.status = status
            else:
                solicitacao.status = StatusSolicitacao.query.filter_by(id=1).first()

            lista_status = StatusSolicitacao.query.all()
            lista_tipos = TipoSolicitacao.query.all()

            if len(lista_status) == 0:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Status de solicitação"'))

            if len(lista_tipos) == 0:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Tipos de solicitação"'))

            solicitacao._lista_status = lista_status
            solicitacao._lista_tipos = lista_tipos

        else:
            return 'O objeto não é uma instância de Solicitação!'

        return None


class ValidadorDadosObrigatoriosSolicitacao(AbstractStrategy):
    
    def processar(self, entidade: Solicitacao):
        if isinstance(entidade, Solicitacao):
            solicitacao: Solicitacao = entidade
            mensagens = []
            if not all([solicitacao.tipo.id, solicitacao.descricao]):
                mensagens.append(utils.ERRO_SALVAR_ENTIDADE_RNS.format('Os campos com (*) são obrigatórios e devem ser devidamente preenchidos!'))
            
            if solicitacao.tipo.id == '':
                mensagens.append(utils.ERRO_SALVAR_ENTIDADE_RNS.format('Um tipo de solicitação deve ser selecionado!'))

            if len(mensagens) != 0:
                return mensagens
        else:
            return 'O objeto não é uma instância de Solicitação!'

        return None


class ComplementarDadosSolicitacao(AbstractStrategy):

    def processar(self, entidade: Solicitacao):
        if isinstance(entidade, Solicitacao):
            solicitacao: Solicitacao = entidade

            if current_user.is_authenticated:
                solicitacao.responsavel_cadastro = current_user.username
            solicitacao.data_cadastro = datetime.datetime.now()

        else:
            return 'O objeto não pode ser cadastrado, pois não é uma instância de solicitação.'



class ApensadorDadosPreOperacaoSalvarAtualizarDespacho(AbstractStrategy):
    
    def processar(self, entidade: Despacho):
        if isinstance(entidade, Despacho):
            despacho: Despacho = entidade

            solicitacao = Solicitacao.query.filter_by(id=entidade.solicitacao.id).first()

            if solicitacao is None:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Solicitação"')
            
            despacho.solicitacao = solicitacao

            if entidade.decisao.id != '':
                decisao = Decisao.query.filter_by(id=entidade.decisao.id).first()
                if decisao is None:
                    flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Tipo de decisão"'))
                else:
                    despacho.decisao = decisao
            
            lista_decisoes = Decisao.query.all()

            if len(lista_decisoes) == 0:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Tipos de decisão"'))

            despacho._lista_decisoes = lista_decisoes

        else:
            return 'O objeto não é uma instância de Despacho!'

        return None


class ValidadorDadosObrigatoriosDespacho(AbstractStrategy):
    
    def processar(self, entidade: Despacho):
        if isinstance(entidade, Despacho):
            despacho: Despacho = entidade
            mensagens = []
            if not all([despacho.solicitacao.id, despacho.decisao.id]):
                mensagens.append(utils.ERRO_SALVAR_ENTIDADE_RNS.format('Os campos com (*) são obrigatórios e devem ser devidamente preenchidos!'))
            
            if len(mensagens) != 0:
                return mensagens
        else:
            return 'O objeto não é uma instância de Despacho!'

        return None


class ComplementarDadosDespacho(AbstractStrategy):

    def processar(self, entidade: Despacho):
        if isinstance(entidade, Despacho):
            despacho: Despacho = entidade

            if current_user.is_authenticated:
                despacho.responsavel_cadastro = current_user.username
            despacho.data_cadastro = datetime.datetime.now()

        else:
            return 'O objeto não pode ser cadastrado, pois não é uma instância de despacho.'


class _Strategy(AbstractStrategy):
    def processar(self, entidade):
        if isinstance(entidade, object):
            pass
        else:
            pass

        return None
