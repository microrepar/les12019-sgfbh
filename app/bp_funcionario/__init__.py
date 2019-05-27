from flask import Blueprint

bp = Blueprint('bp_funcionario', __name__)

from app.bp_funcionario import routes, models