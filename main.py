from argparse import ArgumentParser
import json
import http.client
from departs import Departs
from gdocs import Gdocs


class Request:

    def __init__(self, addr, port=80, url='/',  login='admin', password='admin'):
        self.address = addr
        self.login = login
        self.password = password
        self.port = port
        self.url = url

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
        # print(data.decode('utf8'))
        data = data.decode('utf-8')
        return json.loads(data)


class KppDeparts:

    def __init__(self, request) -> None:
        super().__init__()
        self.req = request


if __name__ == '__main__':
    parser = ArgumentParser(description='Connection to storehouse')

    parser.add_argument('-s', '--server', required=True, type=str,
                        dest='server', help='address of server for connection')
    parser.add_argument('-o', '--port', type=int, default=80,
                        dest='port', help='port of server for connection')

    parser.add_argument('-l', '--login', required=True, type=str,
                        dest='login', help='username for connection to server')
    parser.add_argument('-p', '--password', required=True, type=str,
                        dest='password', help='password for connection to server')

    args = parser.parse_args()
    req = Request(args.server, args.port, '/api/sh5exec', args.login, args.password)
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
