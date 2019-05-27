from flask import Blueprint

bp = Blueprint('bp_escala', __name__)

from app.bp_escala import routes, models
