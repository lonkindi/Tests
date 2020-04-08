import json
import os

documents = list()
directories = dict()


def load_data():
    global documents, directories
    current_path = str(os.path.dirname(os.path.abspath(__file__)))
    path_dirs = os.path.join(current_path, 'fixtures', 'directories.json')
    path_docs = os.path.join(current_path, 'fixtures', 'documents.json')
    # path_dirs = os.path.join('fixtures', 'directories.json')
    # print(path_docs)
    with open(path_docs, 'r', encoding='utf-8') as docs:
        documents = json.load(docs)
    with open(path_dirs, 'r', encoding='utf-8') as dirs:
        directories = json.load(dirs)
    return documents, directories


# documents = [
#     {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
#     {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
#     {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
# ]
# directories = {
#     '1': ['2207 876234', '11-2', '5455 028765'],
#     '2': ['10006', '5400 028765', '5455 002299'],
#     '3': []
# }
commands = {
    'p': 'people – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит',
    'l': 'list – команда, которая выведет список всех документов',
    's': 'shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится',
    'a': 'add – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, '
         'имя владельца и номер полки, на которой он будет храниться',
    'd': 'delete – команда, которая спросит номер документа и удалит его из каталога и из перечня полок',
    'm': 'move – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую',
    'as': 'add shelf – команда, которая спросит номер новой полки и добавит ее в перечень',
    'h': 'help - выводит список доступных команд и их краткое описание',
    'q': 'quit - завершение работы программы'
}


def verify_command(command):
    if command in commands:
        return True
    else:
        print('Введённая команда не найдена, посмотрите список доступных команд (используйте команду h для просмотра '
              'подробного описания каждой из них):')
        show_commands()


def check_empty_input(user_input):
    after_strip = user_input.strip()
    if after_strip == '':
        print('Введено пустое значение!')
        return False
    else:
        return True


def show_commands(short=True):
    for command in commands:
        print(f'{command}', end=' - ')
        if not short:
            print(f'{commands[command]}')
    print('\n')


def find_people_by_docnumber():
    docnumber = input('Введите номер документа для поиска его владельца:>').strip()
    if check_empty_input(docnumber):
        found_doc = None
        for document in documents:
            if docnumber == document['number']:
                found_doc = document
        if found_doc:
            print(f'Владельцем документа №{docnumber} является {found_doc["name"]}')
        else:
            ins_doc = input(f'Документ №{docnumber} не найден, хотите его добавить? (Y/N):>').upper()
            if ins_doc == 'Y':
                add_doc()


def find_shelf_by_docnumber():
    docnumber = input('Введите номер документа для поиска его номера полки:>')
    if check_empty_input(docnumber):
        found_shelf = None
        for shelf in directories:
            if docnumber in directories[shelf]:
                found_shelf = shelf
        if found_shelf:
            print(f'Документ №{docnumber} хранится на полке №{found_shelf}')
        else:
            ins_doc = input(f'Документ №{docnumber} не найден, хотите его добавить? (Y/N):>').upper()
            if ins_doc == 'Y':
                add_doc()


def add_doc():
    parameters = tuple(map(str, input('Введите номер, тип, имя владельца документа и номер полки его хранения через '
                                      'точку с запятой:>').split(sep=';')))
    if len(parameters) == 4:
        found_doc = False
        found_shelf = False
        for document in documents:
            if parameters[0] == document['number']:
                found_doc = True
        if directories.get(parameters[3]) != None:
            found_shelf = True
        if found_doc:
            print(f'Документ №{parameters[0]} уже существует, проверьте вводимые данные.')
        elif not found_shelf:
            ins_shelf = input(f'Полка №{parameters[3]} не существует, хотите добавить новую полку? (Y/N):>').upper()
            if ins_shelf == 'Y':
                add_or_clear_shelf()
        else:
            documents.append({"type": parameters[1], "number": parameters[0], "name": parameters[2]})
            directories[parameters[3]].append(parameters[0])
            print(f'Документ №{parameters[0]} успешно добавлен в каталог и на полку №{parameters[3]}')
    else:
        print(f'Необходимо ввести ровно четыре параметра через точку с запятой, не больше и не меньше...')


