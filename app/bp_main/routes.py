"""[summary]
"""

from flask import render_template, redirect, url_for, request, flash
from app.bp_main import bp
from les12019_web import controle



@bp.route('/index')
def home():
    return render_template('home.html')


@bp.route('/')
@bp.route('/index_')
def home_outros():
    return render_template('home.html')


@bp.route('/admin/')
def admin():
    return redirect(url_for('bp_main.home'))


@bp.route('/funcionario')
def func():
    return redirect(url_for('bp_main.home_outros'))


@bp.route('/usuarios')
def usuarios():
    return render_template('autenticacao/usuarios.html')


@bp.route('/cadastroUsuario')
def cad_usuario():
    return render_template('autenticacao/usuarioCadastro.html')


@bp.route('/alterarUsuario')
def alterar_usuario():
    return render_template('autenticacao/usuarioAlterar.html')

@bp.route('/incluir_pendencia_frequencia')
def incluir_pendencia_frequencia():
    return render_template('solicitacao/incluir_pendencia_frequencia.html')


@bp.route('/contato')
def contato():
    return render_template('contato.html')


@bp.route('/contato_')
def contato_outros():
    return render_template('contato.html')


@bp.route('/ajuda')
def ajuda():
    return render_template('ajuda.html')


@bp.route('/ajuda_')
def ajuda_outros():
    return render_template('ajuda.html')


