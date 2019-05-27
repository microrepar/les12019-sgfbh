from flask import Blueprint

bp = Blueprint('bp_frequencia', __name__)

from app.bp_frequencia import routes, models