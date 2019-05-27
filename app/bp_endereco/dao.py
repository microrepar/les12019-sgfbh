"""[summary]
"""

from les12019_core.abstract_dao import AbstractDAO
from les12019_core import utils
from app import db

from app.bp_funcionario.models import Funcionario
from app.bp_endereco.models import Endereco, StatusEndereco, Logradouro, TipoEndereco

from flask import flash


########################### Classe Concreta - DAO de Endereco##################################
class EnderecoDAO(AbstractDAO):

    def salvar(self, entidade):
        logradouro = Logradouro.query.filter(Logradouro.cep==entidade.cep).first()

        if logradouro is None:
            try:
                endereco = super().salvar(entidade)
            except Exception as e:
                print(e)
                db.session.rollback()
                return utils.ERRO_SALVAR_ENDERECO_BD.format(entidade._logradouro.logradouro)
            else:
                if isinstance(endereco, Endereco):
                    flash(utils.SUCESSO_SALVAR_ENDERECO_BD.format(entidade._logradouro.logradouro))
                    return endereco
                else:
                    return utils.ERRO_SALVAR_ENDERECO_BD.format(entidade._logradouro.logradouro)
        else:
            entidade._logradouro = None
            logradouro._enderecos_moradores.append(entidade)
            try:
                endereco = super().salvar(entidade)
            except Exception as e:
                print(e)
                db.session.rollback()
                return utils.ERRO_SALVAR_ENDERECO_BD.format(entidade._logradouro.logradouro)
            else:
                if isinstance(endereco, Endereco):
                    flash(utils.SUCESSO_SALVAR_ENDERECO_BD.format(entidade._logradouro.tipo_logradouro +' '+entidade._logradouro.logradouro))
                    return endereco
                else:
                    return utils.ERRO_SALVAR_ENDERECO_BD.format(entidade._logradouro.logradouro)


    def listar(self, entidade):
        pass

    def alterar(self, entidade: Endereco):
        endereco: Endereco = super().consultarPorId(entidade)
        
        if endereco is not None:
            endereco.cep = entidade.cep
            endereco.numero = entidade.numero
            endereco.complemento_endereco = entidade.complemento_endereco
            endereco.observacoes = entidade.observacoes
            endereco.funcionario_id = entidade.funcionario_id
            endereco.tipo_endereco_id = entidade.tipo_endereco_id
            endereco.status_id = entidade.status_id 

            try:
                db.session.add(endereco)
                db.session.commit()
            except:
                db.session.rollback()    
                return utils.ERRO_ATUALIZAR_ENDERECO.format(entidade.cep)
                
            logradouro = Logradouro.query.filter(Logradouro.cep == entidade.cep).first()

            if not logradouro:
                logradouro = Logradouro(cep=entidade._logradouro.cep, tipo_logradouro=entidade._logradouro.tipo_logradouro,
                    logradouro=entidade._logradouro.logradouro,bairro=entidade._logradouro.bairro,
                    uf=entidade._logradouro.uf, cidade=entidade._logradouro.cidade) 

                db.session.add(logradouro)
                logradouro._enderecos_moradores.append(endereco)
                try:
                    db.session.commit()
                except Exception as e:
                    print(str(e))
                    db.session.rollback()
                    return utils.ERRO_ATUALIZAR_ENDERECO.format(entidade.cep)
                else:
                    flash(utils.SUCESSO_ATUALIZAR_ENDERECO.format(entidade._logradouro.tipo_logradouro + ' ' + entidade._logradouro.logradouro))
                    return endereco
            else:
                try:
                    logradouro._enderecos_moradores.append(endereco)
                    db.session.commit()
                except Exception as e:
                    print(str(e))
                    db.session.rollback()
                    return utils.ERRO_ATUALIZAR_ENDERECO.format(entidade.cep)
                else:
                    flash(utils.SUCESSO_ATUALIZAR_ENDERECO.format(entidade._logradouro.tipo_logradouro + ' ' + logradouro.logradouro))
                    return endereco
        return utils.ERRO_CONSULTA_POR_ID_ENDERECO.format(entidade.id)

    
    def consultarPorId(self, entidade: Endereco):
        endereco: Endereco= super().consultarPorId(entidade)
        if entidade.cep is not None:
            endereco.cep = entidade.cep
        return endereco


    def consultarPorParametro(self, entidade):
        pass


    def consultar(self, entidade):
        _repositorio = entidade.__class__
        endereco = _repositorio.query.filter(Endereco.status_id != 3).order_by(Endereco.logradouro_id.asc()).all()
        return endereco


    def excluir(self, entidade):
        endereco: Endereco = super().consultarPorId(entidade)
        endereco._status = StatusEndereco.query.filter(StatusEndereco.nome=='EXCLUIDO').first()
        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_EXCLUIR_ENDERECO.format(entidade.cep)
        else:
            flash(utils.SUCESSO_EXCLUIR_ENDERECO.format(entidade.cep))
            return entidade

        
