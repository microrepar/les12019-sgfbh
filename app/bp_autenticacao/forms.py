"""[summary]
"""

from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Regexp, Length
from wtforms import StringField, PasswordField, BooleanField, SubmitField, StringField, \
    TextAreaField, DateTimeField, DateField

import re


class LoginForm(FlaskForm):    
    username = StringField('Username', validators=[
        DataRequired(message='* Este campo é obrigatório.')
    ])
    
    password = PasswordField('Password', validators=[
        DataRequired(message='* Este campo é obrigatório.')
    ])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
