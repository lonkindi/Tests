import unittest
import app
import importlib
from io import StringIO
from unittest.mock import patch


class TestApp(unittest.TestCase):

    def setUp(self):
        importlib.reload(app)
        documents, directories = app.load_data()
        self.docs = documents
        self.dirs = directories
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
        def doc_not_in_shelf(*a, **kw):
            print(*a)
            return '100'

        old_len_docs = len(app.documents)
        test_str = 'Удалён документ № 11-2'
        with patch('app.input', return_value='11-2'):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.delete_doc()
                output = printOutput.getvalue().strip()
            new_len_docs = len(app.documents)
            self.assertGreater(old_len_docs, new_len_docs)
            self.assertEqual(output, test_str)

        old_len_docs = len(app.documents)
        test_str = 'Документ с номером 1000 не найден, возможно он был удалён ранее.'
        with patch('app.input', return_value='1000'):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.delete_doc()
                output = printOutput.getvalue().strip()
            new_len_docs = len(app.documents)
            self.assertEqual(old_len_docs, new_len_docs)
            self.assertEqual(output, test_str)

        old_len_docs = len(app.documents)
        test_str = 'Документ с номером 10 не найден, но числится на полке. Документ удалён с полки.'
        with patch('app.input', return_value='10'):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.delete_doc()
                output = printOutput.getvalue().strip()
            new_len_docs = len(app.documents)
            self.assertEqual(old_len_docs, new_len_docs)
            self.assertEqual(output, test_str)

        old_len_docs = len(app.documents)
        test_str = f'Документ №100 существует, но не привязан к полке. Хотите поместить его на полку? (Y/N):>'
        with patch('app.input', return_value='100'):
            with patch('app.input', side_effect=doc_not_in_shelf):
                with patch('sys.stdout', new=StringIO()) as printOutput:
                    app.delete_doc()
                    output = printOutput.getvalue().strip()
                new_len_docs = len(app.documents)
                self.assertEqual(old_len_docs, new_len_docs)
                self.assertIn(test_str, output)

    def test_move_doc(self):
        def f_shelf(num_doc):
            num_shelf = None
            for item in app.directories:
                if num_doc in app.directories[item]:
                    num_shelf = item
            return num_shelf

        def len_shelf(num_shelf):
            len_s = None
            if app.directories.get(num_shelf):
                len_s = len(app.directories[num_shelf])
            return len_s

        def move_doc_normal(*a, **kw):
            print(*a)
            return '11-2;2'

        def move_doc_not_exist(*a, **kw):
            print(*a)
            return '1111;2'

        def move_doc_not_shelf(*a, **kw):
            print(*a)
            return '11-2;5'

        def move_doc_in_shelf(*a, **kw):
            print(*a)
            return '10;2'

        def move_doc_bad_param(*a, **kw):
            print(*a)
            return '1'

        dep_num = f_shelf('11-2')
        old_dep_len = len_shelf(dep_num)
        old_dist_len = len_shelf('2')
        test_str = 'Документ №11-2 перемещён на полку №2'
        with patch('app.input', side_effect=move_doc_normal):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.move_doc()
                new_dep_len = len_shelf(dep_num)
                new_dis_len = len_shelf('2')
                output = printOutput.getvalue().strip()
            self.assertGreater(old_dep_len, new_dep_len)
            self.assertGreater(new_dis_len, old_dist_len)
            self.assertIn(test_str, output)

        old_dist_len = len_shelf('2')
        test_str = 'Документ №1111 не найден, хотите добавить этот документ? (Y/N):>'
        with patch('app.input', side_effect=move_doc_not_exist):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.move_doc()
                new_dis_len = len_shelf('2')
                output = printOutput.getvalue().strip()
            self.assertEqual(new_dis_len, old_dist_len)
            self.assertIn(test_str, output)


        test_str = 'Полка №5 не найдена, хотите добавить новую полку? (Y/N):>'
        with patch('app.input', side_effect=move_doc_not_shelf):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.move_doc()
                output = printOutput.getvalue().strip()
            self.assertIn(test_str, output)

        old_len = len_shelf('2')
        test_str = 'Документ №10 уже находится на полке №2'
        with patch('app.input', side_effect=move_doc_in_shelf):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.move_doc()
                output = printOutput.getvalue().strip()
            new_len = len_shelf('2')
            self.assertEqual(new_len, old_len)
            self.assertIn(test_str, output)

        test_str = 'Необходимо ввести ровно два параметра через точку с запятой, не больше и не меньше...'
        with patch('app.input', side_effect=move_doc_bad_param):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.move_doc()
                output = printOutput.getvalue().strip()
            self.assertIn(test_str, output)

    def test_add_or_clear_shelf(self):
        def doc_shelf_exist(*a, **kw):
            print(*a)
            return '1'

        old_len = len(app.directories)
        test_str = 'Полка № 5 успешно добавлена'
        with patch('app.input', return_value='5'):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.add_or_clear_shelf()
                output = printOutput.getvalue().strip()
            new_len = len(app.directories)
            self.assertGreater(new_len, old_len)
            self.assertIn(test_str, output)

        old_len = len(app.directories)
        test_str = 'Полка с номером 1 уже существует. Хотите её очистить? (Y/N):>'
        with patch('app.input', side_effect=doc_shelf_exist):
            with patch('sys.stdout', new=StringIO()) as printOutput:
                app.add_or_clear_shelf()
                output = printOutput.getvalue().strip()
            new_len = len(app.directories)
            self.assertEqual(new_len, old_len)
            self.assertIn(test_str, output)


if __name__ == '__main__':
    unittest.runner()
