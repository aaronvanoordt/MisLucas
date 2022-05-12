#Imports
from ast import Return
from re import L
from config import SECRET_KEY, DATABASE_URI
from flask import Flask, redirect, render_template, request, jsonify, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user,login_required, current_user,UserMixin
from flask_migrate import Migrate
from flask.helpers import url_for


#Configuration

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)



#Models
 
class User(db.Model,UserMixin):
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
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@login_manager.unauthorized_handler
def noautorizado():
    flash("PRIMERO INGRESA A TU CUENTA")
    return redirect(url_for("index"))

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/usuario_login', methods= ['POST'])
def login():
    usu= request.form.get('usuario', )
    contra= request.form.get('contrasena', )
    
    u = User.query.filter(
        User.email == usu
    ).filter(
        User.password == contra
    ).first()
    
    if u:
        login_user(u)
        return redirect(url_for("dashboard"))
    else:
        return """<h1>El usuario no existe</h1>"""

    
@app.route('/usuario_crear_registro', methods= ['POST'])
def crear_usuario():
    corr= request.form.get('correo', )
    nomb= request.form.get('nombre', )
    apell= request.form.get('apellido', )
    contra= request.form.get('contrasena', )
    u=User(email=corr,name=nomb,surname=apell,password=contra)
    db.session.add(u)
    db.session.commit()
    login_user(u)
    return redirect(url_for("dashboard"))
    
@app.route('/usuario_recuperar')
def recuperar():
    return render_template('recuperar.html')

@app.route('/usuario_recuperar_contra', methods= ['POST'])
def recuperar_contra():
    usu= request.form.get('usuario', )
    
    u = User.query.filter(User.email == usu).first()
    
    if u :
        flash('Su contraseña es: ' + u.password)
    else: flash('El usuario no existe')
    
    return redirect(url_for("index"))
        

@app.route('/usuario_create')
def create():
    return render_template('register.html')

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


#Runner
if __name__ == "__main__":
	app.run(debug=True, port=5000)