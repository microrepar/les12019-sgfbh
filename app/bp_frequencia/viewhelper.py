from les12019_web.abstract_viewhelper import AbstractViewHelper, _verificar_msg
from les12019_core.aplicacao import Resultado, ConverteData
from les12019_core.utils import get_parameters_request
from app.bp_frequencia.models import EspelhoMensal, StatusEspelho, EspelhoDiario
from app.bp_funcionario.models import Funcionario
from flask import Request, render_template, url_for, redirect, session


################################################# ESPELHO MENSAL #############################################
class EspelhoMensalViewHelper(AbstractViewHelper):

    def getEntidade(self, request: Request):
        
        funcionario = Funcionario()
        espelho_mensal = EspelhoMensal()
        espelho_mensal.funcionario = funcionario


        parameters = get_parameters_request(request)

        operacao  = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:

            if operacao == 'PRE-AVALIAR':
                funcionario_id = parameters.get('txt_funcionario_id', session.get('txt_funcionario_id', '')).strip()
                session['txt_funcionario_id'] = funcionario_id                
                espelho_mensal.funcionario.id = funcionario_id

                mes_referencia = parameters.get('txt-espelho-mensal-mes_referencia','').strip()
                ano_referencia = parameters.get('txt-espelho-mensal-ano_referencia','').strip()

                espelho_mensal.mes_referencia = mes_referencia
                espelho_mensal.ano_referencia = ano_referencia
                
            elif operacao == 'AVALIAR':
                funcionario_id = parameters.get('txt_funcionario_id', session.get('txt_funcionario_id', '')).strip()
                espelho_mensal_id = parameters.get('txt_espelho_mensal_id', session.get('txt_espelho_mensal_id', '')).strip()
                session['txt_funcionario_id'] = funcionario_id
                session['txt_espelho_mensal_id'] = espelho_mensal_id               

                espelho_mensal.funcionario.id = funcionario_id
                espelho_mensal.id = espelho_mensal_id

            elif operacao == 'PRE-VISUALIZAR':
                funcionario_id = parameters.get('txt_funcionario_id', session.get('txt_funcionario_id', '')).strip()
                session['txt_funcionario_id'] = funcionario_id                
                espelho_mensal.funcionario.id = funcionario_id

                mes_referencia = parameters.get('txt-espelho-mensal-mes_referencia','').strip()
                ano_referencia = parameters.get('txt-espelho-mensal-ano_referencia','').strip()

                espelho_mensal.mes_referencia = mes_referencia
                espelho_mensal.ano_referencia = ano_referencia

            elif operacao == 'VISUALIZAR':
                funcionario_id = parameters.get(
                    'txt_funcionario_id', session.get('txt_funcionario_id', '')).strip()
                espelho_mensal_id = parameters.get(
                    'txt_espelho_mensal_id', session.get('txt_espelho_mensal_id', '')).strip()
                session['txt_funcionario_id'] = funcionario_id
                session['txt_espelho_mensal_id'] = espelho_mensal_id

                espelho_mensal.funcionario.id = funcionario_id
                espelho_mensal.id = espelho_mensal_id
            
            
            

        return espelho_mensal


    def setView(self, resultado, request):
        
        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')
        
        if operacao !=  'LISTAR' and operacao is not None:
            
            if operacao == 'PRE-AVALIAR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_frequencia.frequencias', operacao='APONTAR'))
                else:
                    return redirect(url_for('bp_frequencia.apontamento_frequencia_mensal', txt_espelho_mensal_id=resultado.entidades[-1].id, operacao='AVALIAR'))

            elif operacao == 'AVALIAR':
                if _verificar_msg(resultado):
                    return redirect(url_for('bp_frequencia.frequencias', operacao='APONTAR'))
                else:
                    return render_template('frequencia/apontamento_frequencia_mensal.html', resultado=resultado)
            
            elif operacao == 'PRE-VISUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('home.html')
                else:
                    return redirect(url_for('bp_frequencia.visualizar_frequencia_funcionario', txt_espelho_mensal_id=resultado.entidades[-1].id, operacao='VISUALIZAR'))
            
            elif operacao == 'VISUALIZAR':
                if _verificar_msg(resultado):
                    return render_template('home.html')
                else:
                    return render_template('frequencia/visualizar_frequencia_funcionario.html', resultado=resultado)

        else:           
            if _verificar_msg(resultado):
                return render_template('frequencia/frequencias.html', resultado=resultado)
            else:
                return render_template('frequencia/frequencias.html', resultado=resultado)
            
        
        return f'OPERACAO:{operacao}, NOT IMPLEMENTED'


################################################# ESPELHO DIARIO #############################################
class EspelhoDiarioViewHelper(AbstractViewHelper):

    def getEntidade(self, request): 

        espelho_dia = EspelhoDiario()        

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            
            if operacao == 'AVALIAR':
                espelho_dia_id = parameters.get('txt_espelho_diario_id','').strip()
                espelho_dia.id = espelho_dia_id

            
        return espelho_dia


    def setView(self, resultado, request):

        parameters = get_parameters_request(request)

        operacao = parameters.get('operacao')

        if operacao != 'LISTAR' and operacao is not None:
            
            if operacao == 'AVALIAR':
                if _verificar_msg(resultado):
                    return render_template('frequencia/frequencia_diaria.html', resultado=resultado)
                else:
                    return render_template('frequencia/frequencia_diaria.html', resultado=resultado)

            
        else:
            _verificar_msg(resultado)
            return render_template('frequencia/frequencia_diaria.html', resultado=resultado)

        return f'OPERACAO:{operacao}, NOT IMPLEMENTED'

        

################################################# CLASSE BASE #############################################
class _ViewHelper(AbstractViewHelper):

    def getEntidade(self, request):
        pass

    def setView(self, resultado, request):
        pass
