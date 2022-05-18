import requests 
BASE_URL= "http://127.0.0.1:5001"

#Se solicita un endpoint y se compara status code al esperado.
# Respuestas informativas (100–199),
# Respuestas satisfactorias (200–299),
# Redirecciones (300–399),
# Errores de los clientes (400–499),
# y errores de los servidores (500–599).

def test_base(endpoint, status):
    try:
        r = requests.get(BASE_URL+endpoint)
    except:
        return False
    return r.status_code==status
    
#Succes 
def test_index():
    return test_base("/",200)

def test_dashboard():
    return test_base("/dashboard",401)

def test_usuario_login():
    return test_base("/usuario_login",200)

def test_usuario_recuperar():
    return test_base("/usuario_recuperar",200)

def test_usuario_create():
    return test_base("/usuario_create",200)

def test_resgistrar_transaccion():
    return test_base("/registrar_transaccion",200)

def test_editar_transaccion():
    return test_base("/editar_transaccion",200)

def test_eliminar_transaccion():
    return test_base("/eliminar_transaccion",200)

def test_eliminar_transaccion_all():
    return test_base("/eliminar_transaccion_all",200)

def test_logout():
    return test_base("/logout",401)





if __name__ == "__main__":
    print("testeando index....")
    print(test_index())
    print(test_dashboard())
    print(test_usuario_login())
    print(test_usuario_recuperar())
    print(test_usuario_create())
    print(test_resgistrar_transaccion())
    print(test_editar_transaccion())
    print(test_eliminar_transaccion())
    print(test_eliminar_transaccion_all())
    print(test_logout())
