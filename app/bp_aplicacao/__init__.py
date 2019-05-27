from flask import Blueprint

bp = Blueprint('bp_aplicacao', __name__)

from app.bp_aplicacao import routes, models
