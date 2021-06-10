import os

from flask import Flask, jsonify


app = Flask(__name__)

SURNAME_DATA = {}
user_id_seq = 1


class RoutesForMock:

    @staticmethod
    @app.route('/vk_id/<name>', methods=['GET'])
    def get_user_surname(name):
        if len(name) == 7:
            return jsonify({'vk_id': 12345}), 200
        elif len(name) == 8:
            return jsonify({'vk_id': name}), 200
        else:
            return jsonify(f'Surname for user {name} not found'), 404


if __name__ == '__main__':
    host = os.environ.get('STUB_HOST', '0.0.0.0')
    port = os.environ.get('STUB_PORT', '8090')

    app.run(host, port)