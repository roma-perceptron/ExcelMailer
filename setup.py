import os
import logging
import argparse


# Конфигурирование и запуск логгера
logging.basicConfig(
    filename=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'base.log'),
    level=logging.INFO,
    format='%(asctime)s – %(levelname)s – %(filename)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


# Создание парсера аргументов командной строки
parser = argparse.ArgumentParser(description='Скрипт для автоматической рассылки писем по базе из Excel-файла')
parser.add_argument('-t', '--theme', type=str, help='Тема письма', default='Здоровье важнее всего')
parser.add_argument('-fa', '--from_address', type=str, help='Адрес почты отправителя', required=True)
parser.add_argument('-pw', '--password', type=str, help='Пароль от почты отправителя', required=True)
parser.add_argument('-p', '--port', type=str, help='Порт', default='465')
parser.add_argument('-s', '--server', type=str, help='Сервер SMTP', required=True)
parser.add_argument('-f', '--file_excel', type=str, help='Имя Excel файла', default='base.xls')
parser.add_argument('-es', '--excel_sheet', type=int, help='Индекс листа Excel файлы (нумерация с 0)', default=0)
parser.add_argument('-tt', '--template', type=str, help='Имя шаблона для письма', default='message_template.txt')

# Запуск парсера аргументов
args = parser.parse_args()

# Формирование словаря с параметрами конфигурации
base_config = {
    'theme': args.theme,
    'from': args.from_address,
    'pass': args.password,
    'port': args.port,
    'server': args.server,
    'file': args.file_excel,
    'sheet': args.excel_sheet,
    'template': args.template,
    '_dir': os.path.dirname(os.path.abspath(__file__))
}

# Логирование запуска
logger.info(f'Запуск с параметрами: {base_config}')