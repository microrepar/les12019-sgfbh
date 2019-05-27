from flask import Blueprint

bp = Blueprint('bp_relogioponto', __name__)

from app.bp_relogioponto import routes, models