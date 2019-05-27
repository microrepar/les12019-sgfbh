"""[summary]
"""

from app.bp_funcionario import bp
from les12019_web import controle
from flask import render_template, redirect, url_for, request, flash


@bp.route('/funcionarios')
def funcionarios():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/cadastroDeFuncionario', methods=['GET', 'POST'])
def cadastrar_funcionario():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/atualizarFuncionario', methods=['GET', 'POST'])
def alterar_funcionario():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/excluirCadastroFuncionario', methods=['GET', 'POST'])
def excluir_funcionario():
    return controle.ctrl.doProcessRequest(request)
