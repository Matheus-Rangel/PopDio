from puppycompanyblog import db,login_manager
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    profile_image = db.Column(db.String(20), nullable=False, default='default_profile.png')
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # This connects BlogPosts to a User Author.
    posts = db.relationship('BlogPost', backref='author', lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        # https://stackoverflow.com/questions/23432478/flask-generate-password-hash-not-constant-output
        return check_password_hash(self.password_hash,password)

    def __repr__(self):
        return f"UserName: {self.username}"

class BlogPost(db.Model):
    # Setup the relationship to the User table
    users = db.relationship(User)

    # Model for the Blog Posts on Website
    id = db.Column(db.Integer, primary_key=True)
    # Notice how we connect the BlogPost to a particular author
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id =user_id


    def __repr__(self):
        return f"Post Id: {self.id} --- Date: {self.date} --- Title: {self.title}"

class Local(db.Model):
    nome = dio_id = db.Column(db.Integer, db.ForeignKey('dio.id'), nullable=False) 

class Dio(db.Model):
    __tablename__ = 'dio'

    local = db.relationship(Local)
    num_portas = 
class DioPorta(db.Model):
    __tablename__ = 'dio_porta'

    dio = db.relationship(Dio)
    dio_id = db.Column(db.Integer, db.ForeignKey('dio.id'), nullable=False)
    
    local_destino = db.relationship(Local)
    local_destino_id = db.Column(db.Integer, db.ForeignKey('local.id'))
    
    fibra = db.Column(db.Integer, nullable=False) 
    fibra_destino = 

    switch_porta = db.Column(db.String(128), nullable=True)
    estado_link =  
    estado_fibra

class Fibra(db.Model):
