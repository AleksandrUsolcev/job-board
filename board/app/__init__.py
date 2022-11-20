import datetime

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.permanent_session_lifetime = datetime.timedelta(days=14)
app.url_map.strict_slashes = False

login = LoginManager(app)
login.login_view = 'login'

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes
from app.template_filters import *
