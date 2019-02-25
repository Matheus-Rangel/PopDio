import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('pop_fibras.config.DevelopmentConfig')
# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

# Database
db = SQLAlchemy(app)
from . import models
migrate = Migrate(app, db)

# BluePrints
# from pop_dio.core.views import core

# app.register_blueprint(core)