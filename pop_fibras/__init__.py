import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from pop_fibras.config import DevelopmentConfig
app = Flask(__name__)
app.config.from_object('pop_fibras.config.DevelopmentConfig')
# Database
db = SQLAlchemy(app)
Migrate(app,db)

#Login
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "users.login"

#BluePrints
# from pop_dio.core.views import core

# app.register_blueprint(core)