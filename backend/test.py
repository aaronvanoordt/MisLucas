import unittest
import json
from flask_jwt_extended import create_access_token


from app import create_app
from models import setup_db


class TestMisLucasAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.db = setup_db(self.app, "postgresql://postgres:vanarcar08@localhost:5432/testmislucas")
        self.app.app_context().push()
        access_token = create_access_token(1)
        self.headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        
        self.new_user = {
            "name": "test",
            "surname": "test",
            "email": "test@test.com",
            "password": "Contraseña123!"
        }

        self.actual_user = {
            "email": "test@test.com",
            "password": "Contraseña123!"
        }

        self.new_transaccion = {
            "monto": 100,
            "detalle": "test",
            "tipo": "ingreso",
            "fecha": "2020-01-01",
        }


    #---------------Testing---------------
    def test_get_users(self):
        res0= self.client().post('/api/signup', json=self.new_user)

        res = self.client().get('api/users')
        data = json.loads(res.data)
        

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['users']))

    
    def test_signup(self):
        res= self.client().post('/api/signup', json=self.new_user) 
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Un usuario con este email ya existe')
    
    def test_login(self):
        res = self.client().post('/api/login', json=self.actual_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_me(self):
     
        res = self.client().post('/api/login', json=self.actual_user,headers=self.headers)
        with self.client():
            res = self.client().get('/api/me', headers=self.headers)
            data = json.loads(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            

    def test_logout(self):
        res0 = self.client().post('/api/login', json=self.actual_user)
        data0 = json.loads(res0.data)
        res = self.client().post('/api/logout', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Successfully logged out.')
    
    def test_get_all_transacciones(self):
        res= self.client().post('/api/login', json=self.actual_user)
        data0= json.loads(res.data)
        res = self.client().get('/api/transacciones', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_add_transaccion(self):
        res= self.client().post('/api/login', json=self.actual_user)
        res = self.client().post('/api/transacciones', json=self.new_transaccion, headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_delete_transaccion(self):
        res = self.client().delete('api/transacciones/0', headers=self.headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Transacción no encontrada")
    
    '''def test_update_transaccion(self):
        res= self.client().post('/api/login', json=self.actual_user)
        res = self.client().put('/api/transacciones/0', data=self.new_transaccion, headers=self.headers)
        print(res.data)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['transaccion'])'''