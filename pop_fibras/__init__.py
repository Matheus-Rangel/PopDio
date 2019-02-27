import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt import JWT
from flask_restful import Api
from pop_fibras.api.secure_check import authenticate, identity

app = Flask(__name__)
app.config.from_object('pop_fibras.config.DevelopmentConfig')

# Database
db = SQLAlchemy(app)
from . import models
migrate = Migrate(app, db)

#API
api = Api(app)
jwt= JWT(app, authenticate, identity)

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from pop_fibras.core.views import core
app.register_blueprint(core)