def delete_doc():
    doc_number = input('Введите номер документа для удаления:>')
    if check_empty_input(doc_number):
        doc_found = None
        shelf_found = None
        for shelf in directories:
            curr_dir = directories[shelf]
            if doc_number in directories[shelf]:
                shelf_found = shelf
        for doc in documents:
            if doc_number == doc['number']:
                doc_found = doc
        if shelf_found is not None and doc_found is not None:
            documents.remove(doc_found)
            shelf_content = directories[shelf_found]
            shelf_content.remove(doc_number)
            directories[shelf_found] = shelf_content
            print('Удалён документ №', doc_number)
        elif shelf_found != None and doc_found == None:
            shelf_content = directories[shelf_found]
            shelf_content.remove(doc_number)
            directories[shelf_found] = shelf_content
            print(f'Документ с номером {doc_number} не найден, но числится на полке. Документ удалён с полки.')
        elif shelf_found == None and doc_found == None:
            print(f'Документ с номером {doc_number} не найден, возможно он был удалён ранее.')
        elif doc_found != None and shelf_found == None:
            doc_to_shelf = input(f'Документ №{doc_number} существует, но не привязан к полке. Хотите поместить его '
                                 f'на полку? (Y/N):>').upper()
            if doc_to_shelf == 'Y':
                move_doc()


def move_doc():
    parameters = tuple(map(str, input('Введите номер документа и номер полки, куда его переметить, через точку с '
                                      'запятой:>').split(sep=';')))
    if len(parameters) == 2:
        found_doc = None
        found_shelf = None
        number_shelf = None
        if directories.get(parameters[1]) != None:
            found_shelf = parameters[1]
        for shelf in directories:
            if parameters[0] in directories[shelf]:
                found_doc = parameters[0]
                number_shelf = shelf
        if not found_doc:
            ins_doc = input(f'Документ №{parameters[0]} не найден, хотите добавить этот документ? (Y/N):>').upper()
            if ins_doc == 'Y':
                add_doc()
        elif not found_shelf:
            ins_shelf = input(f'Полка №{parameters[1]} не найдена, хотите добавить новую полку? (Y/N):>').upper()
            if ins_shelf == 'Y':
                add_or_clear_shelf()
        elif number_shelf == parameters[1] and found_doc:
            print(f'Документ №{parameters[0]} уже находится на полке №{parameters[1]}')
        else:
            directories[number_shelf].remove(parameters[0])
            directories[parameters[1]].append(parameters[0])
            print(f'Документ №{parameters[0]} перемещён на полку №{parameters[1]}')
    else:
        print(f'Необходимо ввести ровно два параметра через точку с запятой, не больше и не меньше...')


def add_or_clear_shelf():
    shelf_number = input('Введите номер добавляемой полки:>')
    if check_empty_input(shelf_number):
        if directories.get(shelf_number) == None:
            directories[shelf_number] = []
            print(f'Полка № {shelf_number} успешно добавлена')
        else:
            clear_shelf = input(f'Полка с номером {shelf_number} уже существует. Хотите её очистить? (Y/N):>').upper()
            if clear_shelf == 'Y':
                directories[shelf_number] = []


def show_all_docs():
    for doc in documents:
        print(f'№{doc["number"]}, документ имеет тип: {doc["type"]}, а его владелец {doc["name"]}')


def main():
    load_data()
    while True:
        user_command = input('Введите команду и нажмите Enter:>')
        if check_empty_input(user_command) and verify_command(user_command):
            if user_command == 'q':
                print('Работа с программой завершена.')
                break
            elif user_command == 'p':
                find_people_by_docnumber()
            elif user_command == 'l':
                show_all_docs()
            elif user_command == 's':
                find_shelf_by_docnumber()
            elif user_command == 'a':
                add_doc()
            elif user_command == 'd':
                delete_doc()
            elif user_command == 'm':
                move_doc()
            elif user_command == 'as':
                add_or_clear_shelf()
            elif user_command == 'h':
                show_commands(False)


if __name__ == '__main__':
    main()
