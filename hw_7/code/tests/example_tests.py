import json
import requests

import settings
from base.base import ApiBase
from mock.flask_mock import SURNAME_DATA

url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'


class Test_Lection(ApiBase):

    def test_add_get_user(self):
        resp = requests.post(f'{url}/add_user', json={'name': 'Ilya'})
        user_id_from_add = resp.json()['user_id']

        resp = requests.get(f'{url}/get_user/Ilya')
        user_id_from_get = resp.json()['user_id']

        assert user_id_from_add == user_id_from_get

    def test_get_non_existent_user(self):
        resp = requests.get(f'{url}/get_user/dnsfndksfnkjsdnfjkdsjkfnsd')
        assert resp.status_code == 404

    def test_add_existent_user(self):
        requests.post(f'{url}/add_user', json={'name': 'Ilya1'})
        resp = requests.post(f'{url}/add_user', json={'name': 'Ilya1'})
        assert resp.status_code == 400

    def test_get_age(self):
        requests.post(f'{url}/add_user', json={'name': 'Vasya'})

        resp = requests.get(f'{url}/get_user/Vasya')

        assert isinstance(resp.json()['age'], int)
        assert 0 <= resp.json()['age'] <= 100

        print(resp.json()['age'])

    def test_has_surname(self):
        SURNAME_DATA['Olya'] = 'Zaitceva'

        requests.post(f'{url}/add_user', json={'name': 'Olya'})

        resp = requests.get(f'{url}/get_user/Olya')
        assert resp.json()['surname'] == 'Zaitceva'

        print(resp.json())

    def test_has_not_surname(self):
        requests.post(f'{url}/add_user', json={'name': 'Sveta'})

        resp = requests.get(f'{url}/get_user/Sveta')
        assert resp.json()['surname'] == None

        print(resp.json())


class Test_HW(ApiBase):

    def test_socket_client_get(self):
        SURNAME_DATA['David'] = ('Storl', 1)
        resp = self.socket_client.get_user_info(name='David')
        assert resp[0].count("200") == 1
        assert json.loads(resp[-1])[0] == 'Storl'

    def test_socket_client_post(self):
        resp = self.socket_client.post_add_user(name='Yury', surname='Borzakovsky')
        assert resp[0].count("201") == 1

        resp1 = self.socket_client.get_user_info(name='Yury')
        assert resp1[0].count("200") == 1
        assert json.loads(resp1[-1])[0] == "Borzakovsky"

    def test_socket_client_delete(self):
        SURNAME_DATA['Wayde'] = ('Niekerk', 1)
        resp = self.socket_client.delete_user_by_name(name='Wayde')
        assert resp[0].count("200") == 1

        resp1 = self.socket_client.get_user_info(name='Wayde')
        assert resp1[0].count("404") == 1

    def test_socket_client_put(self):
        SURNAME_DATA['Dafne'] = ('Ship', 1)
        resp = self.socket_client.put_user_new_surname(name='Dafne', surname='Schippers')
        assert resp[0].count("200") == 1

        resp1 = self.socket_client.get_user_info(name='Dafne')
        assert json.loads(resp1[-1]) == 'Schippers'
        assert resp1[0].count("200") == 1

    def test_flask_mock_delete(self):
        SURNAME_DATA['David'] = ('Storl', 1)
        SURNAME_DATA['Justin'] = ('Gutlin', 2)

        resp = self.socket_client.delete_user_by_name(name='Justin')
        assert resp[0].count("200") == 1

        resp1 = self.socket_client.get_user_info(name='David')
        assert json.loads(resp1[-1])[0] == 'Storl'
        assert resp1[0].count('200') == 1

    def test_flask_mock_put(self):
        SURNAME_DATA['Asafa'] = ('Pow', 1)

        resp = self.socket_client.put_user_new_surname(name='Asafa', surname='Powell')
        assert resp[0].count('200') == 1

        resp1 = self.socket_client.get_user_info(name='Asafa')
        assert (resp1[-1].count('Powell')) == 1
        assert resp1[0].count('200') == 1
