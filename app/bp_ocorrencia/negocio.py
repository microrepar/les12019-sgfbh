from les12019_core.abstract_strategy import AbstractStrategy
from les12019_core import utils
from app.bp_ocorrencia.models import Pendencia, Ocorrencia, StatusOcorrencia, StatusPendencia, TipoPendencia, PeriodoOcorrencia
from app.bp_frequencia.models import EspelhoDiario
from sqlalchemy import and_
from flask_login import current_user
from flask import flash

import datetime

class ApensadorDadosSalvarAtualizarPendencia(AbstractStrategy):
    def processar(self, entidade: Pendencia):
        if isinstance(entidade, Pendencia):
            pendencia: Pendencia = entidade

            lista_tipos = TipoPendencia.query.all()
            lista_status = StatusPendencia.query.all()

            if len(lista_status) == 0:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Status de pendência"'))
            if len(lista_tipos) == 0:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Tipo de pendência"'))
           
            pendencia._lista_tipos = lista_tipos
            pendencia._lista_status = lista_status
            
        else:
            'O objeto não é um instancia de Pendencia!'

        return None

class ValidadorCamposObrigatoriosPendencia(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Pendencia):
            pendencia: Pendencia = entidade
            
            mensagens = []

            if not all([pendencia.codigo, pendencia.nome, pendencia.sigla, pendencia.tipo.id,
                        pendencia.prazo_pagamento_dias, pendencia.limite_maximo_horas, 
                        pendencia.status.id, pendencia.descricao]):
                mensagens.append(utils.ERRO_SALVAR_ENTIDADE_RNS.format('O campos com (*) devem ser preenchidos com dados válidos!'))
            
            if len(pendencia.descricao) < 20:
                mensagens.append(utils.ERRO_SALVAR_ENTIDADE_RNS.format('O texto da descrição deve conter mais que 20 caracteres!'))

            if len(mensagens) != 0:
                return mensagens

        else:
            return 'O objeto não é uma instância de Pendencia!'
    
        return None

class VerificadorExitenciaPendencia(AbstractStrategy):
    def processar(self, entidade):
        if isinstance(entidade, Pendencia):
            pendencia_codigo = Pendencia.query.filter(
                and_(Pendencia.codigo==entidade.codigo,Pendencia.id != entidade.id)).first()
            pendencia_sigla = Pendencia.query.filter(
                and_(Pendencia.sigla==entidade.sigla, Pendencia.id != entidade.id)).first()
            
            mensagens = []    
        
            if pendencia_codigo is not None:
                mensagens.append(utils.ERRO_SALVAR_ENTIDADE_RNS.format(f'Já existe uma pendência cadastra com o código="{entidade.codigo}"'))
            if pendencia_sigla is not None:
                mensagens.append(utils.ERRO_SALVAR_ENTIDADE_RNS.format(f'Já existe uma pendência cadastra com a sigla="{entidade.sigla}"'))

            if len(mensagens) != 0:
                return mensagens

        else:
            return 'O objeto não é uma instância de Pendencia!'

        return None


class VerificadorHouveAlteracaoDadosPendencia(AbstractStrategy):

    def processar(self, entidade: Pendencia):
        if isinstance(entidade, Pendencia):
            pendencia: Pendencia = Pendencia.query.filter_by(id=entidade.id).first()

            if pendencia is not None:
                if all([pendencia.codigo == int(entidade.codigo), pendencia.nome == entidade.nome, pendencia.sigla == entidade.sigla,
                        pendencia.tipo.id == int(entidade.tipo.id), pendencia.status.id == int(entidade.status.id), pendencia.descricao == entidade.descricao,
                        pendencia.prazo_pagamento_dias == int(entidade.prazo_pagamento_dias), pendencia.limite_maximo_horas == float(entidade.limite_maximo_horas),
                        ]):
                    return f'Não houve alterações nos dados da pendência {pendencia.nome}.'

        else:
            return 'O objeto não é uma instância de Pendencia!'

        return None


class ComplementarDadosPendencia(AbstractStrategy):

    def processar(self, entidade: Pendencia):
        if isinstance(entidade, Pendencia):
            pendencia: Pendencia = entidade

            if current_user.is_authenticated:
                pendencia.responsavel_cadastro = current_user.username
            pendencia.data_cadastro = datetime.datetime.now()

        else:
            return 'O objeto não pode ser cadastrado, pois não é uma instância de pendência.'


class ApensadorDadosSalvarAtualizarOcorrencia(AbstractStrategy):

    def processar(self, entidade: Ocorrencia):
        if isinstance(entidade, Ocorrencia):
            ocorrencia: Ocorrencia = entidade
            
            espelho_diario = EspelhoDiario.query.filter_by(id=entidade.espelho_diario.id).first()
            pendencia = Pendencia.query.filter_by(id=entidade.pendencia.id).first()

            if espelho_diario is None:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Espelho diário"')

            ocorrencia.espelho_diario = espelho_diario

            if pendencia is not None:
                ocorrencia.pendencia = pendencia
            elif entidade.pendencia.id != '':
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Pendência"'))

            lista_status = StatusOcorrencia.query.all()
            lista_pendencias = Pendencia.query.order_by(Pendencia.nome).all()
            lista_periodos = PeriodoOcorrencia.query.all()

            if len(lista_status) == 0:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Status de ocorrência"'))

            if len(lista_pendencias) == 0:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Pendência"'))

            if len(lista_periodos) == 0:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Período de ocorrência"'))

            ocorrencia._lista_status = lista_status
            ocorrencia._lista_pendencias = lista_pendencias
            ocorrencia._lista_periodos = lista_periodos


        else:
            return 'Os dados não pode ser cadastrado, pois não é uma instância de ocorrência.'

        return None



class ValidadorDadosObrigatoriosOcorrencia(AbstractStrategy):

    def processar(self, entidade: Ocorrencia):
        if isinstance(entidade, Ocorrencia):
            ocorrencia: Ocorrencia = entidade

            if not all([ocorrencia.data_inicio, ocorrencia.data_fim, ocorrencia.quantidade_horas, ocorrencia.observacao,
                    ocorrencia.pendencia.id, ocorrencia.periodo.id]):
                return utils.ERRO_SALVAR_ENTIDADE_RNS.format('Todos os campos com (*) devem ser devidamente preenchidos!')

        else:
            return 'O dados não pode ser cadastrado, pois não é uma instância de ocorrência.'

        return None


class ComplementarDadosOcorrencia(AbstractStrategy):

    def processar(self, entidade: Ocorrencia):
        if isinstance(entidade, Ocorrencia):
            ocorrencia: Ocorrencia = entidade

            if current_user.is_authenticated:
                ocorrencia.responsavel_cadastro = current_user.username
            ocorrencia.data_cadastro = datetime.datetime.now()

        else:
            return 'O objeto não pode ser cadastrado, pois não é uma instância de ocorrência.'



class _Strategy(AbstractStrategy):
    def processar(self, entidade):
        if isinstance(entidade, object):
            pass
        else:
            pass

        return None
