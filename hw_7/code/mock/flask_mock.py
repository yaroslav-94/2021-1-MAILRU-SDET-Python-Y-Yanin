import json
import threading

from flask import Flask, jsonify, request

import settings

app = Flask(__name__)

SURNAME_DATA = {}
user_id_seq = 1


class RoutesForMock:

    @staticmethod
    @app.route('/get_surname/<name>', methods=['GET'])
    def get_user_surname(name):
        surname = SURNAME_DATA.get(name)
        if surname:
            return jsonify(surname), 200
        else:
            return jsonify(f'Surname for user {name} not found'), 404

    @staticmethod
    @app.route('/add_user', methods=['POST'])
    def create_user():
        global user_id_seq

        user_name = json.loads(request.data.decode())['name']
        surname_name = json.loads(request.data.decode())['surname']

        if user_name not in SURNAME_DATA:
            SURNAME_DATA[user_name] = (surname_name, user_id_seq)

            data = {'user_id': user_id_seq}
            user_id_seq += 1
            return jsonify(data), 201
        else:
            return jsonify(f'User name {user_name} already exists: if {SURNAME_DATA[user_name]}'), 400

    @staticmethod
    @app.route('/shutdown')
    def shutdown():
        ActionWithMock.shutdown_mock()
        return jsonify(f'OK, exiting'), 200

    @staticmethod
    @app.route('/delete_by_surname/<name>', methods=['DELETE'])
    def delete_user_by_name(name):

        if SURNAME_DATA.get(name):
            SURNAME_DATA.pop(name)
            return jsonify(f"User '{name}' was deleted!"), 200
        else:
            return jsonify(f"User '{name}' not found"), 404

    @staticmethod
    @app.route('/update_user_surname$user_name=<name>$user_surname=<surname>', methods=["PUT"])
    def update_user_surname(name, surname):
        if SURNAME_DATA.get(name):
            SURNAME_DATA[name] = surname
            return jsonify(f"User '{name}' was updated by surname '{surname}'"), 200
        else:
            return jsonify(f"User '{name}' not found"), 404


class ActionWithMock:

    def __init__(self):
        self.host = settings.MOCK_HOST
        self.port = settings.MOCK_PORT

    def run_mock(self):
        server = threading.Thread(target=app.run, kwargs={
            'host': self.host,
            'port': self.port
        })
        server.start()
        return server

    @staticmethod
    def shutdown_mock():
        terminate_func = request.environ.get('werkzeug.server.shutdown')
        if terminate_func:
            terminate_func()
