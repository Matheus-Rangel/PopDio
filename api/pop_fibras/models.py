from pop_fibras import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    admin = db.Column(db.Boolean)
    def __init__(self, username, password, admin=False):
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.admin = admin

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def find_by_username(cls, username):
        return cls.query.filter_by(username = username).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
    
    def to_json(x):
        return {
            'username': x.username,
        }
    
    def return_all(cls):
        return {'users': list(map(lambda x: cls.to_json(x), cls.query.all()))}
    
    def __repr__(self):
        return f"UserName: {self.username}"

class RevokedTokenModel(db.Model):
    __tablename__ = 'revoked_tokens'
    id = db.Column(db.Integer, primary_key = True)
    jti = db.Column(db.String(120), unique = True, index=True)
    
    def add(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod
    def is_jti_blacklisted(cls, jti):
        query = cls.query.filter_by(jti = jti).first()
        return bool(query)

class Local(db.Model):
    __tablename__ = 'local'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(64), nullable=False, unique=True, index=True) 
    observacao = db.Column(db.Text, nullable=False)
    dios = db.relationship("Dio", back_populates="local")
    def __repr__(self):
        return f"Nome: {self.nome}"
    
    def to_json(self):
        return {
            'id':self.id,
            'nome':self.nome, 
            'observacao':self.observacao
        }

class Dio(db.Model):
    __tablename__ = 'dio'
    id = db.Column(db.Integer, primary_key = True)
    local = db.relationship(Local)
    local_id = db.Column(db.Integer, db.ForeignKey('local.id'), nullable=False)

    numero_portas = db.Column(db.Integer, nullable=False)
    nome = db.Column(db.String(64), nullable=False)
    observacao = db.Column(db.Text, nullable=False)
    portas = db.relationship("DioPorta", back_populates="dio")
    def __repr__(self):
        return f"Nome: {self.nome}, Portas: {self.numero_portas}, Local: {self.local.nome}"
    def to_json(self):
        return {
            'id':self.id,
            'local':self.local.to_json(), 
            'numero_portas':self.numero_portas,
            'nome':self.nome,
            'observacao':self.observacao,
            'portas': [porta.to_json() for porta in self.portas]
        }

class CaboFibra(db.Model):
    __tablename__ = 'cabo_fibra'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(128), unique=True)
    quantidade_fibras = db.Column(db.Integer, nullable=False)
    def __repr__(self):
        return f"Nome: {self.nome}"
    
    def to_json(self):
        return {
            'nome':self.nome,
            'quantidade_fibras':self.quantidade_fibras
        }

class EstadoLink(db.Model):
    __tablename__ = 'estado_link'
    
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(64), nullable=False)
    observacao = db.Column(db.Text, nullable=True)
    cor = db.Column(db.String(7), nullable=True)
    def __repr__(self):
        return f"Nome: {self.nome}"
    
    def to_json(self):
        return {
            'nome':self.nome, 
            'observacao':self.observacao,
            'cor':self.cor
        }

class DioPorta(db.Model):
    __tablename__ = 'dio_porta'
    id = db.Column(db.Integer, primary_key = True)
    last_user = db.relationship(User)
    last_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    
    porta_destino = db.relationship('DioPorta')
    porta_destino_id = db.Column(db.Integer, db.ForeignKey('dio_porta.id'), nullable=True)
    local_destino = db.relationship(Local)
    local_destino_id = db.Column(db.Integer, db.ForeignKey('local.id'), nullable=False)

    dio = db.relationship(Dio)
    dio_id = db.Column(db.Integer, db.ForeignKey('dio.id'), nullable=False)
    numero_porta = db.Column(db.Integer, nullable=False)
    
    estado_link = db.relationship(EstadoLink)
    estado_link_id = db.Column(db.Integer, db.ForeignKey('estado_link.id'), nullable=True)

    fibra_cabo = db.relationship(CaboFibra)
    fibra_cabo_id = db.Column(db.Integer, db.ForeignKey('cabo_fibra.id'), nullable=True)

    fibra_grupo = db.Column(db.Integer, nullable=True)
    fibra_numero = db.Column(db.Integer, nullable=True)

    switch_porta = db.Column(db.String(128), nullable=True)
    observacao = db.Column(db.Text, nullable=True)

    bypass = db.Column(db.Boolean, nullable = False)
    porta_bypass = db.relationship('DioPorta')
    porta_bypass_id = db.Column(db.Integer, db.ForeignKey('dio_porta.id'), nullable=True)

    
    def __repr__(self):
        return f"Destino: {self.local_destino.nome}, Estado: {self.estado_link.nome}"
    
    def to_json(self):
        return {
            'last_user':self.last_user,
            'nome':self.nome, 
            'observacao':self.observacao
        }