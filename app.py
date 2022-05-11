#Imports

from flask import Flask, redirect, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.helpers import url_for
from datetime import datetime


#Configuration

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:vanarcar08@localhost:5432/mislucas"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Models
 
class User(db.Model):
    __tablename__ = "Usuarios"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
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

@app.route("/")
def login():
    return render_template("index.html")

@app.route("/login")
def registrar():
    return render_template("login.html")

@app.route("/registrar", methods=["POST"])
def calculate_payment():
    data=request.json
    name = data["name"]
    email = data["email"]
    password = password["password"]
    total = data["total"]
    

    user = User(
		name=name,
		email=email,
        password = password,
		total=int(total),
	)

    db.session.add(user)
    db.session.commit()
    money = user.calculate_total()
    return jsonify({"Monto total": money}), 200


if __name__ == "__main__":
	app.run(debug=True, port=5000)