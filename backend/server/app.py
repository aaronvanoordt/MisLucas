from config import SECRET_KEY, DATABASE_URI
from flask import Flask, redirect, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user,login_required, current_user,UserMixin
from flask_migrate import Migrate
from flask.helpers import url_for
from datetime import datetime
from flask_bcrypt import Bcrypt



#Configuration

app = Flask(__name__)
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = SECRET_KEY
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
bcrypt = Bcrypt(app)

#Runner
if __name__ == "__main__":
	app.run(debug=True, port=5002)