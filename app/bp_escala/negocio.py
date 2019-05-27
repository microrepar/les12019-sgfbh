from les12019_core.abstract_strategy import AbstractStrategy
from les12019_core import utils
from app.bp_funcionario.models import Funcionario
from app.bp_funcionario.dao import FuncionarioDAO
from app.bp_escala.dao import EscalaDAO, JornadaDAO, TurnoDAO, StatusEscalaDAO, StatusHorarioDiarioDAO, StatusAtribuicaoDAO
from app.bp_escala.models import (Escala, Jornada, StatusEscala, StatusJornada, StatusHorarioDiario, StatusAtribuicao,
                                  HorarioDia, AtribuicaoEscala, Turno)
from flask import flash
from app import db
from sqlalchemy import and_, func
import datetime


dias_semana = [None, 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']


class ApensadorDependenciasSalvarAtualizarEscala(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Escala):
            escala: Escala = entidade
            
            lista_status_escala =  StatusEscalaDAO().listar(entidade.status)
            lista_jornadas = JornadaDAO().listar(entidade.jornada)
            lista_turnos = TurnoDAO().listar(entidade.turno)

            if len(lista_status_escala) < 1:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('StatusEscala'))

            if len(lista_jornadas) < 1:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('Jornada'))

            if len(lista_turnos) < 2:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('Turno'))


            escala._lista_status = lista_status_escala
            escala._lista_jornadas = lista_jornadas
            escala._lista_turnos = lista_turnos

        else:
            return 'Não pode ser cadastrado, pois o objeto não é uma escala!'


class ApensadorDependenciasSalvarAtualizarHorarioDia(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, HorarioDia):
            horario_diario: HorarioDia = entidade

            with db.session.no_autoflush:
                
                lista_status = StatusHorarioDiarioDAO().listar(entidade.status)
                
                escala = EscalaDAO().consultarPorId(entidade.escala)
                
                if escala is None:
                    flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Escala"'))

                if len(lista_status) < 1:
                    flash(utils.ERRO_CONSULTA_ENTIDADE.format('StatusHorarioDia'))

                horario_diario.escala = escala
                horario_diario._lista_status = lista_status
                horario_diario._dias_semana = dias_semana

                
        else:
            return 'Não pode ser cadastrado, pois o objeto não é um horário de trabalho diário!'


class ApensadorDependenciasSalvarAtualizarAtribuicao(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, AtribuicaoEscala):

            atribuicao_escala: AtribuicaoEscala = entidade
                                         
            escala = Escala.query.filter(Escala.id==entidade.escala.id).first()
            funcionario: Funcionario = Funcionario.query.filter(Funcionario.id==entidade.funcionario.id).first()
            status: StatusAtribuicao = StatusAtribuicao.query.filter_by(id=entidade.status.id).first()            

            if escala is not None:
                atribuicao_escala.escala = escala            
            
            if status is not None:
                atribuicao_escala.status = status            
            
            if funcionario is None:
                flash(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Funcionario'))
            else:                
                atribuicao_escala.funcionario = funcionario                
                
            lista_escalas = Escala.query.all()
            lista_status = StatusAtribuicao.query.all()

            atribuicao_escala._lista_escalas = lista_escalas
            atribuicao_escala._lista_status = lista_status

            if len(lista_escalas) < 1:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('Escala'))

            if len(lista_status) < 1:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('Status'))
                    
        else:
            return 'Não pode ser cadastrado, pois o objeto não é uma atribuição de escala!'


class ApensadorSalvarAtualizarJornadas(AbstractStrategy):

    def processar(self, entidade: Jornada):
        if isinstance(entidade, Jornada):

            jornada: Jornada = entidade

            lista_status = StatusJornada.query.all()

            jornada._lista_status = lista_status

            if len(lista_status) == 0:
                flash(utils.ERRO_CONSULTA_ENTIDADE.format('Status de jornadas'))
                
        else:
            'Não é possível salvar, porque o objeto não é uma instância de Jornada!'

        return None


class ValidadorDadosObrigatoriosJornada(AbstractStrategy):

    def processar(self, entidade: Jornada):
        if isinstance(entidade, Jornada):
            jornada: Jornada = entidade

            if not all([jornada.codigo, jornada.nome, jornada.carga_horaria, jornada.quantidade_minima_mpto, jornada.quantidade_maxima_dias,
                        jornada.intervalo_minimo, jornada.limite_max_horas_periodo, jornada.status.id, jornada.descricao]):
                return utils.ERRO_SALVAR_ENTIDADE_RNS.format('Todos os campos com (*) devem ser preenchidos corretamente!')
        else:
            'Não é possível salvar, porque o objeto não é uma instância de Jornada!'

        return None


class ComplementarDadosSalvarCadastroEscala(AbstractStrategy):

    def processar(self, entidade: Escala):
        if isinstance(entidade, Escala):
            escala: Escala = entidade

            escala.responsavel_cadastro = 'mcsilva'        

        else:
            return 'O objeto não pode ser cadastrado, pois não é uma instância de escala.'


class ComplementarDadosHorarioDia(AbstractStrategy):

    def processar(self, entidade: HorarioDia):
        if isinstance(entidade, HorarioDia):
            horario_dia: HorarioDia = entidade

            horario_dia.responsavel_cadastro = 'mcsilva'

        else:
            return 'O objeto não pode ser cadastrado, pois não é uma instância de HorarioDia.'


