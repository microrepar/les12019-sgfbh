

"""[summary]
"""

from flask import render_template, redirect, url_for, request, flash
from app.bp_aplicacao import bp
from les12019_web import controle


@bp.route('/banco_de_horas')
def banco_de_horas():
    return render_template('banco_horas/banco_de_horas.html')


@bp.route('/banco_de_horas_detalhes')
def banco_de_horas_detalhes():
    return render_template('banco_horas/banco_de_horas_detalhes.html')


@bp.route('/compensacoes')
def compensacoes():
    return render_template('banco_horas/bancoDeHorasCompensacoes.html')

