
"""[summary]
"""

from flask import render_template, redirect, url_for, request, flash
from app.bp_ocorrencia import bp
from les12019_web import controle


@bp.route('/pendencias', methods=['GET', 'POST'])
def pendencias():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/cadastrar_pendencia', methods=['POST', 'GET'])
def cadastrar_pendencia():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/atualizar_pendencia', methods=['GET', 'POST'])
def atualizar_pendencia():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/excluir_pendencia', methods=['GET', 'POST'])
def excluir_pendencia():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/ocorrencias_frequencia_funcionario')
def ocorrencias_frequencia_funcionario():
    return render_template('ocorrencia/ocorrencias_frequencia_funcionario.html')


@bp.route('/ocorrencias_funcionario', methods=['GET', 'POST'])
def ocorrencias_funcionario():
    return controle.ctrl.doProcessRequest(request)
    # return render_template('ocorrencia/ocorrencias_funcionario.html')


@bp.route('/cadastrar_ocorrencia', methods=['POST', 'GET'])
def cadastrar_ocorrencia():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/atualizar_ocorrencia', methods=['POST', 'GET'])
def atualizar_ocorrencia():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/excluir_ocorrencia', methods=['POST', 'GET'])
def excluir_ocorrencia():
    return controle.ctrl.doProcessRequest(request)