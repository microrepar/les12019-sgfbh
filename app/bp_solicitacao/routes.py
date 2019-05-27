
"""[summary]
"""

from flask import render_template, redirect, url_for, request, flash
from app.bp_solicitacao import bp
from les12019_web import controle




@bp.route('/cadastrar_solicitacao', methods=['POST', 'GET'])
def cadastrar_solicitacao():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/atualizar_solicitacao', methods=['POST', 'GET'])
def atualizar_solicitacao():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/excluir_solicitacao', methods=['POST', 'GET'])
def excluir_solicitacao():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/cadastrar_despacho', methods=['POST', 'GET'])
def cadastrar_despacho():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/consultar_solicitacoes')
def consultar_solicitacoes():
    return controle.ctrl.doProcessRequest(request)


