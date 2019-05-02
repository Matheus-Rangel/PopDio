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
            'observacao':self.observacao,
            'numeroDios': len(self.dios),
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
            'local':self.local_id,
            'quantidadePortas': len(self.portas),
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
    def query_to_json(cls, query):
        return {'dios': [dio.to_json() for dio in query]}
    
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
            'quantidadeFibras':self.quantidade_fibras,
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

    @classmethod
    def query_to_json(cls, query):
        return {'portas': [porta.to_json() for porta in query]}

    def porta_bypass_to_json(self):
        if self.porta_bypass:
            return {
                'id': self.porta_bypass.id,
                'numeroPorta': self.porta_bypass.numeroPorta,
                'dioId': self.porta_bypass.dio.id,
                'dioNome': self.porta_bypass.dio.nome,
                'localId': self.porta_bypass.dio.local.id,
                'localNome': self.porta_bypass.dio.local.nome,
            }
    def porta_destino_to_json(self):
        if self.porta_destino:
            return {
                'id': self.porta_destino.id,
                'numeroPorta': self.porta_destino.numeroPorta,
                'dioId': self.porta_destino.dio.id,
                'dioNome': self.porta_destino.dio.nome,
                'localId': self.porta_destino.dio.local.id,
                'localNome': self.porta_destino.dio.local.nome,
            }
    def to_json(self):
        return {
            'id': self.id,
            'observacao':self.observacao,
            'numeroPorta': self.numero_porta,
            'switchPorta': self.switch_porta,
            'fibraCabo': self.fibra_cabo_id,
            'fibraNumero': self.fibra_numero,
            'portaDestino': self.porta_destino_to_json(),
            'portaBypass': self.porta_bypass_to_json(),
            'estadoLink': self.estado_link_id,
            'dioId': self.dio_id,
        }
