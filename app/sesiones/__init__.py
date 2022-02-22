from flask import Blueprint
sesiones = Blueprint('sesiones', __name__, template_folder='templates', static_folder='static')

from . import routes