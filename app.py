#Imports

from flask import Flask, redirect, render_template, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.helpers import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Configuration

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'super secret key'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:vanarcar08@localhost:5432/mislucas"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Conexión para consultas
engine = create_engine('postgresql://postgres:vanarcar08@localhost:5432/mislucas')
Session = sessionmaker(engine)
session = Session()

#Models
 
class User(db.Model):
    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    total = db.Column(db.Integer(), nullable=False)

    def calculate_total(money):
        total = Ingreso.query.get("Monto") - Egreso.query.get("Monto")
        return total

class Ingreso(db.Model):
    __tablename__ = "Ingresos"
    id = db.Column(db.Integer, primary_key=True)
    monto= db.Column(db.Integer(), nullable=False)
    detalle= db.Column(db.Integer(), nullable=False)
    tipo= db.Column(db.String(), nullable=False)

class Egreso(db.Model):
    __tablename__ = "Egresos"
    id = db.Column(db.Integer, primary_key=True)
    monto= db.Column(db.Integer(), nullable=False)
    detalle= db.Column(db.String(), nullable=False)
    tipo= db.Column(db.String(), nullable=False)

db.create_all()

#Routes

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/usuario_login', methods= ['POST'])
def login_todo():
    usu= request.form.get('usuario', )
    contra= request.form.get('contrasena', )
    
    con = session.query(User).filter(
        User.email == usu
    ).filter(
        User.password == contra
    )
    
    if con.count() > 0:
        return render_template('dashboard.html')
    else:
        return "El usuario no existe"
    
@app.route('/usuario_crear_registro', methods= ['POST'])
def crear_usuario_todo():
    corr= request.form.get('correo', )
    nomb= request.form.get('nombre', )
    apell= request.form.get('apellido', )
    contra= request.form.get('contrasena', )
    
    session.add(User(email=corr,name=nomb,surname=apell,password=contra))
    session.commit()
    
    flash('Usuario Creado')
    
    return render_template('register.html')
    
@app.route('/usuario_recuperar')
def recuperar_todo():
    return render_template('recuperar.html')

@app.route('/usuario_recuperar_contra', methods= ['POST'])
def recuperar_contra_todo():
    usu= request.form.get('usuario', )
    
    con = session.query(User.password).filter(
        User.email == usu
    )
    
    if con.count() > 0:
        flash('Su contraseña es: ' + con[0].contrasena)
    else: flash('El usuario no existe')
    
    return render_template('recuperar.html')
        

@app.route('/usuario_create')
def create_todo():
    return render_template('register.html')


#Runner
if __name__ == "__main__":
	app.run(debug=True, port=5000)