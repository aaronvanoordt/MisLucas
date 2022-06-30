import requests 
BASE_URL= "http://127.0.0.1:5002"

#Se solicita un endpoint y se compara status code al esperado.
# Respuestas informativas (100–199),
# Respuestas satisfactorias (200–299),
# Redirecciones (300–399),
# Errores de los clientes (400–499),
# y errores de los servidores (500–599).

def test_post(endpoint, status):
    try:
        r = requests.post(BASE_URL+endpoint)
    except:
        return False
    return r.status_code==status

def test_get(endpoint, status):
    try:
        r = requests.get(BASE_URL+endpoint)
    except:
        return False
    return r.status_code==status
#Succes 
# Ejmplo se espera que el status code de index sea 200. si son iguales es True
def test_index():
    return test_get("/",200)

def test_dashboard():
    return test_get("/dashboard",401)

def test_usuario_login():
    return test_post("/usuario_login",200)

def test_usuario_recuperar():
    return test_get("/usuario_recuperar",200)

def test_usuario_create():
    return test_get("/usuario_create",200) 

def test_resgistrar_transaccion():
    return test_post("/registrar_transaccion",401)

def test_editar_transaccion():
    return test_post("/editar_transaccion",401)

def test_eliminar_transaccion():
    return test_post("/eliminar_transaccion",401)

def test_logout():
    return test_get("/logout",401)





if __name__ == "__main__":
    print("testeando index....")
    print(test_index())
    print("testeando dashboard....")
    print(test_dashboard())
    print("testeando login....")
    print(test_usuario_login())
    print("testeando user recuperar....")
    print(test_usuario_recuperar())
    print("testeando registrar....")
    print(test_usuario_create())
    print("testeando registrar transaccion....")
    print(test_resgistrar_transaccion())
    print("testeando editar transaccion....")
    print(test_editar_transaccion())
    print("testeando elminiar transaccion....")
    print(test_eliminar_transaccion())
    print("testeando elminiar todas las transacciones....")
    print("testeando logout....")
    print(test_logout())
