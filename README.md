# MisLucas
Gestor de finanzas personales

# Integrantes
1. Aarón van Oordt
2. Carlos Patiño
3. Gabriela Perdomo
4. Sebastian Coll

# Descripción y objetivos
MisLucas es una aplicación web que le permite a los usuarios registrar ingresos y egresos para llevar el control de su caja chica, de su plata del día a día. El objetivo de esta herramienta es que las personas puedan ordenar sus finanzas del día a día y así tener espacios de ahorro, diversión, gastos fijos, etc. La visión apunta a ser la herramienta preferida por todos los peruanos (al menos inicialmente) y contribuir a una gestión del dinero más sana y práctica.

# Librerías/Imports
Config: Es el archivo que contiene la configuración que debe ser independiente para cada persona. Está incluido en .gitignore ya que esta debe modificarse según cada usuario
Flask: Como framework que nos ayudará en el desarrollo web usando python
Flask_login: Para manejar el registro y logeo de usuarios
Flask_migrate: Para crear archivos de migración

# Autenticación
Se usó flask_login como el framework encargado de manejar el logeo de usuarios. Además, tenemos comparación entre variables ("==") de lo que el usuario ingresa en el front end con los datos que tenemos en nuestra base de datos

# Endpoints
- '/' : Renderiza index.
- '/usuario_login' : Mediante el metodo POST revisa que los datos ingresados existan.
- '/usuario_recuperar' : Con los metodos GET y POST comprueba que los datos existan y redirecciona al index.
- '/usuario_create' : Con GET y POST obtiene los datos necesarios para registrarse y especifica requerimientos para la contraseña.
- '/dashboard' : Renderiza las transacciones mediante el metodo POST.
- '/registrar_transaccion' : Se piden los datos necesarios para resgistrar una operacion y redirecciona al dashboard.
- '/editar_transaccion' : Comprueba que los datos de la transacción a editar existan y que sea del usuario. Redirecciona al dashboard.
- '/eliminar_transaccion' : Comprueba que los datos de la transacción a eliminar existan y que sea del usuario. Redirecciona al dashboard.
- '/eliminar_transaccion_all' : Verifica que el usuario actual tenga transacciones para eliminar y redirecciona al dashboard.
- '/logout' : Cierra sesión y redirige al index.

Nuestra app cuenta con 10 endpoints en total. 5 de ellos están orientados al manejo del login del usuario, permitiéndole crear un espacio en la DB, recuperar su contraseña, logearse y desalogearse. El endpoint principal es "dashboard", es aquí donde se muestra la tabla principal de la aplicación de manera ordenada. Los otros 5 endpoints sirven para modificar las transacciones que genera un usuario, ya sea para crearlas, eliminarlas y editarlas; es decir, están encargadas del CRUD de los modelos.

# Hosts
El host del app es nuestra propia máquina apoyada de postgres, usando el puerto 5432.

# Error Handling
Cada endpoint cuenta con un esquema de try, except y finally para poder reaccionar en caso que exista un error en la plataforma, ya sea por parte del usuario o de la base de datos (front y back end respectivamente).

# Deployment Scripts/Configuration
Estando dentro de la carpeta que contenga el archivo, primero se deberá ejecutar el virtual enviroment que ha de contener todos los elementos de requirements.txt; una vez activo deberemos ejecutar el comando "python app.py" para correr el servidor.

## Configuration
1. Crear archivo config.py
2. Agregar a ese archivo la variable = "DATABASE_URI" y "SECRET_KEY"
3. Cambiar variables = "DATABASE_URI" y "SECRET_KEY"
4. Crear el virtual enviroment con psycopg2-binary, flask, flask-Migrate y flask-login usando pip install
5. Correr el servidor y logearse o registrarse para entrar al dashboard para empezar a generar transacciones


