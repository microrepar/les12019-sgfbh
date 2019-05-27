from les12019_web.abstract_viewhelper import AbstractViewHelper, _verificar_msg
from app.bp_escala.models import (
    Jornada, Escala, Turno, HorarioDia, AtribuicaoEscala, StatusEscala, StatusAtribuicao, StatusJornada, StatusHorarioDiario)
from app.bp_funcionario.models import Funcionario
from flask import Request, render_template, redirect, url_for, make_response, Response, session
from les12019_core.utils import get_parameters_request
from les12019_core.aplicacao import ConverteData
from app import db



#################################################################################################

class EscalaViewHelper(AbstractViewHelper):

    def getEntidade(self, request: Request):
        escala = Escala(nome='', codigo='', descricao='', responsavel_cadastro='')
        escala.status = StatusEscala()
        escala.jornada = Jornada(carga_horaria='')
        escala.turno = Turno()
        

        parameters = get_parameters_request(request)

        operacao  = parameters.get('operacao')


        if operacao != 'LISTAR' and operacao is not None:

            if operacao == 'PRE-CADASTRAR':
                codigo = parameters.get('txt-escala-codigo', '').strip()
                nome = parameters.get('txt-escala-nome', '').strip()
                descricao = parameters.get('txt-escala-descricao', '').strip()

                turno_nome = parameters.get('txt-escala-turno', '').strip()
                status_nome = parameters.get('txt-escala-status', '').strip()
                jornada_nome = parameters.get('txt-escala-jornada', '').strip()

                escala.codigo = codigo
                escala.nome = nome
                escala.descricao = descricao

                escala.turno.nome = turno_nome
                escala.status.nome = status_nome
                escala.jornada.nome = jornada_nome
            
            elif operacao == 'SALVAR':
                codigo = parameters.get('txt-escala-codigo', '').strip()
                nome = parameters.get('txt-escala-nome', '').strip()
                descricao = parameters.get('txt-escala-descricao', '').strip()

                turno_nome = parameters.get('txt-escala-turno', '').strip()
                status_nome = parameters.get('txt-escala-status', '').strip()
                jornada_nome = parameters.get('txt-escala-jornada', '').strip()

                escala.codigo = codigo
                escala.nome = nome
                escala.descricao = descricao
                
                escala.turno.nome = turno_nome
                escala.status.nome = status_nome
                escala.jornada.nome = jornada_nome

            elif operacao == 'PRE-ATUALIZAR':                
                escala_id = parameters.get('txt_escala_id', session.get('txt_escala_id', '')).strip()
                session['txt_escala_id'] = escala_id

                turno_id = parameters.get('txt-escala-turno', '').strip()
                status_id = parameters.get('txt-escala-status', '').strip()
                jornada_id = parameters.get('txt-escala-jornada', '').strip()

                codigo = parameters.get('txt-escala-codigo', '').strip()
                nome = parameters.get('txt-escala-nome', '').strip()
                descricao = parameters.get('txt-escala-descricao', '').strip()
                data_cadastro = parameters.get('txt-escala-data_cadastro','').strip()
                responsavel_cadastro = parameters.get('txt-escala-responsavel_cadastro','').strip()

                turno_nome = parameters.get('txt-escala-turno', '').strip()
                status_nome = parameters.get('txt-escala-status', '').strip()
                jornada_nome = parameters.get('txt-escala-jornada', '').strip()

                escala.id = escala_id

                escala.status_id = status_id
                escala.status.id = status_id

                escala.turno_id = turno_id
                escala.turno.id = turno_id

                escala.jornada_id = jornada_id
                escala.jornada.id = jornada_id

                escala.codigo = codigo
                escala.nome = nome
                escala.descricao = descricao
                escala.data_cadastro = ConverteData.stringDate(data_cadastro)
                escala.responsavel_cadastro = responsavel_cadastro

                escala.turno.nome = turno_nome
                escala.status.nome = status_nome
                escala.jornada.nome = jornada_nome

            elif operacao == 'ATUALIZAR':
                escala_id = parameters.get('txt_escala_id', '').strip()

                turno_id = parameters.get('txt-escala-turno', '').strip()
                status_id = parameters.get('txt-escala-status', '').strip()
                jornada_id = parameters.get('txt-escala-jornada', '').strip()

                codigo = parameters.get('txt-escala-codigo', '').strip()
                nome = parameters.get('txt-escala-nome', '').strip()
                descricao = parameters.get('txt-escala-descricao', '').strip()
                data_cadastro = parameters.get('txt-escala-data_cadastro','').strip()
                responsavel_cadastro = parameters.get('txt-escala-responsavel_cadastro','').strip()

                turno_nome = parameters.get('txt-escala-turno', '').strip()
                status_nome = parameters.get('txt-escala-status', '').strip()
                jornada_nome = parameters.get('txt-escala-jornada', '').strip()

                escala.id = escala_id

                escala.status_id = status_id
                escala.status.id = status_id

                escala.turno_id = turno_id
                escala.turno.id = turno_id

                escala.jornada_id = jornada_id
                escala.jornada.id = jornada_id

                escala.codigo = codigo
                escala.nome = nome
                escala.descricao = descricao
                escala.data_cadastro = ConverteData.stringDate(data_cadastro)
                escala.responsavel_cadastro = responsavel_cadastro

                escala.turno.nome = turno_nome
                escala.status.nome = status_nome
                escala.jornada.nome = jornada_nome

            elif operacao == 'PRE-EXCLUIR':
                escala_id = parameters.get('txt_escala_id', '').strip()
                escala.id = escala_id

            elif operacao == 'EXCLUIR':
                escala_id = parameters.get('txt_escala_id', '').strip()
                escala.id = escala_id
            

        return escala


    def setView(self, resultado, request):
        
        parameters = get_parameters_request(request)

        operacao  = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            
            if operacao == 'PRE-SALVAR':
                _verificar_msg(resultado)
                return render_template('escala/cadastro_de_escala.html', resultado=resultado)

            elif operacao == 'SALVAR':
                if _verificar_msg(resultado):
                    return render_template('escala/cadastro_de_escala.html', resultado=resultado)
                else:
                    return render_template('escala/atualizar_escala.html', resultado=resultado)
            
            elif operacao == 'PRE-ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('escala/atualizar_escala.html', resultado=resultado)
                else:
                    return render_template('escala/atualizar_escala.html', resultado=resultado)
            
            elif operacao == 'ATUALIZAR':
                _verificar_msg(resultado)
                return render_template('escala/atualizar_escala.html', resultado=resultado)

            elif operacao == 'PRE-EXCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_escala.escalas'))
                else:
                    return render_template('escala/excluir_escala.html', resultado=resultado)

            elif operacao == 'EXCLUIR':
                _verificar_msg(resultado)
                return redirect(url_for('bp_escala.escalas'))

        else:
            _verificar_msg(resultado)
            return render_template('escala/escalas.html', resultado=resultado )

        return f'OPERACAO="{operacao}" NOT IMPLEMENTED'



