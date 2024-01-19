from easygui import *
from Notes_functions import *

notes = load_notes()

msgbox("Вас приветствует программа для заметок")

while True:
    choices = ['Добавить заметку', 'Просмотреть все заметки',
               'Изменить заметку', 'Выборка по дате', 'Удалить заметку', 'Выход']
    choice = buttonbox("Выберите действие", "Стол заметок", choices)

    if choice == 'Добавить заметку':
        msg = "Введите заметку"
        title = "Карточка заметки"
        field_names = ["Идентификатор", "Заголовок",
                       "Тело заметки", "Дата/время создания/изменения"]
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
                note_names = [f"{note['Идентификатор']} {note['Заголовок']} {
                    note['Тело заметки']}" for note in notes]
                choice = choicebox(
                    "Выберите заметку для изменения", "Стол заметок", note_names)
                if choice:
                    index = note_names.index(choice)
                    edit_notes(notes, index)
            except ValueError:
                msgbox(
                    "Выбрана неверная заметка. Изменение не выполнено.", 'Стол заметок')

    elif choice == 'Выборка по дате':
        if not notes:
            msgbox("Стол заметок пуст. Нельзя выбрать заметку по дате.",
                   'Стол заметок')
        else:
            date = enterbox("Введите дату для выборки", "Выборка по дате")
            if date:
                found_notes = search_by_date(notes, date)
                if found_notes:
                    msg = ""
                    for note in found_notes:
                        msg += f"{note['Идентификатор']} {note['Заголовок']} {
                            note['Тело заметки']}: {note['Дата/время создания/изменения']}\n"
                    msgbox(msg, 'Результат поиска')
                else:
                    msgbox(f"Заметка с датой '{
                           date}' не найдена.", 'Результат поиска')

    elif choice == 'Удалить заметку':
        if not notes:
            msgbox("Стол заметок пуст. Нельзя удалить заметку.", 'Стол заметок')
        else:
            if len(notes) == 1:
                delete_notes(notes, 0)
            else:
                try:
                    note_names = [f"{note['Идентификатор']} {note['Заголовок']} {
                        note['Тело заметки']}" for note in notes]
                    choice = choicebox(
                        "Выберите заметку для удаления", "Стол заметок", note_names)

                    if choice:
                        index = note_names.index(choice)
                        delete_notes(notes, index)

                except ValueError:
                    msgbox("Выбран неверная заметка. Удаление не выполнено.", 'Стол заметок')

    elif choice == 'Выход':
        msgbox("Всего хорошего, Стол заметок закрыт!")
        break
