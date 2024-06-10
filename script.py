import xlrd
from os import path
from tqdm import tqdm
from server import server
from setup import logger, base_config
from utils import error_handler
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Environment, FileSystemLoader, select_autoescape


# Жестко заданный порядок и имена полей-столбцов. В Excel они могут называться иначе, но должны идти в таком порядке
STANDARD_COLS = ('name', 'last_name', 'second_name', 'email', 'appeal')


@error_handler
def get_sheet_data(excel_file=path.join(base_config['_dir'], base_config['file']), sheet_no=base_config['sheet'], fields=STANDARD_COLS):
    """
    Чтение заданного Excel файла и сбор данных
    :param excel_file: имя(путь) к Excel файлу
    :param sheet_no: номер листа в файле
    :param fields: список полей которыми будут поименованы данные в строке
    :return: список словарей с данными о получателе
    """
    workbook = xlrd.open_workbook(excel_file)
    sheet = workbook.sheet_by_index(sheet_no)

    data = []
    for row_index in range(1, sheet.nrows):
        row = sheet.row(row_index)
        data.append(
            {
                fields[n]: row[n].value.strip() for n in range(len(row))
            }
        )
    if data:
        logger.info(f'В Excel файле найдено строк с данными: {len(data)}')
    else:
        logger.warn(f'В Excel файле данных не обнаружено!')
    return data


@error_handler
def config_template(template_file=base_config['template']):
    """
    Загрузка шаблона письма для последующего заполнения
    :param template_file: имя(путь) к файлу-шаблону
    :return: объект класса Template
    """
    env = Environment(
        loader=FileSystemLoader(path.join(base_config['_dir'], 'templates')),
        autoescape=select_autoescape()
    )
    template = env.get_template(template_file)
    return template


def make_letters(data):
    """
    Заполнение шаблона для каждого письма и формирование объекта-письма для отправки
    :param data: список словарей с данными
    :return: список словарей с обновленными данными
    """
    template = config_template()

    letters = []
    for item in data:
        try:
            # Формирование письма
            letter = MIMEMultipart()
            letter['From'] = base_config['from']
            letter['To'] = item['email']
            letter['Subject'] = base_config['theme']
            letter.attach(MIMEText(template.render(item), 'plain'))
            item['body'] = letter
            letters.append(item)
        except BaseException as exp:
            logger.error(f'Ошибка на этапе формирования письма для {item["email"]}. Пропускаю. {exp}')
    return letters


def send_letters(letters):
    """
    Отправка писем, по одному за раз
    :param letters: список словарей с данными для отправки
    """
    sended = 0
    if letters:
        for letter in tqdm(letters):
            try:
                server.sendmail(base_config['from'], letter['email'], letter['body'].as_string())
                logger.info(f'Письмо для {letter["email"]} успешно отправлено!')
                sended += 1
            except Exception as exp:
                logger.warn(f'Письмо для {letter["email"]} не отправлено. Ошибка: {exp}')
        server.quit()
    else:
        logger.warn('Писем для отправки не было сформировано.')
    return sended


def process_letters():
    """
    Запуск полного цикла обработки excel файла и отправки писем
    """
    sended = send_letters(
        make_letters(
            get_sheet_data()
        )
    )
    logger.info(f'Работа скрипта завершена, отправлено писем {sended}')
    print(f'Работа скрипта завершена, отправлено писем {sended}. Подробности в log-файле.')


