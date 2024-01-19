from easygui import *
import json

def load_notes():
    try:
        with open("notes.json", "r") as file:
            notes = json.load(file)
        return notes
    except FileNotFoundError:
        return []
    
def save_notes(notes):
    with open("notes.json", "w") as file:
        json.dump(notes, file, indent=2)
        
def add_notes(notes, data):
    notes.append({"Идентификатор": data[0], "Заголовок": data[1], "Тело заметки": data[2], "Дата/время создания/изменения": data[3]})
    save_notes(notes)
    
def view_all_notes(notes):
    if not notes:
        msgbox("Стол заметок пуст.", 'Стол заметок.')
        return

    msg = ""
    for notes in notes:
        msg += f"{notes['Идентификатор']} {notes['Заголовок']} {notes['Тело заметки']}: {notes['Дата/время создания/изменения']}\n"
    
    msgbox(msg, 'Стол заметок')
    
def delete_notes(notes, index):
    note = notes[index]
    confirmation = ynbox(f"Вы уверены, что хотите удалить заметку:\n{note['Идентификатор']} {note['Заголовок']} {note['Тело заметки']}?", 'Удаление заметки')
    
    if confirmation:
        del notes[index]
        save_notes(notes)
        msgbox("Заметка успешно удалена!")
        
def edit_notes(notes, index):
        note = notes[index]
        msg = "Измените заметку"
        title = "Карточка заметки"
        filed_names = ["Идентификатор","Заголовок","Тело заметки", "Дата/время создания/изменения"]
        faled_values = multenterbox(msg, title, filed_names, 
                                    values=[note['Идентификатор'], note['Заголовок'],
                                            note['Тело заметки'], note['Дата/время создания/изменения']])
        
        if faled_values:
            notes[index] = {"Идентификатор": faled_values[0], 
                           "Заголовок": faled_values[1], "Тело заметки": faled_values[2], 
                           "Дата/время создания/изменения": faled_values[3]}
            save_notes(notes)
            msgbox("Заметка успешно изменена!")
            
def search_by_date(notes, date):
    found_notes = [note for note in notes if note['Дата/время создания/изменения'] == date]
    return found_notes