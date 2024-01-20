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
    while True:
        if not notes:
            msgbox("Стол заметок пуст.", 'Стол заметок.')
            return

        # Создаем список строк для представления заметок в виде "Тема: Заголовок"
        note_strings = [f"{note['Тема заметки']}: {note['Заголовок']}" for note in notes]

        if len(notes) == 1:
            # Если всего одна заметка, выводим сообщение и затем заметку
            msgbox(f"Заметка всего одна: {note_strings[0]}", 'Стол заметок')
            display_note_info(notes[0])

            # После просмотра заметки, предлагаем пользователю вернуться к списку или выйти
            choices = ['Вернуться к списку', 'Выйти в главное меню']
            return_choice = buttonbox("Выберите действие", "Просмотр заметок", choices)

            if return_choice == 'Выйти в главное меню':
                return
            elif return_choice == 'Вернуться к списку':
                continue  # возврат к списку при одной заметке
            else:
                msgbox("Просмотр заметок отменён", 'Стол заметок')
                return
        else:
            # Пользователь выбирает заметку из списка
            chosen_note = choicebox("Выберите заметку", "Стол заметок", note_strings)

            if chosen_note is None:  # нажата кнопка "Cancel"
                msgbox("Просмотр заметок отменён", 'Стол заметок')
                return

            # Ищем выбранную заметку в списке
            chosen_index = note_strings.index(chosen_note)

            # Отображаем полную информацию о выбранной заметке
            display_note_info(notes[chosen_index])

            # После просмотра заметки, предлагаем пользователю вернуться к списку или выйти
            choices = ['Вернуться к списку', 'Выйти в главное меню']
            return_choice = buttonbox("Выберите действие", "Просмотр заметок", choices)

            if return_choice == 'Выйти в главное меню':
                return
            elif return_choice == 'Вернуться к списку':
                continue  # возврат к списку при выборе заметки
            else:
                msgbox("Просмотр заметок отменён", 'Стол заметок')
                return




def display_note_info(note):
    # Форматируем информацию о заметке
    note_info = f"Тема заметки: {note['Тема заметки']}\n" \
                f"Заголовок: {note['Заголовок']}\n" \
                f"Текст заметки: {note['Текст заметки']}\n" \
                f"Дата/время создания/изменения: {note['Дата/время создания/изменения']}"

    # Отображаем информацию в новом окне
    msgbox(note_info, 'Полная информация о заметке')


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
    while True:
        if not notes:
            msgbox("Стол заметок пуст. Нельзя выбрать заметку по дате.", 'Стол заметок')
            return

        unique_dates = set(
            note['Дата/время создания/изменения'].split()[0] for note in notes)
        unique_dates = list(unique_dates)

        if unique_dates:
            date = enterbox(
                "Введите дату для фильтрации (гггг-мм-дд):", "Выборка по дате")

            if date is None:
                msgbox("Выбор даты отменен", "Выборка по дате")
                return

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
            note_info = []

            for note in found_notes:
                note_info.append(
                    f"{note['Тема заметки']} {note['Заголовок']}: {note['Дата/время создания/изменения']}")

            if note_info:
                if len(note_info) == 1:
                    msgbox(note_info[0], f'Заметка за {date}')
                    display_note_info(found_notes[0])
                else:
                    # Пользователь выбирает заметку для подробного просмотра
                    choice = choicebox("Выберите заметку для подробного просмотра", "Выборка по дате", note_info)

                    if choice:
                        index = note_info.index(choice)
                        display_note_info(found_notes[index])

                        # После просмотра заметки, предлагаем пользователю вернуться к списку или выйти
                        choices = ['Вернуться к списку', 'Выйти в главное меню']
                        return_choice = buttonbox("Выберите действие", "Просмотр заметок", choices)

                        if return_choice == 'Выйти в главное меню':
                            return
                        elif return_choice == 'Вернуться к списку':
                            choice = choicebox("Выберите заметку для подробного просмотра", "Выборка по дате", note_info)
                            if choice:
                                index = note_info.index(choice)
                                display_note_info(found_notes[index])
                                
                                choices = ['Вернуться к списку', 'Выйти в главное меню']
                                return_choice = buttonbox("Выберите действие", "Просмотр заметок", choices)
                        else:
                            msgbox("Просмотр заметок отменён", 'Стол заметок')
                            return
            else:
                msgbox(f"Заметок за {date} не найдено.", 'Результат поиска')
        else:
            msgbox("Стол заметок пуст. Нельзя выбрать заметку по дате.", 'Стол заметок')
            return




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

        note_info = [
            f"{note['Тема заметки']} {note['Заголовок']}" for note in found_notes]

        if note_info:
            if len(note_info) == 1:
                msgbox(note_info[0], f'Заметки с темой: {chosen_topic}')
                display_note_info(found_notes[0])
            else:
                # Пользователь выбирает заметку для подробного просмотра
                choice = choicebox("Выберите заметку для подробного просмотра", f"Заметки с темой: {chosen_topic}", note_info)

                if choice:
                    index = note_info.index(choice)
                    display_note_info(found_notes[index])

                    # После просмотра заметки, предлагаем пользователю вернуться к списку или выйти
                    choices = ['Вернуться к списку', 'Выйти в главное меню']
                    return_choice = buttonbox("Выберите действие", "Просмотр заметок", choices)

                    if return_choice == 'Выйти в главное меню':
                        return []
                    elif return_choice == 'Вернуться к списку':
                        choice = choicebox("Выберите заметку для подробного просмотра", f"Заметки с темой: {chosen_topic}", note_info)

                        if choice:
                            index = note_info.index(choice)
                            display_note_info(found_notes[index])

                            # После просмотра заметки, предлагаем пользователю вернуться к списку или выйти
                            choices = ['Вернуться к списку', 'Выйти в главное меню']
                            return_choice = buttonbox("Выберите действие", "Просмотр заметок", choices)  # возврат к списку при выборе заметки
                    else:
                        msgbox("Просмотр заметок отменён", 'Стол заметок')
                        return found_notes
        else:
            msgbox(f"Заметок с темой {chosen_topic} не найдено.", 'Результат поиска')
            return []
    else:
        return []
