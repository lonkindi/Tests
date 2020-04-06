import unittest
import json
import app
import sys
from io import StringIO
from unittest.mock import patch


class TestApp(unittest.TestCase):

    def setUp(self):
        with open(r'..\fixtures\documents.json', 'r', encoding='utf-8') as docs:
            self.doc = json.load(docs)
        with open(r'..\fixtures\directories.json', 'r', encoding='utf-8') as dirs:
            self.dir = json.load(dirs)
        self.commands = app.commands

    def test_verify_command(self):
        with patch('app.input', return_value='q'):
            return_val1 = app.verify_command('z')
            return_val2 = app.verify_command('l')
        self.assertFalse(return_val1)
        self.assertTrue(return_val2)

    def test_check_empty_input(self):
        return_val1 = app.check_empty_input('')
        return_val2 = app.check_empty_input('l')
        self.assertFalse(return_val1)
        self.assertTrue(return_val2)

    def test_show_commands(self):
        test_str = 'p - l - s - a - d - m - as - h - q -'
        with patch('sys.stdout', new=StringIO()) as printOutput:
            app.show_commands()
            output = printOutput.getvalue().strip()
        self.assertEqual(output, test_str)

    def test_find_people_by_docnumber(self):
        def not_find_people_by_docnumber(*a, **kw):
            print(*a)
            return '1000'

        test_str = 'Владельцем документа №10006 является Аристарх Павлов'
        with patch('app.input', return_value='10006'):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.find_people_by_docnumber()
                output = printOutput.getvalue().strip()
            self.assertEqual(output, test_str)

        test_str2 = 'Документ №1000 не найден, хотите его добавить? (Y/N):>'
        with patch('app.input', side_effect=not_find_people_by_docnumber):
            with patch('sys.stdout', new=StringIO()) as printOutput2:
                app.find_people_by_docnumber()
                output2 = printOutput2.getvalue().strip()
            self.assertIn(test_str2, output2)

    def test_find_shelf_by_docnumber(self):
        def not_find_shelf_by_docnumber(*a, **kw):
            print(*a)
            return '1'

        test_str = 'Документ №10006 хранится на полке №2'
        with patch('app.input', return_value='10006'):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.find_shelf_by_docnumber()
                output = printOutput.getvalue().strip()
            self.assertEqual(output, test_str)

        test_str2 = 'Документ №1 не найден, хотите его добавить? (Y/N):>'
        with patch('app.input', side_effect=not_find_shelf_by_docnumber):
            with patch('sys.stdout', new=StringIO()) as printOutput2:
                app.find_people_by_docnumber()
                output2 = printOutput2.getvalue().strip()
            self.assertIn(test_str2, output2)

    def test_add_doc(self):
        def add_doc_normal(*a, **kw):
            print(*a)
            return '1111;certificate;Лора Палмер;2'

        def add_doc_exist(*a, **kw):
            print(*a)
            return '1111;certificate;Лора Палмер;2'

        def add_doc_not_shelf(*a, **kw):
            print(*a)
            return '11111;certificate;Лора Палмер;5'

        def add_doc_bad_param(*a, **kw):
            print(*a)
            return '111;certificate;Лора Палмер;2;2'

        old_len_docs = len(app.documents)
        test_str = 'Документ №1111 успешно добавлен в каталог и на полку №2'
        with patch('app.input', side_effect=add_doc_normal):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.add_doc()
                output = printOutput.getvalue().strip()
            new_len_docs = len(app.documents)
            self.assertGreater(new_len_docs, old_len_docs)
            self.assertIn(test_str, output)

        old_len_docs = len(app.documents)
        test_str = 'Документ №1111 уже существует, проверьте вводимые данные'
        with patch('app.input', side_effect=add_doc_exist):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.add_doc()
                output = printOutput.getvalue().strip()
            new_len_docs = len(app.documents)
            self.assertEqual(new_len_docs, old_len_docs)
            self.assertIn(test_str, output)

        old_len_docs = len(app.documents)
        test_str = 'Полка №5 не существует, хотите добавить новую полку? (Y/N):>'
        with patch('app.input', side_effect=add_doc_not_shelf):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.add_doc()
                output = printOutput.getvalue().strip()
            new_len_docs = len(app.documents)
            self.assertEqual(new_len_docs, old_len_docs)
            self.assertIn(test_str, output)

        old_len_docs = len(app.documents)
        test_str = 'Необходимо ввести ровно четыре параметра через точку с запятой, не больше и не меньше...'
        with patch('app.input', side_effect=add_doc_bad_param):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.add_doc()
                output = printOutput.getvalue().strip()
            new_len_docs = len(app.documents)
            self.assertEqual(new_len_docs, old_len_docs)
            self.assertIn(test_str, output)

    def test_delete_doc(self):
        def delete_doc_normal(*a, **kw):
            print(*a)
            return '10006'

        def delete_doc_not_exist(*a, **kw):
            print(*a)
            return '1000'

        def delete_doc_not_in_shelf(*a, **kw):
            print(*a)
            return '100'

        def delete_doc_not_in_docs(*a, **kw):
            print(*a)
            return '10'


if __name__ == '__main__':
    unittest.runner()
