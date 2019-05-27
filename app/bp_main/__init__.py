from flask import Blueprint

bp = Blueprint('bp_main', __name__)

from app.bp_main import routes, models