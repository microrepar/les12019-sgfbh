from les12019_core.abstract_dao import AbstractDAO
from les12019_core import utils
from app.bp_solicitacao.models import Solicitacao, Despacho, Decisao, StatusDespacho, StatusSolicitacao, TipoSolicitacao
from app.bp_ocorrencia.models import Ocorrencia, StatusOcorrencia
from app import db
from flask import flash

########################### Classe Concreta - DAO de Base para implementar##################################
class SolicitacaoDAO(AbstractDAO):

    def salvar(self, entidade: Solicitacao):
        
        mensagens = []

        solicitacao: Solicitacao = entidade

        tipo = TipoSolicitacao.query.filter_by(id=entidade.tipo.id).first()
        status = StatusSolicitacao.query.filter_by(id=1).first()
        ocorrencia = Ocorrencia.query.filter_by(id=entidade.ocorrencia.id).first()

        if all([tipo, status, ocorrencia]):

            del entidade.tipo
            del entidade.status
            del entidade.ocorrencia
            del entidade.despacho

            solicitacao.tipo = tipo
            solicitacao.status = status
            solicitacao.ocorrencia = ocorrencia            
            
        else:
            if tipo is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"tipo de solicitação"')) 

            if status is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Status de solicitação"')) 

            if ocorrencia is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Ocorrência da solicitação"')) 
           
        if len(mensagens) != 0:            
            return '\n'.join(mensagens)

        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_SALVAR_ENTIDADE_BD.format(f'Solicitação')
        else:
            flash(utils.SUCESSO_SALVAR_ENTIDADE_BD.format(f'Solicitação'))
            return solicitacao


    def listar(self, entidade: Solicitacao):
        pass

    def alterar(self, entidade: Solicitacao):
        
        mensagens = []

        solicitacao = Solicitacao.query.filter_by(id=entidade.id).first()

        if solicitacao is not None:

            if solicitacao.tipo.id != entidade.tipo.id:
                tipo = TipoSolicitacao.query.filter_by(id=entidade.tipo.id).first()
                if tipo is not None:
                    solicitacao.tipo = tipo
                else:
                    mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Tipo de solicitação"'))
            
            if len(mensagens) != 0:
                return '\n'.join(mensagens)

            solicitacao.descricao = entidade.descricao
            
            try:
                db.session.commit()
            except Exception as e:
                print(str(e))
                db.session.rollback()
                return utils.ERRO_ATUALIZAR_ENTIDADE_BD.format('Solicitação')
            else:
                flash(utils.SUCESSO_ATUALIZAR_ENTIDADE_BD.format('Solicitação'))
                return solicitacao
        
        else:
            return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Solicitação')
            

    def consultarPorId(self, entidade: Solicitacao):
        solicitacao = super().consultarPorId(entidade)
        return solicitacao

    def consultarPorParametro(self, entidade: Solicitacao):
        pass

    def consultar(self, entidade: Solicitacao):
        solicitacoes = Solicitacao.query.filter(Solicitacao.status_id!=3).all()
        return solicitacoes

    def excluir(self, entidade: Solicitacao):
        solicitacao: Solicitacao = super().consultarPorId(entidade)
        ocorrencia: Ocorrencia = solicitacao.ocorrencia
        status_ocorrencia = StatusOcorrencia.query.filter_by(id=1).first()

        if all([solicitacao, ocorrencia, status_ocorrencia]):
            if solicitacao is not None:

                foi_excluido = super().excluir(solicitacao)
                if foi_excluido:
                
                    if status_ocorrencia is not None:
                        ocorrencia.status = status_ocorrencia

                    try:
                        db.session.commit()
                    except Exception as e:
                        print(str(e))
                        flash(utils.ERRO_ATUALIZAR_ENTIDADE_BD.format('Status de Ocorrência'))

                    flash(utils.SUCESSO_EXCLUIR_ENTIDADE.format('Solicitação'))
                    return foi_excluido
                else:
                    return utils.ERRO_EXCLUIR_ENTIDADE.format('Solicitação')
            else:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Solicitação')
        else:
            return False


########################### Classe Concreta - DAO de Base para implementar##################################
class DespachoDAO(AbstractDAO):

    def salvar(self, entidade: Despacho):
        mensagens = []

        despacho: Despacho = entidade

        decisao = Decisao.query.filter_by(id=entidade.decisao.id).first()
        solicitacao = Solicitacao.query.filter_by(id=entidade.solicitacao.id).first()

        if all([decisao, solicitacao]):
            del entidade.decisao
            del entidade.solicitacao

            despacho.decisao = decisao
            despacho.solicitacao = solicitacao
        else:
            if decisao is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"tipo de decisão"'))
            
            if solicitacao is None:
                mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"solicitacao"'))
                            
           
        if len(mensagens) != 0:            
            return '\n'.join(mensagens)

        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_SALVAR_ENTIDADE_BD.format(f'Decisão')
        else:
            flash(utils.SUCESSO_SALVAR_ENTIDADE_BD.format(f'Decisão'))
            msg = despacho.concluir()
            if msg is None:
                return despacho
            return msg

    def listar(self, entidade: Despacho):
        pass

    def alterar(self, entidade: Despacho):
        pass

    def consultarPorId(self, entidade: Despacho):
        pass

    def consultarPorParametro(self, entidade: Despacho):
        pass

    def consultar(self, entidade: Despacho):
        pass

    def excluir(self, entidade: Despacho):
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
