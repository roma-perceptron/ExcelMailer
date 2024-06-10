from sys import exit
from setup import logger
from socket import gaierror
from smtplib import SMTPAuthenticationError
from jinja2.exceptions import TemplateNotFound


def error_handler(func):
    """
    Декоратор для отлова и регистрации ошибок прерывающих работу скрипта полностью
    """
    def wrapper(*args, **kwargs):
        try:
            res = func(*args, **kwargs)
            return res
        except FileExistsError as exp:
            logger.error(f'Excel файл не найден {exp}')
        except gaierror as exp:
            logger.error(f'Невозможно подключиться к smtp серверу, проверьте адрес и хост {exp}')
        except SMTPAuthenticationError as exp:
            logger.error(f'Неверные логин и/или пароль {exp}')
        except TemplateNotFound as exp:
            logger.error(f'Файл шаблона не найден {exp}')
        except Exception as exp:
            logger.error(f'Иная ошибка {exp}')
        #
        # Если было исключение, прерываю работу скрипта
        exit()
    #
    return wrapper
