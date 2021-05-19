import json
import socket

import settings


class ClientError(Exception):
    pass


class SocketClient:

    def __init__(self):
        self.port = int(settings.MOCK_PORT)
        self.host = settings.MOCK_HOST

    def __socket_client(self, request):
        data = {}

        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            client.settimeout(0.1)
            client.connect((self.host, self.port))
            client.send(request.encode())

            total_data = []

            while True:
                data = client.recv(4096)
                if data:
                    total_data.append(data.decode())
                else:
                    break
            data = ''.join(total_data).splitlines()

        except ConnectionResetError as err:
            print("Server break connection: ", err)

        except (ValueError, socket.error) as err:
            raise ClientError("Find error in connection to server: ", err)

        finally:
            client.close()
            return data

    def get_user_info(self, name):

        params = f'/get_surname/{name}'
        request = f'GET {params} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'

        return self.__socket_client(request)

    def post_add_user(self, name, surname):

        body = json.dumps({'name': f'{name}', 'surname': f'{surname}'})
        headers = "POST /add_user HTTP/1.1\r\nHost: {host}\r\nContent-Length: {content_length}\r\nContent-Type: application/json\r\nConnection: close\r\n\r\n{body}\r\n\r\n"

        request = headers.format(content_length=len(body.encode()), host=str(self.host) + ":" + str(self.port), body=body)
        return self.__socket_client(request)

    def delete_user_by_name(self, name):

        params = f'/delete_by_surname/{name}'
        request = f'DELETE {params} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'

        return self.__socket_client(request)

    def put_user_new_surname(self, name, surname):

        params = f'/update_user_surname$user_name={name}$user_surname={surname}'
        request = f'PUT {params} HTTP/1.1\r\nHost:{self.host}\r\n\r\n'

        return self.__socket_client(request)
