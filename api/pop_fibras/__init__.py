import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_restful import Api
from pop_fibras.api.secure_check import authenticate, identity
from pop_fibras.api import resources

app = Flask(__name__)
app.config.from_object('pop_fibras.config.DevelopmentConfig')

# Database
db = SQLAlchemy(app)
from . import models
migrate = Migrate(app, db)

#JWT
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

#API
api = Api(app)
api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
api.add_resource(resources.UserLogoutAccess, '/logout/access')
api.add_resource(resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(resources.TokenRefresh, '/token/refresh')
api.add_resource(resources.AllUsers, '/users')
api.add_resource(resources.SecretResource, '/secret')

# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"

from pop_fibras.core.views import core
app.register_blueprint(core)