from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import bcrypt
from flask_login import LoginManager, login_user, logout_user,login_required, current_user,UserMixin


database_name='mislucas'
datatabase_path='postgresql://{}@{}/{}'.format('postgres', 'localhost:5432', database_name)
#postgresql://postgres@localhost:5432/mislucas
db = SQLAlchemy()

class User(db.Model,UserMixin):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False, unique=True)
    password = db.Column(db.String(64), nullable=False)
    transacciones= db.relationship("Transaccion", backref='usuarios')

    @property
    def total(self):
        return sum([t.monto for t in self.transacciones])
    
    def __init__(self,name, surname,email,password):
        self.name=name
        self.surname=surname
        self.email=email
        self.password=bcrypt.generate_password_hash(password).decode("utf-8")
        return None
    
    def format(self):
        return {
            "id": self.id,
            "name": self.name,
            "surname": self.surname,
            "email": self.email,
            "password": self.password,
            "transacciones": self.transacciones
        }
    

class Transaccion(db.Model):
    __tablename__ = "transacciones"
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    monto= db.Column(db.Integer(), nullable=False)
    detalle= db.Column(db.String(), nullable=False)
    tipo= db.Column(db.String(), nullable=False)
    fecha =db.Column(db.DateTime, nullable=False, default = datetime.now)

def setup_db():
    return "hola"

#db.create_all()