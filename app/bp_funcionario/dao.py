"""[summary]
"""

from les12019_core.abstract_dao import AbstractDAO
from les12019_core import utils
from app import db


from app.bp_funcionario.models import Funcionario, StatusFuncionario, TipoVinculo, Cargo
from app.bp_frequencia.models import EspelhoMensal, EspelhoDiario, StatusEspelho

from flask import flash
from sqlalchemy import and_
import datetime


########################### Classe Concreta - DAO de funcionario##################################
class FuncionarioDAO(AbstractDAO):

    def salvar(self, entidade: Funcionario):
        funcionario: Funcionario= entidade
        msg = []
        data_cadastro: datetime.datetime = funcionario.dataCadastro

        status_funcionario: StatusFuncionario= StatusFuncionario.query.filter_by(nome=entidade._status.nome).first()
        tipo_vinculo_funcionario: TipoVinculo= TipoVinculo.query.filter_by(nome=entidade._tipo_vinculo.nome).first()
        cargo_funcionario: Cargo= Cargo.query.filter_by(nome=entidade.cargo.nome).first()
        espelho_mensal: EspelhoMensal = EspelhoMensal.query.filter(
            and_(EspelhoMensal.mes_referencia==data_cadastro.month, EspelhoMensal.ano_referencia==data_cadastro.year)
        ).first()

        
        if tipo_vinculo_funcionario is None:
             msg.append(utils.ERRO_CONSULTA_ENTIDADE.format('Tipo de Vínculo de Funcionário'))

        if status_funcionario is None:
            msg.append(utils.ERRO_CONSULTA_ENTIDADE.format('Status de Funcionário'))

        if cargo_funcionario is None:
            msg.append(utils.ERRO_CONSULTA_ENTIDADE.format(f'cargo {entidade.cargo.nome}'))

        if len(msg) != 0:
            return msg

        try:
            funcionario._status = None
            funcionario._tipo_vinculo = None
            funcionario.cargo = None
            funcionario._status = status_funcionario
            funcionario._tipo_vinculo = tipo_vinculo_funcionario
            funcionario.cargo = cargo_funcionario

            _funcionario = super().salvar(funcionario)

        except Exception as e:
            print(e)
            return utils.ERRO_SALVAR_FUNCIONARIO_BD.format(entidade.nome)
        else:
            if isinstance(_funcionario, Funcionario):
                flash(utils.SUCESSO_SALVAR_FUNCIONARIO_BD.format(entidade.nome))
                return _funcionario
            else:
                return utils.ERRO_SALVAR_FUNCIONARIO_BD.format(entidade.nome)

    def listar(self, entidade: Funcionario):
        funcionarios = super().listar(entidade)

        if funcionarios is not None:
            if len(funcionarios) > 0:
                flash(utils.SUCESSO_LISTAR_TODOS.format(
                    len(funcionarios), Funcionario.__name__.capitalize()))
                return funcionarios
            else:
                return utils.ERRO_LISTAR_TODOS.format('0')
        return utils.ERRO_LISTAR_TODOS.format('0')


    def alterar(self, entidade: Funcionario):
        funcionario: Funcionario = super().consultarPorId(entidade)
        msg = []        
        funcionario.cpf = entidade.cpf
        funcionario.nome = entidade.nome
        funcionario.sexo = entidade.sexo
        funcionario.pisPasep = entidade.pisPasep
        funcionario.rg = entidade.rg
        funcionario.email = entidade.email
        funcionario.responsavelCadastro = entidade.responsavelCadastro
        funcionario.matricula = entidade.matricula        
        funcionario.lotacao = entidade.lotacao
        funcionario.unidadeDeTrabalho = entidade.unidadeDeTrabalho
        funcionario.numeroCTPS = entidade.numeroCTPS
        funcionario.serieCTPS = entidade.serieCTPS
        funcionario.ufCTPS = entidade.ufCTPS
        funcionario.nomeUsuario = entidade.nomeUsuario
        funcionario.senha = entidade.senha
        funcionario.dataCadastro = entidade.dataCadastro
        funcionario.dataAdmissao = entidade.dataAdmissao
        funcionario.dataNascimento = entidade.dataNascimento
        funcionario.dataEmissaoCTPS = entidade.dataEmissaoCTPS

        status_funcionario = StatusFuncionario.query.filter_by(nome=entidade._status.nome).first()
        tipo_vinculo_funcionario = TipoVinculo.query.filter_by(nome=entidade._tipo_vinculo.nome).first()
        cargo_funcionario = Cargo.query.filter_by(nome=entidade.cargo.nome).first()

        if cargo_funcionario is None:
            msg.append(utils.ERRO_CONSULTA_ENTIDADE.format(f'"Cargo" {entidade.cargo.nome}'))
            flash(utils.ERRO_CONSULTA_ENTIDADE.format(f'"Cargo" {entidade.cargo.nome}'))

        if status_funcionario is None:
            msg.append(utils.ERRO_CONSULTA_ENTIDADE.format('"Status de funcionário"'))
            flash(utils.ERRO_CONSULTA_ENTIDADE.format('"Status de funcionário"'))

        if tipo_vinculo_funcionario is None:
            msg.append(utils.ERRO_CONSULTA_ENTIDADE.format('Tipo de Vínculo de Funcionário'))
            flash(utils.ERRO_CONSULTA_ENTIDADE.format('Tipo de Vínculo de Funcionário'))

        if len(msg) != 0:
            return 'Selecione os itens das listas!'


        funcionario.cargo = None
        funcionario._tipo_vinculo = None
        funcionario._status = None

        try:
            funcionario.cargo = cargo_funcionario
            funcionario._status = status_funcionario
            funcionario._tipo_vinculo = tipo_vinculo_funcionario
            db.session.commit()

        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_ATUALIZAR_FUNCIONARIO.format(entidade.nome)
            
        else:
            flash(utils.SUCESSO_ATUALIZAR_FUNCIONARIO.format(entidade.nome))
            return funcionario


    def consultarPorId(self, entidade):
        funcionario = super().consultarPorId(entidade)
        print('>>>>>>>>>>DAO FUNCIONARIO>>>>>>>>>>>>', funcionario)
        return funcionario

    def consultarPorParametro(self, entidade: Funcionario):
        funcionarios = None
        parametros = list(vars(entidade).items())
        print('>>>>PARAMETROS DAO:', parametros)

        if entidade.id != '':
            funcionario = Funcionario.query.filter(Funcionario.id == entidade.id).first()
            if funcionario is not None:                
                return funcionario
            else:
                return utils.ERRO_FILTRO_PARAM_FUNCIONARIO.format('0')

        if entidade.matricula.strip() != '':
            funcionarios = Funcionario.query.filter(Funcionario.matricula == entidade.matricula).first()
            if funcionarios:
                flash(utils.SUCESSO_FILTRO_PARAM_FUNCIONARIO.format('1'))
                return funcionarios
            else:
                return utils.ERRO_FILTRO_PARAM_FUNCIONARIO.format('0')
        if entidade.cpf.strip() != '':
            funcionarios = Funcionario.query.filter(Funcionario.cpf == entidade.cpf).first()
            if funcionarios:
                flash(utils.SUCESSO_FILTRO_PARAM_FUNCIONARIO.format('1'))
                return funcionarios
            else:
                return utils.ERRO_FILTRO_PARAM_FUNCIONARIO.format('0')
        if entidade.nome.strip() != '':
            funcionarios = Funcionario.query.filter(Funcionario.nome.like(f'%{entidade.nome.upper()}%')).all()
            if funcionarios:
                flash(utils.SUCESSO_FILTRO_PARAM_FUNCIONARIO.format(
                    len(funcionarios)))
                return list(funcionarios)
            else:
                return utils.ERRO_FILTRO_PARAM_FUNCIONARIO.format('0')
        return utils.ERRO_FILTRO_PARAM_FUNCIONARIO_NONE.format('0')

    def consultar(self, entidade):
        _repositorio = entidade.__class__
        funcionarios = _repositorio.query.filter(Funcionario.status_id != '3').order_by(Funcionario.nome.asc()).all()
        return funcionarios

    def excluir(self, entidade: Funcionario):
        funcionario: Funcionario = super().consultarPorId(entidade)
        funcionario._status = StatusFuncionario.query.filter_by(nome='EXCLUIDO').first()
        try:
            db.session.commit()
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return utils.ERRO_EXCLUIR_FUNCIONARIO.format(funcionario.nome)
        else:
            flash(utils.SUCESSO_EXCLUIR_FUNCIONARIO.format(funcionario.nome))
            return funcionario
