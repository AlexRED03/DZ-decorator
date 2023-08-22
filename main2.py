import os
import logging


def logger(path):
    name = path
    py_logger = logging.getLogger(__name__)
    py_logger.setLevel(logging.INFO)
    py_handler = logging.FileHandler(name, mode='a')
    py_formatter = logging.Formatter("%(name)s %(asctime)s %(levelname)s %(message)s")
    py_handler.setFormatter(py_formatter)
    py_logger.addHandler(py_handler)

    def __logger(old_function):
        # _cache = {}

        def new_function(*args, **kwargs):
            # key = f'{args}_{kwargs}'
            result = old_function(*args, **kwargs)
            # _cache[key] = result
            py_logger.info(args)
            py_logger.info(kwargs)
            py_logger.info(result)
            py_logger.info(old_function)
            return result

        return new_function

    return __logger


def test_2():
    paths = ('log_1.log', 'log_2.log', 'log_3.log')

    for path in paths:
        # if os.path.exists(path):
        #     os.remove(path)

        @logger(path)
        def hello_world():
            return 'Hello World'

        @logger(path)
        def summator(a, b=0):
            return a + b

        @logger(path)
        def div(a, b):
            return a / b

        assert 'Hello World' == hello_world(), "Функция возвращает 'Hello World'"
        result = summator(2, 2)
        assert isinstance(result, int), 'Должно вернуться целое число'
        assert result == 4, '2 + 2 = 4'
        result = div(6, 2)
        assert result == 3, '6 / 2 = 3'
        summator(4.3, b= 2.2)

    for path in paths:

        assert os.path.exists(path), f'файл {path} должен существовать'

        with open(path) as log_file:
            log_file_content = log_file.read()

        assert 'summator' in log_file_content, 'должно записаться имя функции'

        for item in (4.3, 2.2, 6.5):
            assert str(item) in log_file_content, f'{item} должен быть записан в файл'


if __name__ == '__main__':
    test_2()