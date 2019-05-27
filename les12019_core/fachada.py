"""Módulo contendo a classe da implementação da fachada 
"""
from flask import flash, request
from collections.abc import Sequence
from les12019_core import utils
from les12019_core.aplicacao import Resultado
from les12019_core.abstract_dao import AbstractDAO
from les12019_core.abstract_fachada import AbstractFachada
from les12019_core.abstract_strategy import AbstractStrategy
from app.bp_funcionario.dao import FuncionarioDAO
from app.bp_endereco.dao import EnderecoDAO
from app.bp_escala.dao import EscalaDAO, HorarioDiaDAO, AtribuicaoEscalaDAO, JornadaDAO
from app.bp_frequencia.dao import EspelhoMensalDAO, EspelhoDiarioDAO
from app.bp_ponto.dao import PontoDAO
from app.bp_ocorrencia.dao import PendenciaDAO, OcorrenciaDAO
from app.bp_solicitacao.dao import SolicitacaoDAO, DespachoDAO
from app.bp_funcionario.negocio import (
    ValidadorCpf, ComplementarDtCadastro, ConversorUpperCaseFuncionario, PreencherResponsavelCadastro, 
    ValidadorMatricula, ValidadorPisPasep, ValidadorDadosObrigatoriosFuncionario, ApensadorDependeciasPreOperacaoSalvarFuncionarios)
from app.bp_endereco.negocio import (
    ApensadorDependeciasPreOperacaoSalvarEndereco, ValidadorCep, ValidadorTipoLogradouro, ValidadorNumeroEndereco, 
    PreencherResponsavelCadastroEndereco, ValidadorDadosObrigatoriosEndereco, VerificadorExistenciaEnderecoDuplicadoSalvar, 
    VerificadorExistenciaEnderecoDuplicadoAtualizar, VerificadorExitenciaEndereco)
from app.bp_escala.negocio import (
    ValidadorCamposObrigatorios, ApensadorDependenciasSalvarAtualizarEscala, ComplementarDadosSalvarCadastroEscala,
    ApensadorDependenciasSalvarAtualizarHorarioDia, ValidadorCamposObrigatoriosHorarioDia, ComplementarDadosHorarioDia,
    ApensadorDependenciasSalvarAtualizarAtribuicao, ComplementarDadosAtribuicaoEscala, PreparadorClonarHorarioDia,
    ValidadorDiasSemanaDuplicados, ValidadorQuantidadeMaximaDiasSemana, ApensadorSalvarAtualizarJornadas, ValidadorDadosObrigatoriosJornada)
from app.bp_frequencia.negocio import PreOperacaoFrequenciaMensal
from app.bp_ponto.negocio import (
    ApensadorPreOperacaoSalvarPonto, ValidadorDadosObrigatoriosPonto, ValidadorOpcaoIncluirPonto, VerificadorExistenciaExcluir)
from app.bp_ocorrencia.negocio import (
    ApensadorDadosSalvarAtualizarPendencia, ValidadorCamposObrigatoriosPendencia, VerificadorExitenciaPendencia,
    VerificadorHouveAlteracaoDadosPendencia, ApensadorDadosSalvarAtualizarOcorrencia, ValidadorDadosObrigatoriosOcorrencia,
    ComplementarDadosOcorrencia, ComplementarDadosPendencia)
from app.bp_solicitacao.negocio import (
    ApensadorDadosSalvarAtualizarSolicitacao, ValidadorDadosObrigatoriosSolicitacao, ValidadorDadosObrigatoriosDespacho,
    ApensadorDadosPreOperacaoSalvarAtualizarDespacho, ComplementarDadosSolicitacao, ComplementarDadosDespacho)

from typing import Dict, List
dict_daos = Dict[str, AbstractDAO]
list_strategies = List[AbstractStrategy]


