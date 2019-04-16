from argparse import ArgumentParser
import json
import http.client
from departs import Departs
from gdocs import Gdocs


class Request:

    def __init__(self, addr, port, url,  login, password):
        self.address = addr
        self.login = login
        self.password = password
        self.port = port
        self.url = url

    def check(self):
        if self.address is None:
            self.address = input('Виведите адрес сервере (в формате test.ru или IP адрес): ')
        if self.port is None:
            port = input('Виведите номер порта: ')
            try:
                self.port = int(port)
            except ValueError:
                print('Введен не верный номер порта.')
                exit(-1)
        if self.login is None:
            self.login = input('UserName: ')
        if self.password is None:
            self.password = input('Password: ')
        body = {'UserName': self.login, 'Password': self.password}
        headers = {"Content-type": "application/json"}
        conn = http.client.HTTPConnection(self.address, self.port, timeout=10)
        try:
            conn.request('POST', '/api/sh5info', json.dumps(body), headers)
        except ValueError:
            print('Сервер не доступен')
            conn.close()
            exit(-1)
        response = conn.getresponse()
        data = response.read()
        conn.close()
        data = json.loads(data.decode('utf-8'))
        if data['errorCode'] == 1:
            print(data['errMessage'])
            exit(-1)

    def send(self, proc_name, request={}):
        body = {'UserName': self.login, 'Password': self.password, 'procName': proc_name}
        body.update(request)
        headers = {"Content-type": "application/json"}
        conn = http.client.HTTPConnection(self.address, self.port)
        conn.request('POST', self.url, json.dumps(body), headers)
        response = conn.getresponse()
        if response.status != 200:
            return None
        data = response.read()
        conn.close()
        data = data.decode('utf-8')
        return json.loads(data)


class KppDeparts:

    def __init__(self, request) -> None:
        super().__init__()
        self.req = request


if __name__ == '__main__':
    parser = ArgumentParser(description='Connection to storehouse')

    parser.add_argument('-s', '--server', type=str, default=None,
                        dest='server', help='address of server for connection')
    parser.add_argument('-o', '--port', type=int, default=None,
                        dest='port', help='port of server for connection')

    parser.add_argument('-l', '--login', type=str, default=None,
                        dest='login', help='username for connection to server')
    parser.add_argument('-p', '--password', type=str, default=None,
                        dest='password', help='password for connection to server')

    args = parser.parse_args()
    req = Request(args.server, args.port, '/api/sh5exec', args.login, args.password)
    req.check()

    departs = Departs(req)
    departs.update()
    print('Выбор критерий поиска:')
    find = departs.choose_depart()
    print(find)

    print('\nЗаменить на:')
    replace = departs.choose_depart()
    print(replace)

    docs = Gdocs(req, find, replace)
    docs.update()
    docs.replace()
