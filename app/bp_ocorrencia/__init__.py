from flask import Blueprint

bp = Blueprint('bp_ocorrencia', __name__)

from app.bp_ocorrencia import routes, models