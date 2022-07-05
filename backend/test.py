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
            "email": "test@gmail.com",
            "password": "test"
        }

        self.new_transaccion = {
            "monto": 100,
            "descripcion": "test",
            "tipo": "ingreso",
            "fecha": "2020-01-01",
        }
        
    #---------------Testing---------------
    def test_get_all_users(self):
        res = self.client().get('/users')
        data = json.loads(res.data)
        print(data)
    
    '''def test_get_all_transacciones(self):
        res = self.client().get('/transacciones')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_transaccion_by_id(self):
        res = self.client().get('/transacciones/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_signup(self):
        res = self.client().post('/signup', data=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['user'])
        self.assertTrue(data['user']['id'])
        self.assertTrue(data['user']['email'])
        self.assertTrue(data['user']['name'])
        self.assertTrue(data['user']['surname'])
        self.assertTrue(data['user']['password'])
        self.assertTrue(data['user']['total'])
    
    def test_login(self):
        res = self.client().post('/login', data=self.new_user)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['user'])
        self.assertTrue(data['user']['id'])
        self.assertTrue(data['user']['email'])
        self.assertTrue(data['user']['name'])
        self.assertTrue(data['user']['surname'])
        self.assertTrue(data['user']['password'])
        self.assertTrue(data['user']['total'])
    
    def test_logout(self):
        res = self.client().post('/logout', headers={"Authorization": "Bearer " + self.get_token()})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Successfully logged out.')
    
    def test_add_transaccion(self):
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