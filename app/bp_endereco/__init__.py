from flask import Blueprint

bp = Blueprint('bp_endereco', __name__)

from app.bp_endereco import routes, models