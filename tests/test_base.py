import jinja2
from server import server
from setup import base_config
from email.mime.multipart import MIMEMultipart
from script import get_sheet_data, config_template, make_letters


class Test_basics:
    def test_base_config(self):
        assert len(base_config) == 9

    def test_base_config_email(self):
        assert base_config.get('from', '') != ''
        assert base_config.get('from', '').__contains__('@')

    def test_server(self):
        assert type(server.noop()) == tuple
        assert server.noop()[1] == b'OK'

    def test_load_excel_type(self):
        assert type(get_sheet_data()) == list

    def test_load_excel_size(self):
        assert len(get_sheet_data()) == 3

    def test_load_template(self):
        assert type(config_template()) == jinja2.Template

    def test_make_letters_exist(self):
        assert make_letters(get_sheet_data())[0].get('body', False) != False

    def test_make_letters_type(self):
        assert type(make_letters(get_sheet_data())[0].get('body', False)) == MIMEMultipart
