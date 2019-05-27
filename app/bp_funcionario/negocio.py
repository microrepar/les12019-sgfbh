from les12019_core.abstract_strategy import AbstractStrategy
from les12019_core import utils
from numbers import Integral
from flask import flash
import datetime

from app.bp_funcionario.models import Funcionario, StatusFuncionario, TipoVinculo, Cargo


######################################## Classes concretas de Strategy ########################################
class ApensadorDependeciasPreOperacaoSalvarFuncionarios(AbstractStrategy):

    def processar(self, entidade):
        if entidade is not None:
            if isinstance(entidade, Funcionario):
                funcionario: Funcionario= entidade

                lista_status_funcionario = StatusFuncionario.query.all()
                lista_tipos_vinculo = TipoVinculo.query.all()
                lista_cargos = Cargo.query.all()

                if len(lista_status_funcionario) < 1:
                    flash(utils.ERRO_CONSULTAR_STATUS_ENTIDADE.format('0', '"Status de Funcionário"') + 'Por favor, cadastre os status de funcionário')

                if len(lista_tipos_vinculo) < 1:
                    flash(utils.ERRO_CONSULTAR_TIPO_ENTIDADE.format('0', '"Tipo de Vínculo"') + 'Por favor, cadastre os tipos de vínculos de funcionário')
                
                funcionario._lista_status = lista_status_funcionario
                funcionario._lista_tipos_vinculo = lista_tipos_vinculo
                funcionario._lista_cargos = lista_cargos
            else:
                pass
        else:
            pass


class ValidadorCpf(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Funcionario):
            funcionario: Funcionario = entidade
            if len(funcionario.cpf) != 14 or funcionario._status.nome is None or funcionario._status.nome == '':
                return utils.ERRO_SALVAR_FUNCIONARIO_RNS.format(funcionario.nome) + " CPF deve conter 14 digitos!"
        else:
            return 'CPF não pode ser válidado, pois a entidade não é um funcionário!'

        return None


class ValidadorPisPasep(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Funcionario):
            funcionario: Funcionario = entidade
            if len(funcionario.pisPasep) != 11 or funcionario._status.nome is None:
                return utils.ERRO_SALVAR_FUNCIONARIO_RNS.format(funcionario.nome) + " PISPASEP deve conter 11 digitos!"
        else:
            return 'PISPASEP não pode ser válidado, pois a entidade não é um funcionário!'

        return None


class ValidadorMatricula(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Funcionario):
            funcionario: Funcionario = entidade
            if funcionario._status.nome is None:
                return utils.ERRO_SALVAR_FUNCIONARIO_RNS.format(funcionario.nome) + " MATRICULA não pode ser nula!"

            try:
                int(entidade.matricula)
            except Exception:
                return utils.ERRO_SALVAR_FUNCIONARIO_RNS.format(funcionario.nome) + " MATRICULA deve conter apenas números inteiros!"

            if len(str(funcionario.matricula)) < 5:
                return utils.ERRO_SALVAR_FUNCIONARIO_RNS.format(funcionario.nome) + " MATRICULA deve conter no minimo 5 digitos!"

        else:
            return 'CPF não pode ser válidado, pois a entidade não é um funcionário!'

        return None


class ComplementarDtCadastro(AbstractStrategy):

    def processar(self, entidade):
        if entidade is not None:
            entidade.dataCadastro = datetime.datetime.now()
        else:
            return f'Entidade: {entidade.__class__.__name__.upper()} nula!'

        return None


class PreencherResponsavelCadastro(AbstractStrategy):

    def processar(self, entidade):
        if entidade is not None:
            entidade.responsavelCadastro = 'mc_siva'  # inserir o usuário logado aqui
        else:
            return f'Entidade: {entidade.__class__.__name__.upper()} nula!'

        return None


class ValidadorDadosObrigatoriosFuncionario(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Funcionario):
            f: Funcionario = entidade
            if not all([f._status.nome, f.cpf, f.nome, f.sexo, f.dataNascimento, f.pisPasep, f.rg, f.email, f.matricula,
                        f.dataAdmissao, f.cargo.nome, f.nomeUsuario, f.unidadeDeTrabalho, f.nomeUsuario,
                        f.senha, f.numeroCTPS, f.serieCTPS, f.ufCTPS, f.dataEmissaoCTPS, f._tipo_vinculo.nome]):
                return utils.ERRO_SALVAR_FUNCIONARIO_RNS.format(f.nome) + 'Todos os campos com (*) são obrigatórios e devem ser preenchidos'
        else:
            return utils.ERRO_SALVAR_FUNCIONARIO_RNS.format(f.nome) + " Deve ser registrado um funcionário!"
        return None


class ConversorUpperCaseFuncionario(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Funcionario):
            f: Funcionario = entidade
            f._status.nome = f._status.nome.upper() if f._status.nome is not None else None
            f.nome = f.nome.upper() if f.nome is not None else None
            f.lotacao = f.lotacao.upper() if f.lotacao is not None else None
            f.ufCTPS = f.ufCTPS.upper() if f.ufCTPS is not None else None
            f.unidadeDeTrabalho = f.unidadeDeTrabalho.upper() if f.unidadeDeTrabalho is not None else None
        return None