#################################################################################################
class HorarioDiaViewHelper(AbstractViewHelper):

    def getEntidade(self, request):
        
        horario_trabalho = HorarioDia()
        horario_trabalho.escala = Escala()
        horario_trabalho.status = StatusHorarioDiario()
        

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            
            if operacao == 'PRE-SALVAR':
                horario_trabalho_id = parameters.get('txt_horario_trabalho_diario_id', '').strip()
                escala_id = parameters.get('txt_escala_id', '').strip()
                status_id = parameters.get('txt-horario-trabalho-status_id','').strip()

                dia_semana = parameters.get('txt-horario-trabalho-dia_semana', '').strip()
                hora_ponto1 = parameters.get('txt-horario-trabalho-horario_1', '').strip()
                hora_ponto2 = parameters.get('txt-horario-trabalho-horario_2', '').strip()
                hora_ponto3 = parameters.get('txt-horario-trabalho-horario_3', '').strip()
                hora_ponto4 = parameters.get('txt-horario-trabalho-horario_4', '').strip()
                descricao = parameters.get('txt-horario-trabalho-descricao', '').strip()

                horario_trabalho.id = horario_trabalho_id

                horario_trabalho.escala_id = escala_id
                horario_trabalho.escala.id = escala_id

                horario_trabalho.status_id = status_id
                horario_trabalho.status.id = status_id

                horario_trabalho.dia_semana = dia_semana
                horario_trabalho.hora_ponto1 = hora_ponto1
                horario_trabalho.hora_ponto2 = hora_ponto2
                horario_trabalho.hora_ponto3 = hora_ponto3
                horario_trabalho.hora_ponto4 = hora_ponto4
                horario_trabalho.descricao = descricao


            elif operacao == 'SALVAR':
                horario_trabalho_id = parameters.get('txt_horario_trabalho_diario_id', '').strip()
                escala_id = parameters.get('txt_escala_id', '').strip()
                status_id = parameters.get('txt-horario-trabalho-status_id','').strip()

                dia_semana = parameters.get('txt-horario-trabalho-dia_semana', '').strip()
                hora_ponto1 = parameters.get('txt-horario-trabalho-horario_1', '').strip()
                hora_ponto2 = parameters.get('txt-horario-trabalho-horario_2', '').strip()
                hora_ponto3 = parameters.get('txt-horario-trabalho-horario_3', '').strip()
                hora_ponto4 = parameters.get('txt-horario-trabalho-horario_4', '').strip()
                descricao = parameters.get('txt-horario-trabalho-descricao', '').strip()

                horario_trabalho.id = horario_trabalho_id

                horario_trabalho.escala_id = escala_id
                horario_trabalho.escala.id = escala_id

                horario_trabalho.status_id = status_id
                horario_trabalho.status.id = status_id

                horario_trabalho.dia_semana = dia_semana
                horario_trabalho.hora_ponto1 = hora_ponto1
                horario_trabalho.hora_ponto2 = hora_ponto2
                horario_trabalho.hora_ponto3 = hora_ponto3
                horario_trabalho.hora_ponto4 = hora_ponto4
                horario_trabalho.descricao = descricao

            elif operacao == 'PRE-ATUALIZAR':
                horario_trabalho_id = parameters.get('txt_horario_trabalho_diario_id', '').strip()
                escala_id = parameters.get('txt_escala_id', '').strip()
                status_id = parameters.get('txt-horario-trabalho-status_id','').strip()

                dia_semana = parameters.get('txt-horario-trabalho-dia_semana', '').strip()
                hora_ponto1 = parameters.get('txt-horario-trabalho-horario_1', '').strip()
                hora_ponto2 = parameters.get('txt-horario-trabalho-horario_2', '').strip()
                hora_ponto3 = parameters.get('txt-horario-trabalho-horario_3', '').strip()
                hora_ponto4 = parameters.get('txt-horario-trabalho-horario_4', '').strip()
                descricao = parameters.get('txt-horario-trabalho-descricao', '').strip()

                horario_trabalho.id = horario_trabalho_id

                horario_trabalho.escala_id = escala_id
                horario_trabalho.escala.id = escala_id

                horario_trabalho.status_id = status_id
                horario_trabalho.status.id = status_id

                horario_trabalho.dia_semana = dia_semana
                horario_trabalho.hora_ponto1 = hora_ponto1
                horario_trabalho.hora_ponto2 = hora_ponto2
                horario_trabalho.hora_ponto3 = hora_ponto3
                horario_trabalho.hora_ponto4 = hora_ponto4
                horario_trabalho.descricao = descricao

            elif operacao == 'ATUALIZAR':
                horario_trabalho_id = parameters.get('txt_horario_trabalho_diario_id', '').strip()
                escala_id = parameters.get('txt_escala_id', '').strip()
                status_id = parameters.get('txt-horario-trabalho-status_id','').strip()

                dia_semana = parameters.get('txt-horario-trabalho-dia_semana', '').strip()
                hora_ponto1 = parameters.get('txt-horario-trabalho-horario_1', '').strip()
                hora_ponto2 = parameters.get('txt-horario-trabalho-horario_2', '').strip()
                hora_ponto3 = parameters.get('txt-horario-trabalho-horario_3', '').strip()
                hora_ponto4 = parameters.get('txt-horario-trabalho-horario_4', '').strip()
                descricao = parameters.get('txt-horario-trabalho-descricao', '').strip()
                

                horario_trabalho.id = horario_trabalho_id

                horario_trabalho.escala_id = escala_id
                horario_trabalho.escala.id = escala_id

                horario_trabalho.status_id = status_id
                horario_trabalho.status.id = status_id

                horario_trabalho.dia_semana = dia_semana
                horario_trabalho.hora_ponto1 = hora_ponto1
                horario_trabalho.hora_ponto2 = hora_ponto2
                horario_trabalho.hora_ponto3 = hora_ponto3
                horario_trabalho.hora_ponto4 = hora_ponto4
                horario_trabalho.descricao = descricao

            elif operacao == 'PRE-EXCLUIR':
                horario_trabalho_id = parameters.get('txt_horario_trabalho_diario_id', '').strip()
                escala_id = parameters.get('txt_escala_id', '').strip()
                status_id = parameters.get('txt-horario-trabalho-status_id','').strip()

                horario_trabalho.id = horario_trabalho_id

                horario_trabalho.escala_id = escala_id
                horario_trabalho.escala.id = escala_id

                horario_trabalho.status_id = status_id
                horario_trabalho.status.id = status_id

            elif operacao == 'EXCLUIR':
                horario_trabalho_id = parameters.get('txt_horario_trabalho_diario_id', '').strip()
                escala_id = parameters.get('txt_escala_id', '').strip()
                status_id = parameters.get('txt-horario-trabalho-status_id','').strip()

                horario_trabalho.id = horario_trabalho_id

                horario_trabalho.escala_id = escala_id
                horario_trabalho.escala.id = escala_id

                horario_trabalho.status_id = status_id
                horario_trabalho.status.id = status_id

            elif operacao == 'CLONAR':
                horario_trabalho_id = parameters.get('txt_horario_trabalho_diario_id', '').strip()
                escala_id = parameters.get('txt_escala_id', '').strip()

                horario_trabalho.id = horario_trabalho_id

                horario_trabalho.escala_id = escala_id
                horario_trabalho.escala.id = escala_id

                print('>>>>>>>>>CLONAR>>>>>>>>>>',horario_trabalho_id, escala_id)


        return horario_trabalho


    def setView(self, resultado, request):
        
        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            
            if operacao == 'PRE-SALVAR':
                _verificar_msg(resultado)
                return render_template('escala/cadastrar_horario.html', resultado=resultado)

            elif operacao == 'SALVAR':
                if _verificar_msg(resultado):
                    return render_template('escala/cadastrar_horario.html', resultado=resultado)
                else:
                    return render_template('escala/atualizar_escala.html', resultado=resultado)

            elif operacao == 'PRE-ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('escala/atualizar_horario.html', resultado=resultado)
                else:
                    return render_template('escala/atualizar_horario.html', resultado=resultado)
            
            elif operacao == 'ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('escala/atualizar_horario.html', resultado=resultado)
                else:
                    return render_template('escala/atualizar_horario.html', resultado=resultado)

            elif operacao == 'PRE-EXCLUIR':
                if _verificar_msg(resultado):
                    return render_template('escala/excluir_horario.html', resultado=resultado)
                else:
                    return render_template('escala/excluir_horario.html', resultado=resultado)
            
            elif operacao == 'EXCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_escala.atualizar_escala', operacao='PRE-ATUALIZAR') + '#id-titulo-horarios')
                else:
                    return redirect(url_for('bp_escala.atualizar_escala', operacao='PRE-ATUALIZAR') + '#id-titulo-horarios')

            elif operacao == 'CLONAR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_escala.atualizar_escala', operacao='PRE-ATUALIZAR') + '#id-titulo-horarios')
                else: 
                    return redirect(url_for('bp_escala.atualizar_escala', operacao='PRE-ATUALIZAR') + '#id-titulo-horarios')


        else:
            _verificar_msg(resultado)
            return render_template('escala/cadastrar_horario.html', resultado=resultado)

        return f'OPERACAO={operacao} NO_IMPLEMENTED'


