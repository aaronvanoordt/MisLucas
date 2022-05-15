#Imports
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
    transacciones= db.relationship("Transaccion", backref='usuarios')

    @property
    def total(self):
        return sum([t.monto for t in self.transacciones])

class Transaccion(db.Model):
    __tablename__ = "transacciones"
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer,db.ForeignKey("usuarios.id"),nullable=False)
    monto= db.Column(db.Integer(), nullable=False)
    detalle= db.Column(db.String(), nullable=False)
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
        flash('El usuario no existe')
        return redirect(url_for('index'))

    
@app.route('/usuario_recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method=='POST':
        usu= request.form.get('usuario', )
        u = User.query.filter(User.email == usu).first()
        if u :
            flash('Su contraseña es: ' + u.password)
        else: 
            flash('El usuario no existe')
        
        return redirect(url_for("index"))
    return render_template('recuperar.html')        

@app.route('/usuario_create', methods=['GET', 'POST'])
def create():
    if request.method=='POST':
        corr= request.form.get('correo', )
        nomb= request.form.get('nombre', )
        apell= request.form.get('apellido', )
        contra= request.form.get('contrasena', )
        u=User(email=corr,name=nomb,surname=apell,password=contra)
        db.session.add(u)
        db.session.commit()
        login_user(u)
        return redirect(url_for('dashboard'))
    return render_template('register.html')

@app.route("/dashboard", methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route("/registrar_transaccion", methods=['POST'])
def registrar_transaccion():
    user = current_user.id 
    monto = request.form.get("monto", )
    detalle = request.form.get("detalle", )
    tipo = request.form.get("tipo", )
    try:
        t = Transaccion(user_id=user, monto=monto, detalle=detalle, tipo=tipo)
        db.session.add(t)
        db.session.commit()
    except:
        db.session.rollback()
        flash('Error al crear la transaccion')
    finally:
        db.session.close()
    return redirect(url_for("dashboard"))

@app.route("/editar_transaccion", methods=['POST'])
def editar_transaccion():
    user = current_user.id 
    transaccion_id = request.form.get("transaccion_id", )
    monto = request.form.get("monto", )
    detalle = request.form.get("detalle", )
    tipo = request.form.get("tipo", )
    t = Transaccion.query.get(transaccion_id)
    if not t:
        flash('Esta transaccion no existe')
    elif t.user_id!=user:
        flash('Esta transaccion no pertenece al usuario actual')
    else:
        try:
            t.monto=monto
            t.detalle=detalle
            t.tipo=tipo
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error al editar la transaccion')
        finally:
            db.session.close()
    return redirect(url_for("dashboard"))

@app.route("/eliminar_transaccion", methods=['POST'])
def eliminar_transaccion():
    user = current_user.id 
    transaccion_id=request.form.get('transaccion_id')
    t = Transaccion.query.get(transaccion_id)
    if not t:
        flash('Esta transaccion no existe')
    elif t.user_id!=user:
        flash('Esta transaccion no pertenece al usuario actual')
    else:
        try:
            db.session.delete(t)
            db.session.commit()
        except:
            db.session.rollback()
            flash('Error al eliminar la transaccion')
        finally:
            db.session.close()
    return redirect(url_for("dashboard"))


    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


#Runner
if __name__ == "__main__":
	app.run(debug=True, port=5000)