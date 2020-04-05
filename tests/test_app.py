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
        test_str = 'Владельцем документа №10006 является Аристарх Павлов'
        with patch('app.input', return_value='10006'):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.find_people_by_docnumber()
                output = printOutput.getvalue().strip()
            self.assertEqual(output, test_str)
        test_str2 = 'Документ №1000 не найден, хотите его добавить? (Y/N):>'
        with patch('app.input', return_value='1000'):
            with patch('sys.stdout', new=StringIO()) as printOutput2:
                app.find_people_by_docnumber()
                output2 = printOutput2.getvalue().strip()
            self.assertEqual(output2, test_str2)

    def test_find_shelf_by_docnumber(self):
        test_str = 'Документ №10006 хранится на полке №2'
        with patch('app.input', return_value='10006'):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.find_shelf_by_docnumber()
                output = printOutput.getvalue().strip()
            self.assertEqual(output, test_str)



if __name__ == '__main__':
    unittest.runner()
