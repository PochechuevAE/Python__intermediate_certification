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
        msgbox("Справочник пуст", 'Телефонный справочник')
        return

    msg = ""
    for notes in notes:
        msg += f"{notes['Идентификатор']} {notes['Заголовок']} {notes['Тело заметки']}: {notes['Дата/время создания/изменения']}\n"
    
    msgbox(msg, 'Программа для заметок')