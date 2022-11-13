import datetime

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from .config import Config

app = Flask(__name__)
app.config.from_object(Config)
app.permanent_session_lifetime = datetime.timedelta(days=14)

login_manager = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
