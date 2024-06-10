from setup import logger, base_config
# from script import process_letters


def start():
    """
    Обертка для получения подтверждения от пользователя
    """
    print('Скрипт будет запущен со следующими параметрами:')
    for k, v in base_config.items():
        print(f'\t {k}: {v}')
    print('Все верно, начинаем? y/n д/н')

    answer = input().lower()    # ломается если кириллица и стереть символ
    answer = 'n'
    if answer in ['y', 'д']:
        from script import process_letters  # импорт здесь ради чтобы не выглядел зависшим, если smtp сервер тупит
        process_letters()
    else:
        print('Информация о параметрах: --help')


# Запуск основного скрипта
start()
