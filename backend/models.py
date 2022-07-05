from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_login import UserMixin

database_name='mislucas'
datatabase_path='postgresql://{}@{}/{}'.format('postgres:vanarcar08', 'localhost:5432', database_name)
#postgresql://postgres@localhost:5432/mislucas

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()


def setup_db(app, database_path=datatabase_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SECRET_KEY"] = "Super Secret Key"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    db.create_all()


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
    
    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return created_id
        

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()
    
    def __init__(self,name, surname,email, password):
        self.name=name
        self.surname=surname
        self.email=email
        self.password=bcrypt.generate_password_hash(password).decode("utf-8")

    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'surname': self.surname,
            'email': self.email,
            'total': self.total
        }

    def __repr__(self):
        return f"<User {self.name} {self.surname} {self.email}>"

            
class Transaccion(db.Model):
    __tablename__ = "transacciones"
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    monto= db.Column(db.Integer(), nullable=False)
    detalle= db.Column(db.String(), nullable=False)
    tipo= db.Column(db.String(), nullable=False)
    fecha =db.Column(db.DateTime, nullable=False, default = datetime.now)

    def insert(self):
        try:
            db.session.add(self)
            db.session.commit()
            created_id = self.id
        except:
            db.session.rollback()
        finally:
            db.session.close()
        return created_id
        

    def update(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def __init__(self,user_id,monto,detalle,tipo):
        self.user_id=user_id
        self.monto=monto
        self.detalle=detalle
        self.tipo=tipo
        self.fecha=datetime.now()
    
    def format(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'monto': self.monto,
            'detalle': self.detalle,
            'tipo': self.tipo,
            'fecha': self.fecha
        }
    
    def __repr__(self):
        return f"<Transaccion {self.monto} {self.detalle} {self.tipo}>"



