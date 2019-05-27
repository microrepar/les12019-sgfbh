from flask import Blueprint

bp = Blueprint('bp_ponto', __name__)

from app.bp_ponto import routes, models