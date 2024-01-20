from easygui import *
import json
from datetime import datetime


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


def get_current_datetime():
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def add_notes(notes, data):
    current_datetime = get_current_datetime()
    if not all(data):
        msgbox("Вы заполнили не все поля, повторите ввод.", 'Ошибка ввода')
        return
    else:
        notes.append({
            "Тема заметки": data[0],
            "Заголовок": data[1],
            "Текст заметки": data[2],
            "Дата/время создания/изменения": current_datetime
        })
        save_notes(notes)
        msgbox("Заметка успешно добавлена!")


def view_all_notes(notes):
    if not notes:
        msgbox("Стол заметок пуст.", 'Стол заметок.')
        return

    msg = ""
    for note in notes:
        msg += f"{note['Тема заметки']} {note['Заголовок']
                                         } {note['Текст заметки']} {note['Дата/время создания/изменения']}\n"

    msgbox(msg, 'Стол заметок')


def delete_notes(notes, index):
    note = notes[index]
    confirmation = ynbox(f"Вы уверены, что хотите удалить заметку:\n{note['Тема заметки']} {note['Заголовок']} {note['Текст заметки']}?",
                         'Удаление заметки')

    if confirmation:
        del notes[index]
        save_notes(notes)
        msgbox("Заметка успешно удалена!")


def edit_notes(notes, index):
    note = notes[index]
    msg = "Измените заметку"
    title = "Карточка заметки"
    field_names = ["Тема заметки", "Заголовок", "Текст заметки"]

    field_values = multenterbox(msg, title, field_names, values=[
                                note['Тема заметки'], note['Заголовок'], note['Текст заметки']])

    if not field_values or any(value.strip() == "" for value in field_values):
        msgbox("Вы заполнили не все поля, повторите ввод.", 'Ошибка ввода')
        return
    else:
        current_datetime = get_current_datetime()
        notes[index] = {
            "Тема заметки": field_values[0],
            "Заголовок": field_values[1],
            "Текст заметки": field_values[2],
            "Дата/время создания/изменения": current_datetime
        }
        save_notes(notes)
        msgbox("Заметка успешно изменена!")


def search_by_date(notes):
    if not notes:
        msgbox("Стол заметок пуст. Нельзя выбрать заметку по дате.", 'Стол заметок')
        return

    unique_dates = set(
        note['Дата/время создания/изменения'].split()[0] for note in notes)
    unique_dates = list(unique_dates)

    if unique_dates:
        date = enterbox(
            "Введите дату для фильтрации (гггг-мм-дд):", "Выборка по дате")

        if date:

            found_notes = [
                note for note in notes if note['Дата/время создания/изменения'].startswith(date)]

            choices = ["По возрастанию", "По убыванию"]
            sort_order = choicebox(
                "Выберите порядок сортировки", "Сортировка", choices)

            if sort_order == "По возрастанию":
                found_notes = sorted(
                    found_notes, key=lambda x: x['Дата/время создания/изменения'])
            elif sort_order == "По убыванию":
                found_notes = sorted(
                    found_notes, key=lambda x: x['Дата/время создания/изменения'], reverse=True)

            msg = ""
            for note in found_notes:
                msg += f"{note['Тема заметки']} {note['Заголовок']} {
                    note['Текст заметки']}: {note['Дата/время создания/изменения']}\n"
            msgbox(msg, 'Результат поиска')
        else:
            msgbox("Пожалуйста, введите дату.", 'Выборка по дате')
    else:
        msgbox("Стол заметок пуст. Нельзя выбрать заметку по дате.", 'Стол заметок')


def get_all_topics(notes):
    return list(set(note['Тема заметки'] for note in notes))


def search_by_topic(notes):
    all_topics = get_all_topics(notes)

    if not all_topics:
        msgbox("Нет доступных тем.", 'Стол заметок')
        return []

    if len(all_topics) == 1:
        chosen_topic = all_topics[0]
        msgbox(f"Создана одна тема: {chosen_topic}", 'Стол заметок')
    else:
        chosen_topic = choicebox("Выберите тему", "Стол заметок", all_topics)

    if chosen_topic:
        found_notes = [
            note for note in notes if note['Тема заметки'].lower() == chosen_topic.lower()]

        msg = ""
        for note in found_notes:
            msg += f"{note['Тема заметки']} {note['Заголовок']
                                             } {note['Текст заметки']}: {note['Дата/время создания/изменения']}\n"

        msgbox(msg, f'Заметки с темой: {chosen_topic}')

        return found_notes
    else:
        return []
