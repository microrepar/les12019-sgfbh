"""[summary]
"""

from flask import render_template, redirect, url_for, request, flash
from app.bp_ponto.models import Ponto, StatusPonto, TipoPonto
from app.bp_ponto import bp
from les12019_web import controle
from les12019_core.aplicacao import Resultado


@bp.route('/cadastrar_ponto', methods=['POST', 'GET'])
def cadastrar_ponto():
    return controle.ctrl.doProcessRequest(request)
    
    
@bp.route('/atualizar_ponto', methods=['POST', 'GET'])
def atualizar_ponto():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/excluir_ponto', methods=['POST', 'GET'])
def excluir_ponto():
    return controle.ctrl.doProcessRequest(request)