class ComplementarDadosAtribuicaoEscala(AbstractStrategy):

    def processar(self, entidade: AtribuicaoEscala):
        if isinstance(entidade, AtribuicaoEscala):
            atribuicao_escala: AtribuicaoEscala = entidade

            atribuicao_escala.responsavel_cadastro = 'mcsilva'

        else:
            return 'O objeto não pode ser cadastrado, pois não é uma instância de AtribuicaoEscala.'


class ValidadorCamposObrigatorios(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, Escala):
            escala: Escala= entidade

            if not all([escala.codigo, escala.nome, escala.descricao, escala.jornada.nome, escala.status.nome, escala.turno.nome]):
                return utils.ERRO_SALVAR_ENTIDADE_RNS.format('Todos os campos com * devem ser preenchidos!')

        else:
            return 'O objeto não é uma instância de escala'


class ValidadorCamposObrigatoriosHorarioDia(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, HorarioDia):
            horario_dia: HorarioDia= entidade

            if not all([horario_dia.dia_semana in dias_semana, horario_dia.status.id, horario_dia.descricao]):
                return utils.ERRO_SALVAR_ENTIDADE_RNS.format('Todos os campos com * devem ser preenchidos!')

        else:
            return 'O objeto não é uma instância de horario_dia'


class ValidadorHorarioPontos(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, HorarioDia):
            horario_dia: HorarioDia = entidade
            # Validar a quantidade de pontos lançados no cadastro com a quantidade mínima/máxima permitida pela jornada da escala            # 
            # Validar se a sequência dos pontos respeitam a ordem de hora_ponto1 até hora_pontoN (sem pontos vazios entre eles)
            # Validar tipo horário, isto é, se pode ser convertido para o tipo datetime
            # Validar se a hora posterior é maior que a anterior, se menor tranformar em virada do dia
            # Validar se o horario ponto_1 e do último ponto_n estão dentros do limete do turno\    
            # Validar se o total de horas somadas dos períodos atende os limites do requisitos de negócio.
            # Validar a quantidade de horas do período corresponde ao limite máximo de horas do perído definido na jornada
            # Validar o tempo mínimo do intervalo entre os períodos definido na jornada.
            
        else:
            pass


class PreparadorClonarHorarioDia(AbstractStrategy):
    
    def processar(self, entidade: HorarioDia):
        if isinstance(entidade, HorarioDia):
            clone_horario_dia: HorarioDia = entidade
            
            mensagens = []
            # Consultar por id as dependências para o objeto HorarioDia a ser clonado
            escala = Escala.query.filter_by(id=entidade.escala.id).first()
            status = StatusHorarioDiario.query.filter_by(nome='INATIVO').first()
            horario_dia: HorarioDia = HorarioDia.query.filter_by(id=entidade.id).first()

            if all([escala, status, horario_dia]):
                clone_horario_dia.status.id = status.id                
                clone_horario_dia.escala.id = escala.id
                clone_horario_dia.dia_semana = ''
                clone_horario_dia.hora_ponto1 = horario_dia.hora_ponto1
                clone_horario_dia.hora_ponto2 = horario_dia.hora_ponto2
                clone_horario_dia.hora_ponto3 = horario_dia.hora_ponto3
                clone_horario_dia.hora_ponto4 = horario_dia.hora_ponto4
                clone_horario_dia.responsavel_cadastro = 'clone_mcsilva'
                clone_horario_dia.descricao = horario_dia.descricao
            else:
                if horario_dia is None:
                    mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Horario do dia a ser clonado'))
                if escala is None:
                    mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format(f'Escala  do Horario do dia a ser clonado1'))
                if status is None:
                    mensagens.append(utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('Status do Horario do dia a ser clonado'))
                return '\n'.join(mensagens)
        else:
            return 'Não pode ser clonado, pois não é uma instância de HorarioDia.'


class ValidadorDiasSemanaDuplicados(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, HorarioDia):
            horario_dia: HorarioDia = entidade
            
            if entidade.id == '' or entidade.id is None:
                entidade.id = 0

            lista_dias_semana = db.session.query(HorarioDia.dia_semana).filter(
                and_(HorarioDia.escala_id == int(entidade.escala.id), HorarioDia.status_id == 1,
                     HorarioDia.id != int(entidade.id))).all()

            lista_dias_semana = [dia[0] for dia in lista_dias_semana]        

            if lista_dias_semana is not None:    
                if horario_dia.dia_semana in lista_dias_semana:
                    return f'Não é possível salvar ou atualizar horários, pois já tem um horário do dia da semana "{horario_dia.dia_semana}" cadastrado e ativo'
        else:
            return 'O objeto não é uma instância de HorarioDia.'
            

class ValidadorQuantidadeMaximaDiasSemana(AbstractStrategy):

    def processar(self, entidade):
        if isinstance(entidade, HorarioDia):
            escala: Escala = Escala.query.filter_by(id=entidade.escala.id).first()

            quantidade_dias_ativo = HorarioDia.query.filter(
                and_(HorarioDia.escala_id==entidade.escala_id, HorarioDia.status_id==entidade.status_id)).count()

            if escala is not None:
                quantidade_maxima_dias = escala.jornada.quantidade_maxima_dias
            else:
                return utils.ERRO_CONSULTA_POR_ID_ENTIDADE.format('"Escala"')

            if not quantidade_dias_ativo < quantidade_maxima_dias:
                return utils.ERRO_SALVAR_ENTIDADE_RNS.format(f'A Quantidade máxima permitida para esta escala é de ({quantidade_maxima_dias}) dias cadastrados ativos ')

        else:
            return 'O objeto não é uma instância de HorarioDia.'


