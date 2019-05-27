"""[summary]
"""
from werkzeug.urls import url_parse
from flask import render_template, request, url_for, flash, redirect, Request
from flask_login import login_required, login_user, current_user, logout_user
from flask_wtf import FlaskForm
from app.bp_autenticacao.forms import LoginForm
from app.bp_autenticacao import bp
from app.bp_autenticacao.models import User


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('bp_main.home'))
    form = LoginForm()
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(f'Nome de usuário ou senha inválidos!')
            return render_template('autenticacao/login.html', titulo='Sign In', form=form)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('bp_main.home')
        return redirect(next_page)    
    else:
        return render_template('autenticacao/login.html', titulo='Sign In', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('bp_main.home'))
