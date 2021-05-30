import json
import requests

from hw_7.code import settings
from hw_7.code.base.base import ApiBase
from hw_7.code.mock.flask_mock import SURNAME_DATA
from hw_7.code.user_generator.generator import Generator

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
        user_name, user_surname = Generator().create_user_name()
        SURNAME_DATA[user_name] = (user_surname, 1)

        resp = self.socket_client.get_user_info(name=user_name)
        assert resp[0].count('200') == 1
        assert json.loads(resp[-1])[0] == user_surname

    def test_socket_client_post(self):
        user_name, user_surname = Generator().create_user_name()

        resp = self.socket_client.post_add_user(name=user_name, surname=user_surname)
        assert resp[0].count("201") == 1

        resp1 = self.socket_client.get_user_info(name=user_name)
        assert resp1[0].count('200') == 1
        assert json.loads(resp1[-1])[0] == user_surname

    def test_socket_client_delete(self):
        user_name, user_surname = Generator().create_user_name()
        SURNAME_DATA[user_name] = (user_surname, 1)

        resp = self.socket_client.delete_user_by_name(name=user_name)
        assert resp[0].count('200') == 1

        resp1 = self.socket_client.get_user_info(name=user_name)
        assert resp1[0].count('404') == 1

    def test_socket_client_put(self):
        user_name, user_surname = Generator().create_user_name()
        user_surname_new = Generator().create_user_name()[1]
        SURNAME_DATA[user_name] = (user_surname, 1)

        resp = self.socket_client.put_user_new_surname(name=user_name, surname=user_surname_new)
        assert resp[0].count('200') == 1

        resp1 = self.socket_client.get_user_info(name=user_name)
        assert json.loads(resp1[-1]) == user_surname_new
        assert resp1[0].count('200') == 1

    def test_flask_mock_delete(self):
        user_name1, user_surname1 = Generator().create_user_name()
        user_name2, user_surname2 = Generator().create_user_name()

        SURNAME_DATA[user_name1] = (user_surname1, 1)
        SURNAME_DATA[user_name2] = (user_surname2, 2)

        resp = self.socket_client.delete_user_by_name(name=user_name2)
        assert resp[0].count('200') == 1

        resp1 = self.socket_client.get_user_info(name=user_name1)
        assert json.loads(resp1[-1])[0] == user_surname1
        assert resp1[0].count('200') == 1

    def test_flask_mock_put(self):
        user_name, user_surname = Generator().create_user_name()
        user_surname_new = Generator().create_user_name()[1]
        SURNAME_DATA[user_name] = (user_surname, 1)

        resp = self.socket_client.put_user_new_surname(name=user_name, surname=user_surname_new)
        assert resp[0].count('200') == 1

        resp1 = self.socket_client.get_user_info(name=user_name)
        assert (resp1[-1].count(user_surname_new)) == 1
        assert resp1[0].count('200') == 1
