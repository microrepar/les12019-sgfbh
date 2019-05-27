
"""[summary]
"""

from flask import render_template, redirect, url_for, request, flash
from app.bp_frequencia import bp
from les12019_web import controle


@bp.route('/frequencias')
def frequencias():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/apontamento_frequencia_mensal', methods=['GET', 'POST'])
def apontamento_frequencia_mensal():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/frequencia_diaria')
def frequencia_diaria():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/frequencias_mensais_funcionario')
def frequencias_mensais_funcionario():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/apontamento_frequencia_funcionario')
def apontamento_frequencia_funcionario():
    return render_template('frequencia/apontamento_frequencia_funcionario.html')


@bp.route('/visualizar_frequencia_funcionario', methods=['GET', 'POST'])
def visualizar_frequencia_funcionario():
    return controle.ctrl.doProcessRequest(request)

