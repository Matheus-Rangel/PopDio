from pop_fibras import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

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

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        de.session.commit()

    def to_json(self):
        return {'username': self.username,}
    
    @classmethod
    def all_to_json(cls):
        return {'users': [user.to_json() for user in cls.query.all()]}
    
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
    observacao = db.Column(db.Text, nullable=True)
    dios = db.relationship("Dio", back_populates="local", order_by="Dio.nome", cascade="all, delete-orphan")
    
    def __init__(self, nome, observacao):
        self.nome = nome
        self.observacao = observacao

    @classmethod
    def find_by_nome(cls, nome):
        return cls.query.filter_by(nome=nome).first()
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
    
    def to_json(self):
        return {
            'id':self.id,
            'nome':self.nome, 
            'observacao':self.observacao
        }

    def dios_to_json(self):
        return {'dios': [dio.to_json() for dio in self.dios]}

    @classmethod
    def all_to_json(cls):
        return {'locais': [local.to_json() for local in cls.query.all()]}

class Dio(db.Model):
    __tablename__ = 'dio'
    id = db.Column(db.Integer, primary_key = True)
    local = db.relationship(Local)
    local_id = db.Column(db.Integer, db.ForeignKey('local.id'), nullable=False)

    nome = db.Column(db.String(64), nullable=False)
    observacao = db.Column(db.Text, nullable=True)
    portas = db.relationship("DioPorta", back_populates="dio", order_by="DioPorta.numero_porta", cascade="all, delete-orphan")
    def __init__(self, local, nome, observacao):
        self.local = local
        self.nome = nome
        self.observacao = observacao
    
    def to_json(self):
        return {
            'id':self.id,
            'local':self.local.to_json(), 
            'quantidade_portas': len(self.portas),
            'nome':self.nome,
            'observacao':self.observacao,
        }

    def portas_to_json(self):
        return {
            'portas': [porta.to_json(dio=False) for porta in self.portas]
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all_to_json(cls):
        return {'dios': [dio.to_json() for dio in cls.query.all()]}

class CaboFibra(db.Model):
    __tablename__ = 'cabo_fibra'
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(128), unique=True, index=True)
    quantidade_fibras = db.Column(db.Integer, nullable=False)
    observacao = db.Column(db.String(128), nullable=True)
    def __repr__(self):
        return f"Nome: {self.nome}"

    @classmethod
    def find_by_nome(cls, nome):
        return cls.query.filter_by(nome=nome).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id':self.id,
            'nome':self.nome,
            'quantidade_fibras':self.quantidade_fibras,
            'observacao':self.observacao,
        }
    @classmethod
    def all_to_json(cls):
        return {'cabos': [cabo.to_json() for cabo in cls.query.all()]}


class EstadoLink(db.Model):
    __tablename__ = 'estado_link'
    
    id = db.Column(db.Integer, primary_key = True)
    nome = db.Column(db.String(64), nullable=False, unique=True)
    observacao = db.Column(db.Text, nullable=True)
    cor = db.Column(db.String(7), nullable=True)
    def __repr__(self):
        return f"Nome: {self.nome}"

    @classmethod
    def find_by_nome(cls, nome):
        return cls.query.filter_by(nome=nome).first()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id':self.id,
            'nome':self.nome, 
            'observacao':self.observacao,
            'cor':self.cor
        }
    
    @classmethod
    def all_to_json(cls):
        return {'estados': [estado.to_json() for estado in cls.query.all()]}

class DioPorta(db.Model):
    __tablename__ = 'dio_porta'
    id = db.Column(db.Integer, primary_key = True)

    porta_destino_id = db.Column(db.Integer, db.ForeignKey('dio_porta.id'), nullable=True)
    porta_destino = db.relationship('DioPorta', foreign_keys=[porta_destino_id])
    
    dio = db.relationship(Dio)
    dio_id = db.Column(db.Integer, db.ForeignKey('dio.id'), nullable=False)
    numero_porta = db.Column(db.Integer, nullable=False)
    
    estado_link = db.relationship(EstadoLink)
    estado_link_id = db.Column(db.Integer, db.ForeignKey('estado_link.id'), nullable=True)

    fibra_cabo = db.relationship(CaboFibra)
    fibra_cabo_id = db.Column(db.Integer, db.ForeignKey('cabo_fibra.id'), nullable=True)

    fibra_numero = db.Column(db.Integer, nullable=True)

    switch_porta = db.Column(db.String(128), nullable=True)
    observacao = db.Column(db.Text, nullable=True)

    porta_bypass_id = db.Column(db.Integer, db.ForeignKey('dio_porta.id'), nullable=True)
    porta_bypass = db.relationship('DioPorta', foreign_keys=[porta_bypass_id])

    def __repr__(self):
        return f"Destino: {self.local_destino.nome}, Estado: {self.estado_link.nome}"

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __porta_destino_json(self):
        if self.porta_destino:
            return {
                'id' : self.porta_destino_id,
                'dio': self.porta_destino.dio.to_json(),
                'numero_porta': self.porta_destino.numero_porta
            }

    def __porta_bypass_json(self):
        if self.porta_bypass:
            return {
                'id' : self.porta_bypass_id,
                'dio': self.porta_bypass.dio.to_json(),
                'numero_porta': self.porta_bypass.numero_porta,
            }

    def to_json(self, dio=True):
        if self.estado_link:
            estado_link = self.estado_link.to_json()
        else:
            estado_link = None
        if self.fibra_cabo:
            fibra_cabo = self.fibra_cabo.to_json()
        else:
            fibra_cabo = None
        json = {
            'id': self.id,
            'observacao':self.observacao,
            'numero_porta': self.numero_porta,
            'switch_porta': self.switch_porta,
            'fibra_cabo': fibra_cabo,
            'fibra_numero': self.fibra_numero,
            'porta_destino': self.__porta_destino_json(),
            'porta_bypass': self.__porta_bypass_json(),
            'estado_link': estado_link,
        }
        if dio:
            json['dio'] = self.dio.to_json()
        return json
