from builtins import print

from departs import get_obj


def get_index_field(store: list, name: str):
    try:
        return store.index(name)
    except ValueError:
        return None


class Gdocs:
    def __init__(self, request, condition, replace) -> None:
        super().__init__()
        self.req = request
        self.cond = condition
        self.repl = replace
        self.obj111 = None
        self.count = 0

    def update(self):
        body = {'Input': [
            {
                'head': '108',
                'original': ['111\\\\8'],
                'values': [[15667]]
            },
            {
                'head': '106#10',
                'original': ['1'],
                'values': [[self.cond[0]]]
            }
        ]}
        docs = self.req.send('GDocs', body)
        if docs['errorCode'] != 0:
            print('Ошибка при запросе списка накладных.')
            print(docs)
            exit(-1)
        self.obj111 = get_obj(docs['shTable'], '111')
        if self.obj111 is None:
            print('Объекты 111 не найден при запросе списка накладных.')
            exit(-1)
        print('Найдено ' + str(len(self.obj111['values'][0])) + ' накладных')

    def replace(self):
        user_answer = input('Произвести замену? (yes/no): ')
        if user_answer == 'no' or user_answer != 'yes':
            print('Отменено пользователем')
            exit(0)
        values = self.obj111['values']
        original = self.obj111['original']

        doc_worker = DocWorker(self.req, self.cond, self.repl)
        index_type = get_index_field(original, '5')
        index_id = get_index_field(original, '1')
        for i in range(len(values[0])):
            ok = doc_worker.process(values[index_type][i], values[index_id][i])
            if ok:
                self.count = self.count + 1
        print('Обновлено записей: ' + str(self.count))


class DocWorker:

    def __init__(self, request, cond, replace) -> None:
        super().__init__()
        self.request = request
        self.cond = cond
        self.rep = replace

    def getdoc(self, proc, index):
        body = {'Input': [{'head': '111', 'original': ['1'], 'values': [[index]]}]}
        doc = self.request.send(proc, body)
        if doc['errorCode'] == 1:
            return None
        return get_obj(doc['shTable'], '111')

    def replace(self, obj111: dict) -> dict:
        #  RID         Name        Flag         RID KPP          Name KPP
        # '105\\1',   '105\\3',   '105\\31',   '105\\114\\1',   '105\\114\\3'
        # '105#1\\1', '105#1\\3', '105#1\\31', '105#1\\114\\1', '105#1\\114\\3'
        f = False
        names_fields = obj111['original']
        values = obj111['values']
        i_rid = get_index_field(names_fields, '105\\1')
        i_kpp = get_index_field(names_fields, '105\\114\\1')
        if i_rid is not None and i_kpp is not None and \
                values[i_rid][0] == self.cond[0] and \
                values[i_kpp][0] == self.cond[1]:
            values[i_rid] = [self.rep[0]]
            values[i_kpp] = [self.rep[1]]
            f = True

        i_rid = get_index_field(names_fields, '105#1\\1')
        i_kpp = get_index_field(names_fields, '105#1\\114\\1')
        if i_rid is not None and i_kpp is not None and \
                values[i_rid][0] == self.cond[0] and \
                values[i_kpp][0] == self.cond[1]:
            values[i_rid] = [self.rep[0]]
            values[i_kpp] = [self.rep[1]]
            f = True

        if not f:
            return {}
        obj111.pop('fields', None)
        # obj111.update(values=values)
        return obj111

    def write_obj(self, proc_name, obj):
        body = {'Input': [obj]}
        return self.request.send(proc_name, body)

    def process(self, type_doc, index) -> bool:
        if type_doc in [1, 10, 13]:
            return False
        obj111 = self.getdoc('GDoc' + str(type_doc), index)
        new_obj111 = self.replace(obj111)
        if not new_obj111:
            return False
        result = self.write_obj('UpdGDoc' + str(type_doc), new_obj111)
        if result['errorCode'] != 0:
            print('write GDoc' + str(type_doc) + ' id:' + str(index) + ' запись не удачна')
            print(result)
            return False
        return True
