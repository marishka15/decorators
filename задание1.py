import os
import datetime
from functools import wraps

list_element = []
def logger(old_function):
    @wraps(old_function)
    def new_function(*args, **kwargs):
        name_function = old_function.__name__
        arguments = f'{args} и {kwargs}'
        date_time = datetime.datetime.now()
        result = old_function(*args, **kwargs)

        elements = {
            'name': name_function,
            'data': str(date_time),
            'arguments': arguments,
            'result': result
        }
        list_element.append(elements)

        with open('main.log', 'w', encoding='utf-8') as log_file_:
            for line in list_element:
                log_file_.write(f"Сейчас будет вызвана функция {line['name']}\n")
                log_file_.write(f"Текущая дата и время вызова функции: {line['data']}\n")
                log_file_.write(f"C аргументами {line['arguments']}\n")
                log_file_.write(f"Возращаемое значение: {line['result']}\n\n")

        return result
    return new_function


def test_1():
    path = 'main.log'
    if os.path.exists(path):
        os.remove(path)

    @logger
    def hello_world():
        return 'Hello World'

    @logger
    def summator(a, b=0):
        return a + b

    @logger
    def div(a, b):
        return a / b

    assert 'Hello World' == hello_world()
    result = summator(2, 2)
    assert isinstance(result, int)
    assert result == 4, '2 + 2 = 4'
    result = div(6, 2)
    assert result == 3, '6 / 2 = 3'

    assert os.path.exists(path)

    summator(4.3, b=2.2)
    summator(a=0, b=0)

    with open(path) as log_file:
        log_file_content = log_file.read()

    assert 'summator' in log_file_content
    for item in (4.3, 2.2, 6.5):
        assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_1()


