import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_restful import Api

app = Flask(__name__)
app.config.from_object('pop_fibras.config.DevelopmentConfig')

# Database
db = SQLAlchemy(app)
db.metadata.schema = 'dev'
from . import models
migrate = Migrate(app, db)

#JWT
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)

#API
from pop_fibras.resources import (user_resources, cabo_fibra_resources,
                                    estado_link_resources, dio_resources,
                                    porta_dio_resources, local_resources)
api = Api(app)
#USER RESOURCES
api.add_resource(user_resources.UserRegistration, '/registration')
api.add_resource(user_resources.UserLogin, '/login')
api.add_resource(user_resources.UserLogoutAccess, '/logout/access')
api.add_resource(user_resources.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user_resources.TokenRefresh, '/token/refresh')
#CABO_FIBRA RESOURCES
api.add_resource(cabo_fibra_resources.CabosResource, '/cabos')
api.add_resource(cabo_fibra_resources.CaboResource, '/cabo')
#ESTADO_LINK RESOURCES
api.add_resource(estado_link_resources.EstadosResource,'/estados-link')
api.add_resource(estado_link_resources.EstadoResource,'/estado-link')
#DIO RESOURCES
api.add_resource(dio_resources.DiosResource, '/dios')
api.add_resource(dio_resources.DioResource, '/dio')
#PORTA_DIO RESOURCES
api.add_resource(porta_dio_resources.PortaResource, '/porta-dio')
api.add_resource(porta_dio_resources.PortasResource, '/portas-dio')
#LOCAL RESOURCES
api.add_resource(local_resources.LocaisResource, '/locais')
api.add_resource(local_resources.LocalResource, '/local')



# Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"