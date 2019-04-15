from departs import get_obj


class Gdocs:
    def __init__(self, request, condition, replace) -> None:
        super().__init__()
        self.req = request
        self.cond = condition
        self.repl = replace
        self.obj111 = None

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
        doc_worker = DocWorker(self.req)
        for i in range(len(values[0])):
            doc_worker.dispatch(values[2][i], values[0][i])
            input('next')


class DocWorker:

    def __init__(self, request) -> None:
        super().__init__()
        self.req = request

    def dispatch(self, value, index):
        method_name = 'process_doc' + str(value)
        method = getattr(self, method_name)
        method(index)

    def getdoc(self, proc, index):
        body = {'Input': [{'head': '111', 'original': ['1'], 'values': [[index]]}]}
        doc = self.req.send(proc, body)
        if doc['errorCode'] == 1:
            return None
        return get_obj(doc['shTable'], '111')

    def process_doc0(self, index):
        doc = self.getdoc('GDoc0', index)
        print(doc)
        print('process_doc0 - ' + str(index))

    def process_doc1(self, index):
        print('process_doc1 - ' + str(index))

    def process_doc4(self, index):
        print('process_doc4 - ' + str(index))

    def process_doc5(self, index):
        print('process_doc5 - ' + str(index))

    def process_doc8(self, index):
        print('process_doc8 - ' + str(index))

    def process_doc10(self, index):
        print('process_doc10 - ' + str(index))

    def process_doc11(self, index):
        print('process_doc11 - ' + str(index))

    def process_doc12(self, index):
        print('process_doc12 - ' + str(index))

    def process_doc13(self, index):
        print('process_doc13 - ' + str(index))
