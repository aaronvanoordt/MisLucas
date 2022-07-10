from models import setup_db, User, Transaccion

from flask import Flask, Blueprint, jsonify, redirect, render_template, request, flash
from flask_login import LoginManager, login_manager, login_user, logout_user,login_required, current_user
from flask.helpers import url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

login_manager = LoginManager()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = 'm!SLUC4A$'
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
    setup_db(app)
    CORS(app)
    

    api = Blueprint("api", __name__, url_prefix="/api")

    login_manager.init_app(app)
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback():
        return jsonify({
            'description': 'The token has expired.',
            'error': 'token_expired'
        }), 401

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @login_manager.unauthorized_handler
    def noautorizado():
        if request.path.startswith(api.url_prefix):
            return {
                "success": False,
                "message": "Usuario no loggeado"
            }, 401
        else:
            flash("Primero debes registrarte")
            return redirect(url_for("index"))

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorizations, true")
        response.headers.add("Access-Control-Allow-Methods", "GET, OPTIONS, POST, PATCH, DELETE")
        return response

    #
    # API ROUTES
    #

    # GET

    @api.route('/', methods=['GET'])
    def api_index():
        return {"message": "Bienvenido al API de MisLucas"}, 200

    #@login_required
    @api.route('/me', methods=['GET'])
    @jwt_required()
    def api_me():
        uid = get_jwt_identity()
        u = User.query.filter(User.id == uid).first()
        return {"nombre": u.name , "apellidos": u.surname}, 200

    @api.route("/users", methods=["GET"])
    def get_users():
        users = User.query.order_by("id").all()

        if len(users) == 0:
            return {
                "message": "No se encontaron usuarios"
            }, 404
        
        return {
            "success": True,
            "users": [user.format() for user in users],
            "total_users": len(users)
        }, 200

    #@login_required
    @api.route("/transacciones", methods=["GET"])
    @jwt_required()
    def get_transacciones():
        uid = get_jwt_identity()
        u = User.query.filter(User.id == uid).first()
        t = Transaccion.query.filter(Transaccion.user_id == u.id).all()
        return {
            "transacciones": [transaccion.format() for transaccion in t],
        }, 200

    @api.route("/transacciones/<id>", methods=["GET"])
    @login_required
    def get_transaccion(id):
        t = Transaccion.query.get(id)

        if t is None:
            return {
                "success": False,
                "message": "Transacción no encontrada"
            }, 404

        if t.user_id != current_user.id:
            return {
                "success": False,
                "message": "La transacción no le pertenece a este usuario"
            }, 403

        return t.format(), 200

    # POST
    @api.route('/signup', methods=['POST'])
    def api_signup():
        if current_user.is_authenticated:
            return {
                "success": False,
                "message": "Usuario ya loggeado"
            }, 400

        email = request.json.get('email')
        name = request.json.get('name')
        surname = request.json.get('surname')
        password = request.json.get('password')

        if email is None:
            return {
                "success": False,
                "message": "No se ha enviado el email"
            }, 400

        if password is None:
            return {
                "success": False,
                "message": "No se ha enviado contraseña"
            }, 400

        if name is None:
            return {
                "success": False,
                "message": "No se ha enviado nombre"
            }, 400

        if surname is None:
            return {
                "success": False,
                "message": "No se ha enviado apellido"
            }, 400

        if User.query.filter_by(email=email).first():
            return {
                "success": False,
                "message": "Un usuario con este email ya existe"
            }, 400

        if len(email) < 8:
            return {
                "success": False,
                "message": "El email debe tener minimo 8 caracteres"
            }, 400

        if len(password) < 8:
            return {
                "success": False,
                "message": "La contraseña debe tener minimo 8 caracteres"
            }, 400
    
        if password.islower():
            return {
                "success": False,
                "message": "La contraseña debe tener minimo una mayúscula"
            }, 400

        if True not in [char.isdigit() for char in password]:
            return {
                "success": False,
                "message": "La contraseña debe tener mínimo un número"
            }, 400

        try:
            u = User(name, surname, email, password)
            u.insert()
            #login_user(u)
            token = create_access_token(identity=u.id)
            return {"success": True,"token": token}, 200
        except Exception as e:
            return {
                "success": False,
                "message": "Error al registrar usuario",
                "error": str(e)
            }, 400

    @api.route('/login', methods=['POST'], )
    def api_login():
        if current_user.is_authenticated:
            return {
                "success": False,
                "message": "Usuario ya loggeado"
            }, 400
        email = request.json.get('email')
        password = request.json.get('password')

        if password is None:
            return {
                "success": False,
                "message": "No se ha enviado contraseña"
            }, 400
        
        u = User.query.filter(User.email == email).first()
        
        if not u:
            return {
                "success": False,
                "message": "El usuario no existe"
            }, 404
        elif not u.check_password(password):
            return {
                "success": False,
                "message": "Contraseña incorrecta"
            }, 401
        else:
            login_user(u, remember=True)
            token = create_access_token(identity=u.id)
            return {"success": True,"token": token}, 200

    #@login_required
    @api.route("/logout", methods=["POST"])
    @jwt_required()
    def api_logout():
        logout_user()
        return {"success": True, 'message':'Successfully logged out.'}, 200


    @api.route("/transacciones", methods=['POST'])
    #@login_required
    @jwt_required()
    def api_registrar_transaccion():
        
        monto = request.json.get("monto")
        detalle = request.json.get("detalle")
        tipo = request.json.get("tipo")

        if monto is None:
            return {
                "success": False,
                "message": "No se ha enviado el monto"
            }, 400
        
        if not str(monto).isdigit():
            return {
                "success": False,
                "message": "El monto debe ser un número"
            }, 400

        if detalle is None:
            return {
                "success": False,
                "message": "No se ha enviado el detalle"
            }, 400
    
        if tipo is None:
            return {
                "success": False,
                "message": "No se ha enviado el tipo"
            }, 400

        try:
            uid = get_jwt_identity()
            t = Transaccion(user_id=uid, monto=int(monto), detalle=detalle, tipo=tipo)
            t.insert()
            return {"success": True, "fecha": t.fecha, "id": t.id}, 200
        except:
            return {
                "success": False,
                "message": "Error al registrar transaccion"
            }, 400

        

    # PATCH / PUT

    @api.route("/transacciones/<id>", methods=['PATCH'])
    #@login_required
    @jwt_required()
    def api_editar_transaccion(id):
        monto = request.json.get("monto")
        detalle = request.json.get("detalle")
        tipo = request.json.get("tipo")
    
        t = Transaccion.query.get(id)
        uid = get_jwt_identity()
        if t is None:
            return {
                "success": False,
                "message": "Transacción no encontrada"
            }, 404

        if t.user_id != uid:
            return {
                "success": False,
                "message": "La transacción no le pertenece a este usuario"
            }, 403

        if monto is not None:
            try: 
                t.monto = int(monto)
            except:
                return {
                    "success": False,
                    "message": "Error al actualizar el monto"
                }, 400

        if detalle is not None:
            try: 
                t.detalle = detalle
            except:
                return {
                    "success": False,
                    "message": "Error al actualizar el detalle"
                }, 400

        if tipo is not None:
            try: 
                t.tipo = tipo
            except:
                return {
                    "success": False,
                    "message": "Error al actualizar el tipo"
                }, 400

        try:
            t.update()
        except Exception as e:
            return {
                "success": False,
                "message": "Error al actualizar transacción",
                "error": str(e)
            }, 400
        else:
            return {"success": True}, 200

    # DELETE

    @api.route("/transacciones/<id>", methods=['DELETE'])
    #@login_required
    @jwt_required()
    def api_eliminar_transaccion(id):
        t = Transaccion.query.get(id)
        uid = get_jwt_identity()
        if t is None:
            return {
                "success": False,
                "message": "Transacción no encontrada"
            }, 404

        if t.user_id != uid:
            return {
                "success": False,
                "message": "La transacción no le pertenece a este usuario"
            }, 403

        try:
            t.delete()
        except:
            return {
                "success": False,
                "message": "Error al eliminar transacción"
            }, 400
        else:
            return {"success": True}, 200

    #
    # TEMPLATE ROUTES
    #

    @app.route('/')
    def index():
        return render_template('login.html')

    @app.route('/usuario_login', methods= ['POST'])
    def login():
        usu= request.form.get('usuario')
        contra= request.form.get('contrasena')
        
        u = User.query.filter(User.email == usu).first()
        
        if not u:
            flash('El usuario no existe')
            return redirect(url_for('index'))
        elif not u.check_password(contra):
            flash('Contraseña incorrecta')
            return redirect(url_for('index'))
        else:
            login_user(u)
            return redirect(url_for("dashboard"))

        
    @app.route('/usuario_recuperar', methods=['GET', 'POST'])
    def recuperar():
        if request.method=='POST':
            usu= request.form.get('usuario', )
            u = User.query.filter(User.email == usu).first()
            if u :
                flash("Te enviamos un correo")
            else: 
                flash('El usuario no existe')
            
            return redirect(url_for("index"))
        return render_template('recuperar.html')        

    @app.route('/usuario_create', methods=['GET', 'POST'])
    def create():
        if request.method=='POST':
            corr= request.form.get('correo', )
            name = request.form.get('nombre', )
            surname= request.form.get('apellido', )
            contra= request.form.get('contrasena', )
            if User.query.filter_by(email=corr).first():
                flash("ERROR EMAIL: Un usuario con este correo ya existe")
                return redirect(url_for('create'))
            
            if len(contra)<8:
                flash("ERROR DE CONTRASEÑA: Tienes que tener minimo 8 caracteres")
                return redirect(url_for('create'))
        
            if contra.islower():
                flash("ERROR DE CONTRASEÑA: Tiene que tener minimo una mayúscula")
                return redirect(url_for('create'))

            if True not in [char.isdigit() for char in contra]:
                flash("ERROR DE CONTRASEÑA: Tiene que tener minimo un número")
                return redirect(url_for('create'))

            #error handling - manejo de errores
            try:
                u = User(name, surname, corr, contra)
                u.insert()
                login_user(u)
            except Exception as e:
                flash("ERROR: " + str(e))
            else:
                return redirect(url_for('dashboard'))
        return render_template('register.html')


    @app.route("/dashboard", methods=['GET'])
    @login_required
    def dashboard():
        #Se orderna por fecha de transaccion  mas reciente >
        return render_template('dashboard.html', transacciones=sorted(current_user.transacciones, key=lambda t:t.fecha, reverse=True)) 

    @app.route("/registrar_transaccion", methods=['POST'])
    @login_required
    def registrar_transaccion():
        monto = request.form.get("monto")
        detalle = request.form.get("detalle")
        tipo = request.form.get("tipo")

        try:
            t = Transaccion(user_id=current_user.id, monto=monto, detalle=detalle, tipo=tipo)
            t.insert()
        except:
            flash('Error al crear la transaccion')
        return redirect(url_for("dashboard"))

    @app.route("/editar_transaccion", methods=['POST'])
    @login_required
    def editar_transaccion():
        user = current_user.id 
        transaccion_id = int(request.form.get("transaccion_id", ))
        monto = int(request.form.get("monto", ))
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
                t.update()
            except Exception as e:
                print(e)
                flash('Error al editar la transaccion')
        return redirect(url_for("dashboard"))

    @app.route("/eliminar_transaccion", methods=['POST'])
    @login_required
    def eliminar_transaccion():
        user = current_user.id 
        transaccion_id = request.form.get('transaccion_id')
        t = Transaccion.query.get(transaccion_id)
        if not t:
            flash('Esta transaccion no existe')
        elif t.user_id != user:
            flash('Esta transaccion no pertenece al usuario actual')
        else:
            try:
                t.delete()
            except:
                flash('Error al eliminar la transaccion')
        return redirect(url_for("dashboard"))

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect(url_for("index"))

    app.register_blueprint(api)

    return app
