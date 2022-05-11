#Imports

from config import SECRET_KEY, DATABASE_URI
from flask import Flask, redirect, render_template, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.helpers import url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Configuration

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)



#Models
 
class User(db.Model):
    __tablename__ = "usuarios"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    surname = db.Column(db.String(32), nullable=False)
    email = db.Column(db.String(32), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    transacciones= db.relationship("Transaccion", backref="usuario")

    @property
    def total(self):
        return sum([t.monto for t in self.transacciones])

class Transaccion(db.Model):
    __tablename__ = "transacciones"
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    monto= db.Column(db.Integer(), nullable=False)
    detalle= db.Column(db.Integer(), nullable=False)
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
    
    con = User.query.filter(
        User.email == usu
    ).filter(
        User.password == contra
    )
    
    if con.count() > 0:
        return redirect(url_for("dashboard"))
    else:
        return """<h1>El usuario no existe</h1>"""

    
@app.route('/usuario_crear_registro', methods= ['POST'])
def crear_usuario_todo():
    corr= request.form.get('correo', )
    nomb= request.form.get('nombre', )
    apell= request.form.get('apellido', )
    contra= request.form.get('contrasena', )
    
    
    db.session.add(User(email=corr,name=nomb,surname=apell,password=contra))
    db.session.commit()
    
    
    
    return render_template('dashboard.html')
    
@app.route('/usuario_recuperar')
def recuperar_todo():
    return render_template('recuperar.html')

@app.route('/usuario_recuperar_contra', methods= ['POST'])
def recuperar_contra_todo():
    usu= request.form.get('usuario', )
    
    u = User.query.filter(User.email == usu).first()
    
    if u :
        flash('Su contraseña es: ' + u.password)
    else: flash('El usuario no existe')
    
    return render_template('recuperar.html')
        

@app.route('/usuario_create')
def create_todo():
    return render_template('register.html')

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html')


#Runner
if __name__ == "__main__":
	app.run(debug=True, port=5000)