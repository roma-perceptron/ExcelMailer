import smtplib
from utils import error_handler
from setup import logger, base_config


@error_handler
def config_smtpserver(sender_config):
    """
    Создание и конфигурирование менеджера SMTP-сервера
    :param sender_config:
    :return:
    """
    # Параметры для подключения к SMTP серверу
    smtp_server = sender_config['server']
    port = sender_config['port']
    sender_email = sender_config['from']
    password = sender_config['pass']

    # Аутентификация на сервере SMTP
    server = smtplib.SMTP_SSL(smtp_server, port)
    resp = server.login(sender_email, password)
    logger.info(f'Успешное подключение к SMTP-серверу: {resp}')
    #
    return server


# Создание объекта сервера-smtp
server = config_smtpserver(base_config)
