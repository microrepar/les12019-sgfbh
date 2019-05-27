from les12019_core.abstract_strategy import AbstractStrategy
from les12019_core import utils
from app.bp_frequencia.models import EspelhoMensal, EspelhoDiario, StatusEspelho
from app.bp_funcionario.models import Funcionario
from app import db

from sqlalchemy import and_
import datetime

_formato_data = '%d/%m/%Y'
_meses_do_ano = [(1, 'Janeiro'), (2, 'Fevereiro'), (3, 'Março'), (4, 'Abril'), (5, 'Maio'), (6, 'Junho'), 
    (7, 'Julho'), (8, 'Agosto'), (9, 'Setembro'), (10, 'Outubro'), (11, 'Novembro'), (12, 'Dezembro')]


class PreOperacaoFrequenciaMensal(AbstractStrategy):
    """Cria as instâncias de espelho diário e insere no espelho mensal quando ainda não existe a folha do referido mês
    
    Arguments:
        AbstractStrategy {entidadeDominio} -- Instancia do objeto entidade do dominio 
    
    Returns:
        None -- se não houver erros nas regras de negócio   
        str -- se houver erro na execução das regras de negócio
    """
    def processar(self, entidade):
        if isinstance(entidade, EspelhoMensal):
            
            espelho_mensal: EspelhoMensal = entidade

            # data atual
            hoje = datetime.datetime.now()
            um_dia = datetime.timedelta(days=1)

            # verifica se o ano e mês de referencia da espelho de ponto mensal estão preenchidos:
            if all([espelho_mensal.mes_referencia, espelho_mensal.ano_referencia]):

                try:
                    mes_atual = int(espelho_mensal.mes_referencia)
                    ano_atual = int(espelho_mensal.ano_referencia)                    
                except TypeError as e:
                    print(str(e))
                    return utils.ERRO_EXECUTAR_RNS.format('Somente números inteiros são permitidos no campo ano de referência!')

            else:                
                mes_atual = hoje.month
                ano_atual = hoje.year
            
            mes_anterior = mes_atual - 1 if mes_atual > 1 else 12
            ano_mes_anterior = ano_atual -1 if mes_anterior == 12 else ano_atual

            funcionario = Funcionario.query.filter_by(id=entidade.funcionario.id).first()
            if funcionario is None:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Funcionario')

            status = StatusEspelho.query.filter_by(id=1).first()
            if status is None:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status de espelhos de ponto')

            espelho_mensal = EspelhoMensal.query.filter(
                and_(EspelhoMensal.mes_referencia==mes_atual, EspelhoMensal.ano_referencia==ano_atual, 
                EspelhoMensal.funcionario_id==funcionario.id)).first()

            if espelho_mensal is None:
                espelho_mensal = EspelhoMensal(responsavel_cadastro='sistema')
                espelho_mensal.mes_referencia = mes_atual
                espelho_mensal.ano_referencia = ano_atual
                espelho_mensal.data_inicio = datetime.datetime.strptime(f'16/{mes_anterior}/{ano_mes_anterior:0>2}', _formato_data) 
                espelho_mensal.data_fim = datetime.datetime.strptime(f'15/{mes_atual}/{ano_atual}', _formato_data) 
                
                espelho_mensal.funcionario = funcionario
                espelho_mensal.status = status

                dia_frequencia_atual: datetime.datetime = espelho_mensal.data_inicio

                while dia_frequencia_atual <= espelho_mensal.data_fim:
                    print('>>>>>>>>>>>>>ESPELHO DIARIO>>>>>>>>>>>>>', dia_frequencia_atual, espelho_mensal.data_fim)
                    espelho_dia = EspelhoDiario(data_cadastro=hoje, responsavel_cadastro='sistema')
                    espelho_dia.data = dia_frequencia_atual
                    espelho_dia.autopreencher_dados_data()
                    espelho_dia.observacao = 'teste'
                    
                    espelho_dia.status = status
                    espelho_dia.funcionario = funcionario
                    
                    espelho_mensal.espelhos_diarios.append(espelho_dia)

                    dia_frequencia_atual += um_dia

                db.session.commit()
                entidade.id = espelho_mensal.id
            else:
                entidade.id = espelho_mensal.id

            entidade._meses_do_ano = _meses_do_ano

        else:
            'O objeto não é uma instância de espelho de ponto diario!'
        

class _Strategy(AbstractStrategy):
    def processar(self, entidade):
        pass
