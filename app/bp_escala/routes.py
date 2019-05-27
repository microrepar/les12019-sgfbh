from app.bp_escala import bp
from les12019_web import controle
from flask import render_template, request

from app.bp_escala.models import AtribuicaoEscala
from les12019_core.aplicacao import Resultado


@bp.route('/escalas')
def escalas():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/cadastro_de_escala', methods=['POST', 'GET'])
def cadastro_de_escala():   
    return controle.ctrl.doProcessRequest(request)


@bp.route('/atualizar_escala', methods=['POST', 'GET'])
def atualizar_escala():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/excluir_escala', methods=['POST', 'GET'])
def excluir_escala():
    return controle.ctrl.doProcessRequest(request)


@bp.route('/cadastrar_horario', methods=['POST', 'GET'])
def cadastrar_horario():
   return controle.ctrl.doProcessRequest(request)


@bp.route('/atualizar_horario', methods=['POST', 'GET'])
def atualizar_horario():
   return controle.ctrl.doProcessRequest(request)


@bp.route('/excluir_horario', methods=['POST', 'GET'])
def excluir_horario():
   return controle.ctrl.doProcessRequest(request)

@bp.route('/salvar_atribuicao_escala', methods=['GET', 'POST'])
def salvar_atribuicao_escala():
   return controle.ctrl.doProcessRequest(request)
   

@bp.route('/visualizar_atribuicao_escala')
def visualizar_atribuicao_escala():
   return controle.ctrl.doProcessRequest(request)


@bp.route('/jornadas')
def jornadas():
   return controle.ctrl.doProcessRequest(request)


@bp.route('/cadastrar_jornada', methods=['POST', 'GET'])
def cadastrar_jornada():
   return controle.ctrl.doProcessRequest(request)


@bp.route('/atualizar_jornada', methods=['POST', 'GET'])
def atualizar_jornada():
   return controle.ctrl.doProcessRequest(request)
   

@bp.route('/excluir_jornada', methods=['POST', 'GET'])
def excluir_jornada():
   return controle.ctrl.doProcessRequest(request)