class Fachada(AbstractFachada):

    def __init__(self):
        # Mapeamento das instancias da classe DAO
        self.daos: dict_daos = {
            'FUNCIONARIO': FuncionarioDAO(), 'ENDERECO': EnderecoDAO(),
            'ESCALA': EscalaDAO(), 'HORARIODIA': HorarioDiaDAO(), 'JORNADA': JornadaDAO(),
            'ATRIBUICAOESCALA': AtribuicaoEscalaDAO(), 'ESPELHOMENSAL': EspelhoMensalDAO(),
            'ESPELHODIARIO': EspelhoDiarioDAO(), 'PONTO': PontoDAO(), 'PENDENCIA': PendenciaDAO(),
            'OCORRENCIA': OcorrenciaDAO(), 'SOLICITACAO': SolicitacaoDAO(), 'DESPACHO': DespachoDAO(),
        }


        # TODO: Implentar as strategy e adicionar nas listas        
        self.rnsPreOperacaoEndereco = []
        self.rnsPreOperacaoEndereco.append(ApensadorDependeciasPreOperacaoSalvarEndereco())

        self.rnsSalvarEndereco = []
        self.rnsSalvarEndereco.append(ValidadorCep())
        self.rnsSalvarEndereco.append(ValidadorTipoLogradouro())
        self.rnsSalvarEndereco.append(ValidadorNumeroEndereco())
        self.rnsSalvarEndereco.append(PreencherResponsavelCadastroEndereco())
        self.rnsSalvarEndereco.append(ValidadorDadosObrigatoriosEndereco())
        self.rnsSalvarEndereco.append(VerificadorExistenciaEnderecoDuplicadoSalvar())

        self.rnsAtualizarEndereco = list()
        self.rnsAtualizarEndereco.append(ValidadorCep())
        self.rnsAtualizarEndereco.append(ValidadorTipoLogradouro())
        self.rnsAtualizarEndereco.append(ValidadorNumeroEndereco())
        self.rnsAtualizarEndereco.append(PreencherResponsavelCadastroEndereco())
        self.rnsAtualizarEndereco.append(ValidadorDadosObrigatoriosEndereco())
        self.rnsAtualizarEndereco.append(VerificadorExistenciaEnderecoDuplicadoAtualizar())

        self.rnsConsultarEndereco = []
        self.rnsConsultarEndereco.append(VerificadorExitenciaEndereco())
        
        self.rnsExcluirEndereco = []
        self.rnsExcluirEndereco.append(VerificadorExitenciaEndereco())
        
        # regras para entidade funcionario
        self.rnsPreOperacaoFuncionario = []
        self.rnsPreOperacaoFuncionario.append(ApensadorDependeciasPreOperacaoSalvarFuncionarios())

        self.rnsSalvarFuncionario = []
        self.rnsSalvarFuncionario.append(ValidadorCpf())
        self.rnsSalvarFuncionario.append(PreencherResponsavelCadastro())
        self.rnsSalvarFuncionario.append(ComplementarDtCadastro())
        self.rnsSalvarFuncionario.append(ValidadorMatricula())
        self.rnsSalvarFuncionario.append(ValidadorPisPasep())
        self.rnsSalvarFuncionario.append(ValidadorDadosObrigatoriosFuncionario())
        self.rnsSalvarFuncionario.append(ConversorUpperCaseFuncionario())
        
        self.rnsAtualizarFuncionario = []
        self.rnsAtualizarFuncionario.append(ValidadorCpf())
        self.rnsAtualizarFuncionario.append(ValidadorMatricula())
        self.rnsAtualizarFuncionario.append(ValidadorPisPasep())
        self.rnsAtualizarFuncionario.append(ValidadorDadosObrigatoriosFuncionario())
        self.rnsAtualizarFuncionario.append(ConversorUpperCaseFuncionario())
        

        # regras para entidade escala
        self.rnsPreOperacaoEscala = []
        self.rnsPreOperacaoEscala.append(ApensadorDependenciasSalvarAtualizarEscala())

        self.rnsSalvarEscala = []
        self.rnsSalvarEscala.append(ValidadorCamposObrigatorios())
        self.rnsSalvarEscala.append(ComplementarDadosSalvarCadastroEscala())

        self.rnsAtualizarEscala = []
        self.rnsAtualizarEscala.append(ApensadorDependenciasSalvarAtualizarEscala())
        
        # regras para entidade HorarioDia
        self.rnsPreoperacaoHorarioDia = []
        self.rnsPreoperacaoHorarioDia.append(ApensadorDependenciasSalvarAtualizarHorarioDia())
        
        self.rnsSalvarHorarioDia = []
        self.rnsSalvarHorarioDia.append(ValidadorCamposObrigatoriosHorarioDia())
        self.rnsSalvarHorarioDia.append(ComplementarDadosHorarioDia())
        self.rnsSalvarHorarioDia.append(ValidadorDiasSemanaDuplicados())
        self.rnsSalvarHorarioDia.append(ValidadorQuantidadeMaximaDiasSemana())

        self.rnsAtualizarHorarioDia = []
        self.rnsAtualizarHorarioDia.append(ComplementarDadosHorarioDia())
        self.rnsAtualizarHorarioDia.append(ValidadorCamposObrigatoriosHorarioDia())
        self.rnsAtualizarHorarioDia.append(ValidadorDiasSemanaDuplicados())
        self.rnsAtualizarHorarioDia.append(ValidadorQuantidadeMaximaDiasSemana())

        self.rnsClonarHorarioDia = []
        self.rnsClonarHorarioDia.append(PreparadorClonarHorarioDia())

        # regras para entidade AtribuicaoEscala
        self.rnsPreOpecacaoAtribuicaoEscala = []
        self.rnsPreOpecacaoAtribuicaoEscala.append(ApensadorDependenciasSalvarAtualizarAtribuicao())

        self.rnsSalvarAtribuicaoEscala = []
        self.rnsSalvarAtribuicaoEscala.append(ComplementarDadosAtribuicaoEscala())

        # regras para entidade Jornada
        self.rnsPreOperacaoJornada = []
        self.rnsPreOperacaoJornada.append(ApensadorSalvarAtualizarJornadas())

        self.rnsSalvarJornada = []
        self.rnsSalvarJornada.append(ApensadorSalvarAtualizarJornadas())
        self.rnsSalvarJornada.append(ValidadorDadosObrigatoriosJornada())

        self.rnsAtualizarJornada = []
        self.rnsAtualizarJornada.append(ApensadorSalvarAtualizarJornadas())

        # regras para entidade EspelhoMensal 
        self.rnsPreOperacaoEspelhoMensal = []
        self.rnsPreOperacaoEspelhoMensal.append(PreOperacaoFrequenciaMensal())

        # regras para entidades de Ponto
        self.rnsPreoperacaoPonto = []
        self.rnsPreoperacaoPonto.append(ApensadorPreOperacaoSalvarPonto())

        self.rnsSalvarPonto = []
        self.rnsSalvarPonto.append(ValidadorDadosObrigatoriosPonto())

        self.rnsAtualizarPonto = []
        self.rnsAtualizarPonto.append(ValidadorDadosObrigatoriosPonto())

        self.rnsOpcaoIncluirPonto = []
        self.rnsOpcaoIncluirPonto.append(ValidadorOpcaoIncluirPonto())

        self.rnsOpcaoExcluirPonto = []
        self.rnsOpcaoExcluirPonto.append(VerificadorExistenciaExcluir())

        # regras para entidade Pendencia
        self.rnsPreOperacaoPendencia = []
        self.rnsPreOperacaoPendencia.append(ApensadorDadosSalvarAtualizarPendencia())

        self.rnsSalvarPendencia = []
        self.rnsSalvarPendencia.append(ValidadorCamposObrigatoriosPendencia())
        self.rnsSalvarPendencia.append(VerificadorExitenciaPendencia())
        self.rnsSalvarPendencia.append(ComplementarDadosPendencia())
        
        self.rnsAtualizarPendencia = []
        self.rnsAtualizarPendencia.append(ValidadorCamposObrigatoriosPendencia())
        self.rnsAtualizarPendencia.append(VerificadorExitenciaPendencia())
        self.rnsAtualizarPendencia.append(VerificadorHouveAlteracaoDadosPendencia())

        # regras para entidade Ocorrencia
        self.rnsPreOperacaoOcorrencia = []
        self.rnsPreOperacaoOcorrencia.append(ApensadorDadosSalvarAtualizarOcorrencia())

        self.rnsSalvarOcorrencia = []
        self.rnsSalvarOcorrencia.append(ApensadorDadosSalvarAtualizarOcorrencia())
        self.rnsSalvarOcorrencia.append(ValidadorDadosObrigatoriosOcorrencia())
        self.rnsSalvarOcorrencia.append(ComplementarDadosOcorrencia())

        self.rnsAtualizarOcorrencia = []
        self.rnsAtualizarOcorrencia.append(ApensadorDadosSalvarAtualizarOcorrencia())
        self.rnsAtualizarOcorrencia.append(ValidadorDadosObrigatoriosOcorrencia())

        # regras para entidade Solicitacao
        self.rnsPreOperacaoSolicitacao = []
        self.rnsPreOperacaoSolicitacao.append(ApensadorDadosSalvarAtualizarSolicitacao())

        self.rnsSalvarSolicitacao = []
        self.rnsSalvarSolicitacao.append(ValidadorDadosObrigatoriosSolicitacao())
        self.rnsSalvarSolicitacao.append(ComplementarDadosSolicitacao())

        self.rnsAtualizarSolicitacao = []

        self.rnsExcluirSolicitacao = []

        # regras para entidade Despacho
        self.rnsPreOperacaoDespacho = []
        self.rnsPreOperacaoDespacho.append(ApensadorDadosPreOperacaoSalvarAtualizarDespacho())

        self.rnsSalvarDespacho = []
        self.rnsSalvarDespacho.append(ValidadorDadosObrigatoriosDespacho())
        self.rnsSalvarDespacho.append(ComplementarDadosDespacho())

        self.rnsAtualizarDespacho = []
        self.rnsAtualizarDespacho.append(ValidadorDadosObrigatoriosDespacho())

        self.rnsExcluirDespacho = []

        
        self.rnsEndereco = {
            'SALVAR': self.rnsSalvarEndereco, 'PRE-OPERACAO': self.rnsPreOperacaoEndereco,
            'ATUALIZAR': self.rnsAtualizarEndereco, 'CONSULTAR': self.rnsConsultarEndereco,
            'EXCLUIR': self.rnsExcluirEndereco,}
        
        self.rnsFuncionario = {
            'SALVAR': self.rnsSalvarFuncionario, 'ATUALIZAR': self.rnsAtualizarFuncionario,
            'PRE-OPERACAO': self.rnsPreOperacaoFuncionario,}

        self.rnsEscala = {
            'SALVAR': self.rnsSalvarEscala, 'ATUALIZAR': self.rnsAtualizarEscala,
            'PRE-OPERACAO': self.rnsPreOperacaoEscala,}

        self.rnsHorarioDia = {
            'PRE-OPERACAO': self.rnsPreoperacaoHorarioDia, 'SALVAR': self.rnsSalvarHorarioDia,
            'ATUALIZAR': self.rnsAtualizarHorarioDia, 'CLONAR': self.rnsClonarHorarioDia,}

        self.rnsAtribuicaoEscala = {
            'PRE-OPERACAO': self.rnsPreOpecacaoAtribuicaoEscala, 'SALVAR': self.rnsSalvarAtribuicaoEscala,}
        
        self.rnsJornada = {
            'PRE-OPERACAO': self.rnsPreOperacaoJornada, 'SALVAR': self.rnsSalvarJornada, 'ATUALIZAR': self.rnsAtualizarJornada,}

        self.rnsEspelhoMensal = {
            'PRE-OPERACAO': self.rnsPreOperacaoEspelhoMensal,
        }        

        self.rnsPonto = {
            'PRE-OPERACAO': self.rnsPreoperacaoPonto, 'SALVAR': self.rnsSalvarPonto,
            'ATUALIZAR': self.rnsAtualizarPonto, 'INCLUIR': self.rnsOpcaoIncluirPonto,
            'EXCLUIR': self.rnsOpcaoExcluirPonto,
        }

        self.rnsPendencia = {
            'PRE-OPERACAO': self.rnsPreOperacaoPendencia, 'SALVAR': self.rnsSalvarPendencia,
            'ATUALIZAR': self.rnsAtualizarPendencia,
        }

        self.rnsOcorrencia = {
            'PRE-OPERACAO': self.rnsPreOperacaoOcorrencia, 'SALVAR': self.rnsSalvarOcorrencia,
            'ATUALIZAR': self.rnsAtualizarOcorrencia,
        }

        self.rnsSolicitacao = {
            'PRE-OPERACAO': self.rnsPreOperacaoSolicitacao, 'SALVAR': self.rnsSalvarSolicitacao,
            'ATUALIZAR': self.rnsAtualizarSolicitacao, 'EXCLUIR': self.rnsExcluirSolicitacao,
        }

        self.rnsDespacho = {
            'PRE-OPERACAO': self.rnsPreOperacaoDespacho, 'SALVAR': self.rnsSalvarDespacho,
            'ATUALIZAR': self.rnsAtualizarDespacho, 'EXCLUIR': self.rnsExcluirDespacho
        }
        

        self.rns = {
            'FUNCIONARIO': self.rnsFuncionario, 'ENDERECO': self.rnsEndereco, 'ESCALA': self.rnsEscala,
            'HORARIODIA': self.rnsHorarioDia, 'ATRIBUICAOESCALA': self.rnsAtribuicaoEscala,
            'ESPELHOMENSAL': self.rnsEspelhoMensal, 'PONTO': self.rnsPonto, 'PENDENCIA': self.rnsPendencia,
            'JORNADA': self.rnsJornada, 'OCORRENCIA': self.rnsOcorrencia, 'SOLICITACAO': self.rnsSolicitacao,
            'DESPACHO': self.rnsDespacho,
        }
           

    def salvar(self, entidade):
        resultado = Resultado()
        class_name = entidade.__class__.__name__.upper()

        resultado.msg = self._executarRegras(entidade, 'SALVAR')

        if resultado.qtde_msg() == 0:
            dao: AbstractDAO= self.daos.get(class_name)
            respostaDao = dao.salvar(entidade)
            if not isinstance(respostaDao, str):
                resultado.msg = self._executarRegras(respostaDao, 'PRE-OPERACAO')
                resultado.entidades = respostaDao
                return resultado
            else:
                resultado.msg = self._executarRegras(entidade, 'PRE-OPERACAO')
                resultado.msg = respostaDao
                resultado.entidades = entidade
                return resultado
        else:
            resultado.msg = self._executarRegras(entidade, 'PRE-OPERACAO')
            resultado.entidades = entidade
            return resultado


    def atualizar(self, entidade):
        resultado = Resultado()
        class_name = entidade.__class__.__name__.upper()

        resultado.msg = self._executarRegras(entidade, 'ATUALIZAR')

        if resultado.qtde_msg() == 0:
            dao: AbstractDAO= self.daos.get(class_name)
            respostaDao = dao.alterar(entidade)
            if not isinstance(respostaDao, str):
                resultado.msg = self._executarRegras(respostaDao, 'PRE-OPERACAO')
                resultado.entidades = respostaDao
                return resultado
            else:
                resultado.msg = self._executarRegras(entidade, 'PRE-OPERACAO')
                resultado.msg = respostaDao
                resultado.entidades = entidade
                return resultado
        else:
            resultado.msg = self._executarRegras(entidade, 'PRE-OPERACAO')
            resultado.entidades = entidade
            return resultado


    def consultar(self, entidade):
        resultado = Resultado()
        class_name = entidade.__class__.__name__.upper()
        dao: AbstractDAO = self.daos.get(class_name)
        resultado.entidades = dao.consultar(entidade)
        return resultado


    def consultarPorId(self, entidade):
        resultado = Resultado()
        class_name = entidade.__class__.__name__.upper()
        
        resultado.msg = self._executarRegras(entidade, 'CONSULTAR')

        if resultado.qtde_msg() == 0:
            dao: AbstractDAO = self.daos.get(class_name)
            respostaDao = dao.consultarPorId(entidade)
            if isinstance(respostaDao, str):
                resultado.entidades = entidade
                resultado.msg = self._executarRegras(entidade, 'PRE-OPERACAO')
                resultado.msg = respostaDao
                return resultado
            else:
                resultado.msg = self._executarRegras(respostaDao, 'PRE-OPERACAO')
                resultado.entidades = respostaDao
                return resultado
        else:
            resultado.msg = self._executarRegras(respostaDao, 'PRE-OPERACAO')
            resultado.entidades = respostaDao
            return resultado


    def consultarPorParametro(self, entidade):
        resultado = Resultado()
        class_name = entidade.__class__.__name__.upper()
        dao: AbstractDAO = self.daos.get(class_name)
        respostaDao = dao.consultarPorParametro(entidade)
        if isinstance(respostaDao, str):
            resultado.msg = respostaDao
            return resultado
        else:
            resultado.entidades = respostaDao
            return resultado


    def listar(self, entidade):
        resultado = Resultado()
        class_name: str = entidade.__class__.__name__.upper()
        dao: AbstractDAO= self.daos.get(class_name)
        respostaDao = dao.listar(entidade)
        if isinstance(respostaDao, str):
            resultado.msg = respostaDao
            return resultado
        else:
            resultado.entidades = respostaDao
            return resultado


    def excluir(self, entidade):
        resultado = Resultado()
        class_name = entidade.__class__.__name__.upper()

        resultado.msg = self._executarRegras(entidade, 'EXCLUIR')

        if resultado.qtde_msg() == 0:
            dao: AbstractDAO = self.daos.get(class_name)
            respostaDao = dao.excluir(entidade)
            if not isinstance(respostaDao, str):
                resultado.entidades = entidade                
                return resultado
            else:
                resultado.entidades = entidade
                resultado.msg = respostaDao
                return resultado
        else:
            resultado.entidades = entidade
            return resultado


    
    def preOperacao(self, entidade):
        resultado = Resultado()

        resultado.msg = self._executarRegras(entidade, 'PRE-OPERACAO')

        resultado.entidades = entidade
        return resultado

    
    def clonar(self, entidade):
        resultado = Resultado()
        class_name = entidade.__class__.__name__.upper()
        
        resultado.msg = self._executarRegras(entidade, 'CLONAR')

        if resultado.qtde_msg() == 0:
            dao: AbstractDAO = self.daos.get(class_name)
            respostaDao = dao.salvar(entidade)
            if not isinstance(respostaDao, str):
                resultado.entidades = respostaDao
                return resultado
            else:
                resultado.entidades = entidade
                return resultado
        else:
            resultado.entidades = entidade
            return resultado


    def incluir(self, entidade):
        resultado = Resultado()

        resultado.msg = self._executarRegras(entidade, 'INCLUIR')

        resultado.entidades = entidade
        return resultado


    def _executarRegras(self, entidade , operacao: str) -> str:
        
        class_name = entidade.__class__.__name__.upper()
        
        regrasOperacao = self.rns.get(class_name)

        msg = list()

        if regrasOperacao is not None:
            regras:list_strategies = regrasOperacao.get(operacao)

            if isinstance(regras, Sequence):
                for regra in regras:
                    
                    m = regra.processar(entidade)
                    if m is not None:
                        if isinstance(m , str):
                            msg.append(m)
                        elif isinstance(m , Sequence):
                            msg += list(m)
        if len(msg) > 0:
            return msg
        else:
            return None

        return None
