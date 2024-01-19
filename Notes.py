from easygui import *
from Notes_functions import *

notes = load_notes()

msgbox("Вас приветствует программа для заметок")

while True:
    choices = ['Добавить заметку', 'Просмотреть все заметки', 
               'Изменить заметку','Выборка по дате', 'Удалить заметку','Выход']
    choice = buttonbox("Выберите действие", "Стол заметок", choices)

    if choice == 'Добавить заметку':
        msg = "Введите заметку"
        title = "Карточка заметки"
        field_names = ["Идентификатор", "Заголовок", "Тело заметки", "Дата/время создания/изменения"]
        field_values = multenterbox(msg, title, field_names)
        
        if field_values:
            add_notes(notes, field_values)
            msgbox("Заметка успешно добавлена!")
            
    elif choice == 'Просмотреть все заметки':
        view_all_notes(notes)
        
    
            
    elif choice == 'Выход':
        msgbox("Всего хорошего, Стол заметок закрыт!")
        break