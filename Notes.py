from easygui import *
from Notes_functions import *

notes = load_notes()

msgbox("Вас приветствует программа для заметок")

while True:
    choices = ['Добавить заметку', 'Просмотреть все заметки',
               'Изменить заметку', 'Выборка по дате', 'Выборка по теме', 'Удалить заметку', 'Выход']
    choice = buttonbox("Выберите действие", "Стол заметок", choices)

    if choice == 'Добавить заметку':
        msg = "Введите заметку"
        title = "Карточка заметки"
        field_names = ["Тема заметки", "Заголовок", "Тело заметки"]
        field_values = multenterbox(msg, title, field_names)

        if field_values:
            add_notes(notes, field_values)
            msgbox("Заметка успешно добавлена!")

    elif choice == 'Просмотреть все заметки':
        view_all_notes(notes)

    elif choice == 'Изменить заметку':
        if len(notes) == 1:
            edit_notes(notes, 0)
        else:
            try:
                note_names = [f"{note['Тема заметки']} {note['Заголовок']} {note['Тело заметки']}" for note in notes]
                choice = choicebox(
                    "Выберите заметку для изменения", "Стол заметок", note_names)
                if choice:
                    index = note_names.index(choice)
                    edit_notes(notes, index)
            except ValueError:
                msgbox(
                    "Выбрана неверная заметка , либо Стол заметок пуст. Изменение не выполнено.", 'Стол заметок')

    elif choice == 'Выборка по дате':
        search_by_date(notes)

    elif choice == 'Удалить заметку':
        if not notes:
            msgbox("Стол заметок пуст. Нельзя удалить заметку.", 'Стол заметок')
        else:
            if len(notes) == 1:
                delete_notes(notes, 0)
            else:
                try:
                    note_names = [f"{note['Тема заметки']} {note['Заголовок']} {note['Тело заметки']}" for note in notes]
                    choice = choicebox(
                        "Выберите заметку для удаления", "Стол заметок", note_names)

                    if choice:
                        index = note_names.index(choice)
                        delete_notes(notes, index)

                except ValueError:
                    msgbox("Выбрана неверная заметка. Удаление не выполнено.", 'Стол заметок')


    elif choice == 'Выборка по теме':
        search_by_topic(notes)


    elif choice == 'Выход':
        msgbox("Всего хорошего, Стол заметок закрыт!")
        break
