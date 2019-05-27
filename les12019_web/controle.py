"""Módulo controle - contém a classe Controladora para receber as requisições roteadas
"""
from flask import Request
from les12019_web.abstract_viewhelper import AbstractViewHelper 
from app.bp_funcionario.viewhelper import FuncionarioViewHelper
from app.bp_endereco.viewhelper import EnderecoViewHelper
from app.bp_escala.viewhelper import EscalaViewHelper, HorarioDiaViewHelper, AtribuicaoEscalaViewHelper, JornadaViewHelper
from app.bp_frequencia.viewhelper import EspelhoMensalViewHelper, EspelhoDiarioViewHelper
from app.bp_ponto.viewhelper import PontoViewHelper
from app.bp_ocorrencia.viewhelper import PendenciaViewHelper, OcorrenciaViewHelper
from app.bp_solicitacao.viewhelper import SolicitacaoViewHelper, DespachoViewHelper
from les12019_web.command import (
    AbstractCommand, SalvarCommand, ListarCommand, ConsultarCommand, ExcluirCommand, NoneCommand, AtualizarCommand,
    ConsultarPorIdCommand, PreOperacaoCommand, ConsultarPorParametro, ClonarCommand, IncluirCommand)

from les12019_core.aplicacao import Resultado


class Controle:
    """Recebe as requisições de todas as rotas estabelecidas e despacha para os objetos viewhelper e command
    
    Returns:
        [Template jinja2] -- template html renderizado com jinja2
    """
    def __init__(self):

        # Mapear os objetos viewhelper indexados pelo path da requisição
        self.vhs = {
            '/funcionarios': FuncionarioViewHelper(),
            '/atualizarFuncionario': FuncionarioViewHelper(), 
            '/cadastroDeFuncionario': FuncionarioViewHelper(),
            '/excluirCadastroFuncionario': FuncionarioViewHelper(),
            '/consultar_solicitacoes': FuncionarioViewHelper(),
            '/ocorrencias_funcionario': FuncionarioViewHelper(),
            '/cadastroDeEndereco': EnderecoViewHelper(),
            '/alteracaoDeEndereco': EnderecoViewHelper(),
            '/exclusaoDeEndereco': EnderecoViewHelper(),
            '/escalas': EscalaViewHelper(),
            '/cadastro_de_escala': EscalaViewHelper(),
            '/atualizar_escala': EscalaViewHelper(),
            '/excluir_escala': EscalaViewHelper(),
            '/cadastrar_horario': HorarioDiaViewHelper(),
            '/atualizar_horario': HorarioDiaViewHelper(),
            '/excluir_horario': HorarioDiaViewHelper(),
            '/salvar_atribuicao_escala': AtribuicaoEscalaViewHelper(),
            '/visualizar_atribuicao_escala': AtribuicaoEscalaViewHelper(),
            '/frequencias': FuncionarioViewHelper(),
            '/apontamento_frequencia_mensal': EspelhoMensalViewHelper(),
            '/visualizar_frequencia_funcionario': EspelhoMensalViewHelper(),
            '/frequencia_diaria': EspelhoDiarioViewHelper(),
            '/cadastrar_ponto': PontoViewHelper(),
            '/atualizar_ponto': PontoViewHelper(),
            '/excluir_ponto': PontoViewHelper(),
            '/pendencias': PendenciaViewHelper(),
            '/cadastrar_pendencia': PendenciaViewHelper(),
            '/atualizar_pendencia': PendenciaViewHelper(),
            '/excluir_pendencia': PendenciaViewHelper(),
            '/jornadas': JornadaViewHelper(),
            '/cadastrar_jornada': JornadaViewHelper(),
            '/atualizar_jornada': JornadaViewHelper(),
            '/excluir_jornada': JornadaViewHelper(),
            '/cadastrar_ocorrencia': OcorrenciaViewHelper(),
            '/atualizar_ocorrencia': OcorrenciaViewHelper(),
            '/excluir_ocorrencia': OcorrenciaViewHelper(),
            '/cadastrar_solicitacao': SolicitacaoViewHelper(),
            '/atualizar_solicitacao': SolicitacaoViewHelper(),
            '/excluir_solicitacao': SolicitacaoViewHelper(),
            '/cadastrar_despacho': DespachoViewHelper(),
        }
                        
        # Mapear os objetos command indexados pela operação da requisição
        self.commands = {
            None: ConsultarCommand(),
            'CONSULTAR': ConsultarCommand(),
            'CONSULTAR_ID': ConsultarPorIdCommand(),
            'PRE-ATUALIZAR': ConsultarPorIdCommand(),
            'ATUALIZAR': AtualizarCommand(),
            'PRE-SALVAR': PreOperacaoCommand(),
            'SALVAR': SalvarCommand(),
            'PRE-EXCLUIR': ConsultarPorIdCommand(),
            'EXCLUIR': ExcluirCommand(),
            'LISTAR': ListarCommand(),
            'FILTRAR': ConsultarPorParametro(),
            'PRE-VISUALIZAR': PreOperacaoCommand(),
            'VISUALIZAR': ConsultarPorIdCommand(),
            'CLONAR': ClonarCommand(),
            'APONTAR': ConsultarCommand(),
            'PRE-AVALIAR': PreOperacaoCommand(),
            'AVALIAR': ConsultarPorIdCommand(),
            'INCLUIR': IncluirCommand(),
        }

    def doProcessRequest(self, request: Request):

        # Normaliza a chamada dos dicionários de parâmetros get e post 
        if request.method == 'GET':
            parameters = request.args
        else:
            parameters = request.form
       
        # Atribui a uri (path) para recuperação da viewhelper indexada   
        uri: str = request.path

        # Recupera o objeto viewhelper do dicionário indexada pela uri
        vh: AbstractViewHelper = self.vhs.get(uri)

        # Executa o objeto viewhelper passando o objeto request da chamada
        entidade = vh.getEntidade(request)

        # Atribui à variável operacao, a operação realizada na requisição
        operacao: str = parameters.get('operacao')
        print('>>>> CONTROLE OPERACAO:', operacao)
        
        # Recupera o objeto command do dicionário indexado pela operação
        command: AbstractCommand = self.commands.get(operacao)
        
        print('>>>>', str(uri) + ':', vh.__class__.__name__, '->',
              entidade.__class__.__name__,'\n>>>>',
              str(operacao) + ':', command.__class__.__name__)

        # Executa o método execute do objeto command indexado pela operacao, devolvendo um objeto resultado
        resultado: Resultado= command.execute(entidade)

        # Renderiza a tela de respota da requisição do usuário
        return vh.setView(resultado, request)

ctrl = Controle()
