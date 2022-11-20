from flask import Blueprint

workspace = Blueprint('workspace', __name__)

from app.workspace import routes
