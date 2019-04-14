import json


def get_obj(objs, number):
    for obj in objs:
        if obj['head'] == number:
            return obj
    return None


class Departs:

    def __init__(self, request) -> None:
        super().__init__()
        self.obj106 = None
        self.req = request

    def update(self):
        deps = self.req.send('Departs')
        if deps['errorCode'] != 0:
            print('Список подразделений не получен.')
            print(deps)
            exit(-1)
        self.obj106 = get_obj(deps['shTable'], '106')
        if self.obj106 is None:
            print('Объект 106 не найден в ответе в получении списка подразделений.')
            exit(-1)

    def choose_depart(self):
        values = self.obj106['values']
        for i in range(len(values[0])):
            print('\t' + str(i) + '. ' + values[2][i])
        user_input = input('Выберите подразделение: ')
        try:
            index = int(user_input)
        except ValueError:
            index = -1
        if isinstance(index, int) and index not in range(len(values[0])):
            print('Выбор не верный.')
            exit(-1)
        depart_find = Depart(self.req, values[0][index])
        depart_find.update()
        kpp = depart_find.choose_kpp()
        return values[0][index], kpp


class Depart:

    def __init__(self, request, key) -> None:
        super().__init__()
        self.req = request
        self.key = key
        self.obj106 = None
        self.obj114 = None

    def update(self):
        body = {'Input': [
            {
                'head': '106',
                'original': ['1'],
                'values': [[self.key]]
             }
        ]}
        deps = self.req.send('Depart', body)
        if deps['errorCode'] != 0:
            print('Подразделение не найдено.')
            print(deps)
            exit(-1)
        self.obj114 = get_obj(deps['shTable'], '114')
        self.obj106 = get_obj(deps['shTable'], '106')
        if self.obj114 is None:
            print('Объект 114 не найден в ответе в получении подразделения.')
            exit(-1)
        if self.obj106 is None:
            print('Объект 106 не найден в ответе в получении подразделения.')
            exit(-1)

    def choose_kpp(self):
        values = self.obj114['values']
        for i in range(len(values[0])):
            if values[3][i] is None:
                kpp = ''
            else:
                kpp = values[3][i]
            if values[7][i] is None:
                name = ''
            else:
                name = values[7][i]
            print('\t' + str(i) + '. ' + kpp + ', ' + name)
        user_input = input('Выберите КПП: ')
        try:
            index = int(user_input)
        except ValueError:
            index = -1
        if isinstance(index, int) and index not in range(len(values[0])):
            print('Выбор не верный.')
            exit(-1)
        return values[0][index]
