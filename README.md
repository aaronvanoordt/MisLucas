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

# Hosts

# Error Handling

# Deployment Scripts/Configuration
Estando dentro de la carpeta que contenga el archivo, primero se deberá ejecutar el virtual enviroment que ha de contener todos los elementos de requirements.txt; una vez activo deberemos ejecutar el comando "python app.py" para correr el servidor.
## Configuration
1. Crear archivo config.py
2. Agregar a ese archivo la variable = "DATABASE_URI" y "SECRET_KEY"
3. Cambiar variables = "DATABASE_URI" y "SECRET_KEY"
4. Crear el virtual enviroment con psycopg2-binary, flask, flask-Migrate y flask-login usando pip install


