from flask import Blueprint

bp = Blueprint('bp_autenticacao', __name__)

from app.bp_autenticacao import routes, models