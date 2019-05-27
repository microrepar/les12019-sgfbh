from flask import Blueprint

bp = Blueprint('bp_solicitacao', __name__)

from app.bp_solicitacao import routes, models