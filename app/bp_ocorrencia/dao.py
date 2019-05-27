from les12019_core.abstract_dao import AbstractDAO
from les12019_core import utils
from app.bp_ocorrencia.models import Ocorrencia, Pendencia, StatusOcorrencia, StatusPendencia, TipoPendencia, PeriodoOcorrencia
from app.bp_frequencia.models import EspelhoDiario
from flask import flash
from app import db

########################### Classe Concreta - DAO de Base para implementar##################################
class OcorrenciaDAO(AbstractDAO):

    def salvar(self, entidade: Ocorrencia):
        
        mensagens = []

        status = StatusOcorrencia.query.filter_by(id=1).first()
        periodo = PeriodoOcorrencia.query.filter_by(id=entidade.periodo.id).first()
        pendencia = Pendencia.query.filter_by(id=entidade.pendencia.id).first()
        espelho_diario = EspelhoDiario.query.filter_by(id=entidade.espelho_diario.id).first()

        if all([status, periodo, pendencia, espelho_diario]):
            ocorrencia: Ocorrencia = entidade
            
            del entidade.status
            del entidade.periodo
            del entidade.pendencia
            del entidade.espelho_diario
            db.session.rollback()

            ocorrencia.status = status
            ocorrencia.periodo = periodo
            ocorrencia.pendencia = pendencia
            ocorrencia.espelho_diario = espelho_diario

        else:
            if status is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Status de ocorrência"')) 

            if periodo is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Período de ocorrência"')) 

            if pendencia is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Pendência de ocorrência"')) 

            if espelho_diario is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Espelho diário de ocorrência"'))  

        if len(mensagens) != 0:
            return '\n'.join(mensagens)

        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_SALVAR_ENTIDADE_BD.format(f'ocorrência {ocorrencia.pendencia.nome} da {ocorrencia.periodo.momento} do {ocorrencia.periodo.nome} do dia {ocorrencia.espelho_diario.data_formatada}')
        else:
            flash(utils.SUCESSO_SALVAR_ENTIDADE_BD.format(f'ocorrência {ocorrencia.pendencia.nome} da {ocorrencia.periodo.momento} do {ocorrencia.periodo.nome} do dia {ocorrencia.espelho_diario.data_formatada}'))
            return ocorrencia



    def listar(self, entidade: Ocorrencia):
        pass

    def alterar(self, entidade: Ocorrencia):
        db.session.expunge_all()
        mensagens = []

        ocorrencia: Ocorrencia = Ocorrencia.query.filter_by(id=entidade.id).first()

        if ocorrencia is not None:            
            
            if ocorrencia.pendencia.id != entidade.pendencia.id:  
                pendencia = Pendencia.query.filter_by(id=entidade.pendencia.id).first()              
                if pendencia is not None:
                    ocorrencia.pendencia = pendencia
                else:
                    mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Pendência"'))
            
            if ocorrencia.status.id != entidade.status.id:
                status = StatusOcorrencia.query.filter_by(id=entidade.status.id).first()             
                if status is not None:
                    ocorrencia.status = status
                else:
                    mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Status de Ocorrência"'))

            if ocorrencia.periodo.id != entidade.periodo.id:                
                periodo = PeriodoOcorrencia.query.filter_by(id=entidade.periodo.id).first()
                if periodo is not None:
                    ocorrencia.periodo = periodo
                else:
                    mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Período"'))
                    

            if len(mensagens) != 0:
                return '\n'.join(mensagens)            

            ocorrencia.quantidade_horas = entidade.quantidade_horas
            ocorrencia.cobranca = entidade.cobranca
            ocorrencia.data_inicio = entidade.data_inicio
            ocorrencia.data_fim = entidade.data_fim
            ocorrencia.observacao = entidade.observacao

            try:                
                db.session.commit()
            except Exception as e:
                print(str(e))
                db.session.rollback()                
                return utils.ERRO_ATUALIZAR_ENTIDADE_BD.format('Ocorrência')
            else:
                flash(utils.SUCESSO_ATUALIZAR_ENTIDADE_BD.format(f'Ocorrência'))
                return ocorrencia

        else:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Ocorrência teste')



    def consultarPorId(self, entidade: Ocorrencia):
        ocorrencia = super().consultarPorId(entidade)
        return ocorrencia

    def consultarPorParametro(self, entidade: Ocorrencia):
        pass

    def consultar(self, entidade: Ocorrencia):
        pass

    def excluir(self, entidade: Ocorrencia):
        ocorrencia: Ocorrencia = super().consultarPorId(entidade)        

        if ocorrencia is not None:
            nome_pendencia = ocorrencia.pendencia.nome
            
            foi_excluido = super().excluir(ocorrencia)
            if foi_excluido:
                flash(utils.SUCESSO_EXCLUIR_ENTIDADE.format(f'Ocorrência {nome_pendencia}'))
                return foi_excluido
            else:
                return utils.ERRO_EXCLUIR_ENTIDADE.format(f'Ocorrência de {nome_pendencia}')
        else:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format(f'Ocorrência')




