"""[summary]
"""

from flask import render_template, redirect, url_for, request, flash
from app.bp_endereco import bp
from les12019_web import controle


@bp.route('/cadastroDeEndereco', methods=['GET', 'POST'])
def cadastrar_endereco():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/alteracaoDeEndereco', methods=['GET', 'POST'])
def alterar_endereco():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/exclusaoDeEndereco', methods=['GET', 'POST'])
def excluir_endereco():
    return controle.ctrl.doProcessRequest(request)