class AtribuicaoEscalaViewHelper(AbstractViewHelper):

    def getEntidade(self, request):
       
        atribuicao_escala = AtribuicaoEscala(observacao='')
        atribuicao_escala.status = StatusAtribuicao()
        atribuicao_escala.funcionario = Funcionario()
        atribuicao_escala.escala = Escala(
            codigo='', nome='', responsavel_cadastro='', descricao='')

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':
                atribuicao_escala_id = parameters.get('txt-atribuicao-status', '').strip()
                status_id = parameters.get('txt-atribuicao-status', '').strip()
                # funcionario_id = parameters.get('txt_funcionario_id', '').strip()
                funcionario_id = session.get('funcionario_id')
                escala_id = parameters.get('txt-atribuicao-escala-id', '').strip()

                funcionario_matricula = parameters.get('txt-funcionario-matricula','').strip()
                funcionario_nome = parameters.get('txt-funcionario-nome', '').strip()
                
                data_inicio = parameters.get('text-atribuicao-data-inicio', '').strip()
                data_fim = parameters.get('text-atribuicao-data-fim', '').strip()
                data_cadastro = parameters.get('txt-escala-data_cadastro', '').strip()
                responsavel_cadastro = parameters.get('txt-escala-responsavel_cadastro', '').strip()
                observacao = parameters.get('txt-atribuicao-escala-observacao', '').strip()


                atribuicao_escala.id = atribuicao_escala_id

                atribuicao_escala.funcionario_id = funcionario_id
                atribuicao_escala.funcionario.id = funcionario_id

                atribuicao_escala.escala_id = escala_id
                atribuicao_escala.escala.id = escala_id

                atribuicao_escala.status_id = status_id
                atribuicao_escala.status.id = status_id

                atribuicao_escala.funcionario.matricula = funcionario_matricula
                atribuicao_escala.funcionario.nome = funcionario_nome

                atribuicao_escala.data_inicio = ConverteData.stringDate(data_inicio)
                atribuicao_escala.data_fim = ConverteData.stringDate(data_fim)
                atribuicao_escala.data_cadastro = ConverteData.stringDate(data_cadastro)
                atribuicao_escala.responsavel_cadastro = responsavel_cadastro
                atribuicao_escala.observacao = observacao

            elif operacao == 'SALVAR':
                atribuicao_escala_id = parameters.get('txt-atribuicao-status', '').strip()
                status_id = parameters.get('txt-atribuicao-status', '').strip()
                # funcionario_id = parameters.get('txt_funcionario_id', '').strip()
                funcionario_id = session.get('funcionario_id')
                escala_id = parameters.get('txt-atribuicao-escala-id', '').strip()

                funcionario_matricula = parameters.get('txt-funcionario-matricula','').strip()
                funcionario_nome = parameters.get('txt-funcionario-nome', '').strip()
                
                data_inicio = parameters.get('text-atribuicao-data-inicio', '').strip()
                data_fim = parameters.get('text-atribuicao-data-fim', '').strip()
                data_cadastro = parameters.get('txt-escala-data_cadastro', '').strip()
                responsavel_cadastro = parameters.get('txt-escala-responsavel_cadastro', '').strip()
                observacao = parameters.get('txt-atribuicao-escala-observacao', '').strip()


                atribuicao_escala.id = atribuicao_escala_id

                atribuicao_escala.funcionario_id = funcionario_id
                atribuicao_escala.funcionario.id = funcionario_id

                atribuicao_escala.escala_id = escala_id
                atribuicao_escala.escala.id = escala_id

                atribuicao_escala.status_id = status_id
                atribuicao_escala.status.id = status_id

                atribuicao_escala.funcionario.matricula = funcionario_matricula
                atribuicao_escala.funcionario.nome = funcionario_nome

                atribuicao_escala.data_inicio = ConverteData.stringDate(data_inicio)
                atribuicao_escala.data_fim = ConverteData.stringDate(data_fim)
                atribuicao_escala.data_cadastro = ConverteData.stringDate(data_cadastro)
                atribuicao_escala.responsavel_cadastro = responsavel_cadastro
                atribuicao_escala.observacao = observacao

            elif operacao == 'VISUALIZAR':
                atribuicao_escala_id = parameters.get('txt_atribuicao_escala', '').strip()
                atribuicao_escala.id = atribuicao_escala_id               
        
        return atribuicao_escala


    
    def setView(self, resultado, request):
        
        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':
                if _verificar_msg(resultado):
                    return render_template('escala/salvar_atribuicao_escala.html', resultado=resultado)
                else:
                    return render_template('escala/salvar_atribuicao_escala.html', resultado=resultado)
            elif operacao == 'SALVAR':
                if _verificar_msg(resultado):
                    return render_template('escala/salvar_atribuicao_escala.html', resultado=resultado)
                else:
                    return redirect(url_for('bp_funcionario.alterar_funcionario', operacao='PRE-ATUALIZAR') + '#id-titulo-jornadas')

            elif operacao == 'VISUALIZAR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_funcionario.alterar_funcionario', operacao='PRE-ATUALIZAR') + '#id-titulo-jornadas')
                else:
                    return render_template('escala/visualizar_atribuicao_escala.html', resultado=resultado)

        else:
            pass


        return f'OPERACAO={operacao}, NOT IMPLEMENTED!'