########################### Classe Concreta - DAO de Base para implementar##################################
class PendenciaDAO(AbstractDAO):

    def salvar(self, entidade: Pendencia):
        
        mensagens = []
        
        tipo: TipoPendencia = TipoPendencia.query.filter_by(id=entidade.tipo.id).first()
        status: StatusPendencia = StatusPendencia.query.filter_by(id=entidade.status.id).first()

        if all([tipo, status]):
            pendencia: Pendencia = entidade
            del pendencia.status
            del pendencia.tipo
            pendencia.status = status
            pendencia.tipo = tipo
        else:
            if tipo is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Tipo de pendencia"'))
            if status is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Status de pendencia"'))

        if len(mensagens) !=0:
            return '\n'.join(mensagens)

        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_SALVAR_ENTIDADE_BD.format(f'Pendência {pendencia.nome}')
        else:
            flash(utils.SUCESSO_SALVAR_ENTIDADE_BD.format(f'Pendência {pendencia.nome}'))
            return pendencia
            

    def listar(self, entidade: Pendencia):
        pass

    def alterar(self, entidade: Pendencia):
        mensagens = []

        pendencia: Pendencia = Pendencia.query.filter_by(id=entidade.id).first()

        if pendencia is not None:

            if pendencia.status.id != entidade.status.id:
                status = StatusPendencia.query.filter_by(id=entidade.status.id).first()
                if status is not None:
                    pendencia.status = status
                else:
                    mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status de Pendência'))

            if pendencia.tipo.id != entidade.tipo.id:
                tipo = TipoPendencia.query.filter_by(id=entidade.tipo.id).first()
                if tipo is not None:
                    pendencia.tipo = tipo
                else:
                    mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Tipo de Pendência'))

            if len(mensagens) != 0:
                return '\n'.join(mensagens)
            
            pendencia.codigo = entidade.codigo
            pendencia.nome = entidade.nome
            pendencia.sigla = entidade.sigla
            pendencia.prazo_pagamento_dias = entidade.prazo_pagamento_dias
            pendencia.limite_maximo_horas = entidade.limite_maximo_horas
            pendencia.descricao = entidade.descricao                

            try:
                db.session.commit()
            except Exception as e:
                print(str(e))
                db.session.rollback()
                return utils.ERRO_SALVAR_ENTIDADE_BD.format('Pendência')
            else:
                flash(utils.SUCESSO_SALVAR_ENTIDADE_BD.format(f'Pendência "{pendencia.nome}"'))
                return pendencia

        else:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Pendência')
           

    def consultarPorId(self, entidade: Pendencia):
        pendencia = super().consultarPorId(entidade)
        return pendencia

    def consultarPorParametro(self, entidade: Pendencia):
        pass

    def consultar(self, entidade: Pendencia):
        pendencias = Pendencia.query.filter(Pendencia.status_id != 3).all()
        return pendencias

    def excluir(self, entidade: Pendencia):   

        pendencia: Pendencia = super().consultarPorId(entidade)
        
        if pendencia is not None:
            foi_excluido = super().excluir(pendencia)
            if foi_excluido:
                flash(utils.SUCESSO_EXCLUIR_ENTIDADE.format(f'Pendência {entidade.nome}'))
                return foi_excluido
            else:
                return utils.ERRO_EXCLUIR_ENTIDADE.format(f'Pendência {pendencia.nome}')
        else:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format(f'Pendencia de código={entidade.codigo} nome={entidade.nome}')
