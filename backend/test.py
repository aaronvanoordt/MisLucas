import unittest
import json


from app import create_app
from models import setup_db


class TestMisLucasAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.db = setup_db(self.app, "postgresql://postgres:vanarcar08@localhost:5432/testmislucas")
        

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
            "descripcion": "test",
            "tipo": "ingreso",
            "fecha": "2020-01-01",
        }


    #---------------Testing---------------
    def test_get_users(self):
        res0= self.client().post('/api/signup', json=self.new_user)
        data0= json.loads(res0.data)

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
        res = self.client().post('/api/login', json=self.actual_user)
        with self.client():
            data0 = json.loads(res.data)
            print(data0)

            res = self.client().get('/api/me')
            data = json.loads(res.data)
            print(res.data)

            self.assertEqual(res.status_code, 200)
            self.assertEqual(data['success'], True)
            
            
        
        
    
    '''def test_logout(self):
        res0 = self.client().post('/api/login', json=self.actual_user)
        data0 = json.loads(res0.data)
        res = self.client().post('/api/logout')
        data = json.loads(res.data)

        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Successfully logged out.')'''
    
    '''def test_get_all_transacciones(self):
        res= self.client().post('/api/login', json=self.actual_user)
        data0= json.loads(res.data)
        res = self.client().get('/api/transacciones')
        data = json.loads(res.data)

        print(data0)
        print(data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)'''

    '''def test_get_transaccion_by_id(self):
        res = self.client().get('/transacciones/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)'''
    
    '''def test_add_transaccion(self):
        res = self.client().post('/transacciones', data=self.new_transaccion, headers={"Authorization": "Bearer " + self.get_token()})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['transaccion'])
    
    def test_update_transaccion(self):
        res = self.client().patch('/transacciones/1', data=self.new_transaccion, headers={"Authorization": "Bearer " + self.get_token()})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['transaccion'])
    
    def test_delete_transaccion(self):
        res = self.client().delete('/transacciones/1', headers={"Authorization": "Bearer " + self.get_token()})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Transaccion deleted.')'''