#################################################################################################
class JornadaViewHelper(AbstractViewHelper):

    def getEntidade(self, request):
        jornada = Jornada()
        jornada.status = StatusJornada()

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':

                # jornada_id = parameters.get('txt_jornada_id', '').strip()
                status_id = parameters.get('txt-jornada-status', '').strip()

                jornada_codigo = parameters.get('txt-jornada-codigo', '').strip()
                jornada_nome = parameters.get('txt-jornada-nome', '').strip()
                jornada_carga_horaria = parameters.get('txt-jornada-carga_horaria', '').strip()
                jornada_quantidade_minima_mpto = parameters.get('txt-jornada-quantidade_minima_mpto', '').strip()
                jornada_quantidade_maxima_dias = parameters.get('txt-jornada-quantidade_maxima_dias', '').strip()
                jornada_intervalo_minimo = parameters.get('txt-jornada-intervalo_minimo', '').strip()
                jornada_limite_max_horas_periodo = parameters.get('txt-jornada-limite_max_horas_periodo', '').strip()
                jornada_data_cadastro = parameters.get('txt-jornada-data_cadastro', '').strip()
                jornada_responsavel_cadastro = parameters.get('txt-jornada-responsavel_cadastro', '').strip()
                jornada_descricao = parameters.get('txt-jornada-descricao', '').strip()

                # jornada.id = jornada_id
                jornada.status.id = status_id

                jornada.codigo = jornada_codigo
                jornada.nome = jornada_nome
                jornada.carga_horaria = jornada_carga_horaria
                jornada.quantidade_minima_mpto = jornada_quantidade_minima_mpto
                jornada.quantidade_maxima_dias = jornada_quantidade_maxima_dias
                jornada.intervalo_minimo = jornada_intervalo_minimo
                jornada.limite_max_horas_periodo = jornada_limite_max_horas_periodo
                jornada.data_cadastro = ConverteData.stringDate(jornada_data_cadastro)
                jornada.responsavel_cadastro = jornada_responsavel_cadastro
                jornada.descricao = jornada_descricao

            elif operacao == 'SALVAR':

                # jornada_id = parameters.get('txt_jornada_id', '').strip()
                status_id = parameters.get('txt-jornada-status', '').strip()

                jornada_codigo = parameters.get('txt-jornada-codigo', '').strip()
                jornada_nome = parameters.get('txt-jornada-nome', '').strip()
                jornada_carga_horaria = parameters.get('txt-jornada-carga_horaria', '').strip()
                jornada_quantidade_minima_mpto = parameters.get('txt-jornada-quantidade_minima_mpto', '').strip()
                jornada_quantidade_maxima_dias = parameters.get('txt-jornada-quantidade_maxima_dias', '').strip()
                jornada_intervalo_minimo = parameters.get('txt-jornada-intervalo_minimo', '').strip()
                jornada_limite_max_horas_periodo = parameters.get('txt-jornada-limite_max_horas_periodo', '').strip()
                jornada_data_cadastro = parameters.get('txt-jornada-data_cadastro', '').strip()
                jornada_responsavel_cadastro = parameters.get('txt-jornada-responsavel_cadastro', '').strip()
                jornada_descricao = parameters.get('txt-jornada-descricao', '').strip()

                # jornada.id = jornada_id
                jornada.status.id = status_id

                jornada.codigo = jornada_codigo
                jornada.nome = jornada_nome
                jornada.carga_horaria = jornada_carga_horaria
                jornada.quantidade_minima_mpto = jornada_quantidade_minima_mpto
                jornada.quantidade_maxima_dias = jornada_quantidade_maxima_dias
                jornada.intervalo_minimo = jornada_intervalo_minimo
                jornada.limite_max_horas_periodo = jornada_limite_max_horas_periodo
                jornada.data_cadastro = ConverteData.stringDate(jornada_data_cadastro)
                jornada.responsavel_cadastro = jornada_responsavel_cadastro
                jornada.descricao = jornada_descricao
           
            elif operacao == 'PRE-ATUALIZAR':

                jornada_id = parameters.get('txt_jornada_id', '').strip()
                status_id = parameters.get('txt-jornada-status', '').strip()

                jornada_codigo = parameters.get('txt-jornada-codigo', '').strip()
                jornada_nome = parameters.get('txt-jornada-nome', '').strip()
                jornada_carga_horaria = parameters.get('txt-jornada-carga_horaria', '').strip()
                jornada_quantidade_minima_mpto = parameters.get('txt-jornada-quantidade_minima_mpto', '').strip()
                jornada_quantidade_maxima_dias = parameters.get('txt-jornada-quantidade_maxima_dias', '').strip()
                jornada_intervalo_minimo = parameters.get('txt-jornada-intervalo_minimo', '').strip()
                jornada_limite_max_horas_periodo = parameters.get('txt-jornada-limite_max_horas_periodo', '').strip()
                jornada_data_cadastro = parameters.get('txt-jornada-data_cadastro', '').strip()
                jornada_responsavel_cadastro = parameters.get('txt-jornada-responsavel_cadastro', '').strip()
                jornada_descricao = parameters.get('txt-jornada-descricao', '').strip()

                jornada.id = jornada_id
                jornada.status.id = status_id

                jornada.codigo = jornada_codigo
                jornada.nome = jornada_nome
                jornada.carga_horaria = jornada_carga_horaria
                jornada.quantidade_minima_mpto = jornada_quantidade_minima_mpto
                jornada.quantidade_maxima_dias = jornada_quantidade_maxima_dias
                jornada.intervalo_minimo = jornada_intervalo_minimo
                jornada.limite_max_horas_periodo = jornada_limite_max_horas_periodo
                jornada.data_cadastro = ConverteData.stringDate(jornada_data_cadastro)
                jornada.responsavel_cadastro = jornada_responsavel_cadastro
                jornada.descricao = jornada_descricao
            
            elif operacao == 'ATUALIZAR':

                jornada_id = parameters.get('txt_jornada_id', '').strip()
                status_id = parameters.get('txt-jornada-status', '').strip()

                jornada_codigo = parameters.get('txt-jornada-codigo', '').strip()
                jornada_nome = parameters.get('txt-jornada-nome', '').strip()
                jornada_carga_horaria = parameters.get('txt-jornada-carga_horaria', '').strip()
                jornada_quantidade_minima_mpto = parameters.get('txt-jornada-quantidade_minima_mpto', '').strip()
                jornada_quantidade_maxima_dias = parameters.get('txt-jornada-quantidade_maxima_dias', '').strip()
                jornada_intervalo_minimo = parameters.get('txt-jornada-intervalo_minimo', '').strip()
                jornada_limite_max_horas_periodo = parameters.get('txt-jornada-limite_max_horas_periodo', '').strip()
                jornada_data_cadastro = parameters.get('txt-jornada-data_cadastro', '').strip()
                jornada_responsavel_cadastro = parameters.get('txt-jornada-responsavel_cadastro', '').strip()
                jornada_descricao = parameters.get('txt-jornada-descricao', '').strip()

                jornada.id = jornada_id
                jornada.status.id = status_id

                jornada.codigo = jornada_codigo
                jornada.nome = jornada_nome
                jornada.carga_horaria = jornada_carga_horaria
                jornada.quantidade_minima_mpto = jornada_quantidade_minima_mpto
                jornada.quantidade_maxima_dias = jornada_quantidade_maxima_dias
                jornada.intervalo_minimo = jornada_intervalo_minimo
                jornada.limite_max_horas_periodo = jornada_limite_max_horas_periodo
                jornada.data_cadastro = ConverteData.stringDate(jornada_data_cadastro)
                jornada.responsavel_cadastro = jornada_responsavel_cadastro
                jornada.descricao = jornada_descricao

            elif operacao == 'PRE-EXCLUIR':

                jornada_id = parameters.get('txt_jornada_id', '').strip()
                status_id = parameters.get('txt-jornada-status', '').strip()

                jornada_codigo = parameters.get('txt-jornada-codigo', '').strip()
                jornada_nome = parameters.get('txt-jornada-nome', '').strip()
                jornada_carga_horaria = parameters.get('txt-jornada-carga_horaria', '').strip()
                jornada_quantidade_minima_mpto = parameters.get('txt-jornada-quantidade_minima_mpto', '').strip()
                jornada_quantidade_maxima_dias = parameters.get('txt-jornada-quantidade_maxima_dias', '').strip()
                jornada_intervalo_minimo = parameters.get('txt-jornada-intervalo_minimo', '').strip()
                jornada_limite_max_horas_periodo = parameters.get('txt-jornada-limite_max_horas_periodo', '').strip()
                jornada_data_cadastro = parameters.get('txt-jornada-data_cadastro', '').strip()
                jornada_responsavel_cadastro = parameters.get('txt-jornada-responsavel_cadastro', '').strip()
                jornada_descricao = parameters.get('txt-jornada-descricao', '').strip()

                jornada.id = jornada_id
                jornada.status.id = status_id

                jornada.codigo = jornada_codigo
                jornada.nome = jornada_nome
                jornada.carga_horaria = jornada_carga_horaria
                jornada.quantidade_minima_mpto = jornada_quantidade_minima_mpto
                jornada.quantidade_maxima_dias = jornada_quantidade_maxima_dias
                jornada.intervalo_minimo = jornada_intervalo_minimo
                jornada.limite_max_horas_periodo = jornada_limite_max_horas_periodo
                jornada.data_cadastro = ConverteData.stringDate(jornada_data_cadastro)
                jornada.responsavel_cadastro = jornada_responsavel_cadastro
                jornada.descricao = jornada_descricao
            
            elif operacao == 'EXCLUIR':

                jornada_id = parameters.get('txt_jornada_id', '').strip()
                status_id = parameters.get('txt-jornada-status', '').strip()

                jornada_codigo = parameters.get('txt-jornada-codigo', '').strip()
                jornada_nome = parameters.get('txt-jornada-nome', '').strip()
                jornada_carga_horaria = parameters.get('txt-jornada-carga_horaria', '').strip()
                jornada_quantidade_minima_mpto = parameters.get('txt-jornada-quantidade_minima_mpto', '').strip()
                jornada_quantidade_maxima_dias = parameters.get('txt-jornada-quantidade_maxima_dias', '').strip()
                jornada_intervalo_minimo = parameters.get('txt-jornada-intervalo_minimo', '').strip()
                jornada_limite_max_horas_periodo = parameters.get('txt-jornada-limite_max_horas_periodo', '').strip()
                jornada_data_cadastro = parameters.get('txt-jornada-data_cadastro', '').strip()
                jornada_responsavel_cadastro = parameters.get('txt-jornada-responsavel_cadastro', '').strip()
                jornada_descricao = parameters.get('txt-jornada-descricao', '').strip()

                jornada.id = jornada_id
                jornada.status.id = status_id

                jornada.codigo = jornada_codigo
                jornada.nome = jornada_nome
                jornada.carga_horaria = jornada_carga_horaria
                jornada.quantidade_minima_mpto = jornada_quantidade_minima_mpto
                jornada.quantidade_maxima_dias = jornada_quantidade_maxima_dias
                jornada.intervalo_minimo = jornada_intervalo_minimo
                jornada.limite_max_horas_periodo = jornada_limite_max_horas_periodo
                jornada.data_cadastro = ConverteData.stringDate(jornada_data_cadastro)
                jornada.responsavel_cadastro = jornada_responsavel_cadastro
                jornada.descricao = jornada_descricao

        return jornada
        

    def setView(self, resultado, request):

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            if operacao == 'PRE-SALVAR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_escala.jornadas'))
                else:
                    return render_template('escala/cadastrar_jornada.html', resultado=resultado)

            elif operacao == 'SALVAR':
                if _verificar_msg(resultado):
                    return render_template('escala/cadastrar_jornada.html', resultado=resultado)
                else:
                    return redirect(url_for('bp_escala.jornadas'))

            elif operacao == 'PRE-ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('escala/atualizar_jornada.html', resultado=resultado)
                else:
                    return render_template('escala/atualizar_jornada.html', resultado=resultado)
            
            elif operacao == 'ATUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('escala/atualizar_jornada.html', resultado=resultado)
                else:
                    return render_template('escala/atualizar_jornada.html', resultado=resultado)
           
            elif operacao == 'PRE-EXCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_escala.jornadas'))
                else:
                    return render_template('escala/excluir_jornada.html', resultado=resultado)
            
            elif operacao == 'EXCLUIR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_escala.jornadas'))
                else:
                    return redirect(url_for('bp_escala.jornadas'))
                    
        else:
            _verificar_msg(resultado)
            return render_template('escala/jornadas.html', resultado=resultado)
            
        return f'OPERACAO={operacao}, NOT IMPLEMENTED!'

