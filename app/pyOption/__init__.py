from flask import Blueprint

pyOption = Blueprint('pyOption', __name__)

from . import views
