import telebot # Библиотека для ботов
from telebot import types # Для кнопок получения информации от пользователя
import datetime # Библиотека для работы с датой и временем
import os # Модуль для работы с операционной системой, в частности для отправки пользователю excel файла
import pandas as pd # Библиотека для работы с данными

import excel
import settings

# Создаем бота по токену
bot = telebot.TeleBot(settings.TOKEN)

# Создаем все кнопки меню
a = types.ReplyKeyboardRemove()

menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn1 = types.KeyboardButton("Make a note")
btn2 = types.KeyboardButton("Get Excel table with data")
menu_markup.add(btn1, btn2)

yn_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn3 = types.KeyboardButton("Yes")
btn4 = types.KeyboardButton("No")
yn_markup.add(btn3, btn4)

treatments_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn5 = types.KeyboardButton("Pentalgin")
btn6 = types.KeyboardButton("Citramon")
btn7 = types.KeyboardButton("Nurofen")
btn8 = types.KeyboardButton("Aspirin")
btn9 = types.KeyboardButton("Paracetamol")
btn10 = types.KeyboardButton("Analgin")
treatments_markup.add(btn5, btn6, btn7, btn8, btn9, btn10)

doze_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
btn11 = types.KeyboardButton("1/2 of a tablet")
btn12 = types.KeyboardButton("1 tablet")
btn13 = types.KeyboardButton("2 tablets")
btn14 = types.KeyboardButton("3 tablets")
doze_markup.add(btn11, btn12, btn13, btn14)

# Список для хранения информации о пользователях
persons = []

# Описание команды /start
@bot.message_handler(commands = ["start"])
def start_message(message):
    # Получаем id и имя пользователя
    user_id = message.from_user.id
    name = message.from_user.first_name

    # Создаём пустую таблицу для пользователя
    headache_data = excel.first_table()
    # Создаем объект класса Person
    person = excel.Person(user_id, headache_data)

    # Если объекта нет в списке persons, то добавляем его туда и ему открывается главное меню
    if not person in persons:
        persons.append(person)
        bot.send_message(message.chat.id, f"<b>Hello</b>, <b>{name}</b>!\n"
                                          f"I'll help you with collecting data about your headaches!\n\n"
                                          f"Select <b>Make a note</b> to tell about your headache\n\n"
                                          f"Select <b>Get Excel table with data</b> to get the info about your headaches",
                                          parse_mode="html", reply_markup=menu_markup)
        bot.register_next_step_handler(message, menu_items)

    # Если объект есть в списке, то ему открывается главное меню
    else:
        bot.send_message(message.chat.id, f"<b>Hello</b>, <b>{name}</b>!\n"
                                          f"I'll help you with collecting data about your headaches!\n\n"
                                          f"Select <b>Make a note</b> to tell about your headache\n\n"
                                          f"Select <b>Get Excel table with data</b> to get the info about your headaches",
                         parse_mode="html", reply_markup=menu_markup)
        bot.register_next_step_handler(message, menu_items)

# Главное меню с двумя пунктами
def menu_items(message):
    user_id = message.from_user.id

    # Если пользователь выбирает первый пункт меню, то ему предлагается ввести данные
    if message.text == "Make a note":
        bot.send_message(message.chat.id, "When did you have a headache?\n"
                                          "Enter the date in format <b>DD.MM.YYYY</b>\n"
                                          "D - day, M - month, Y - year",
                                          parse_mode='html', reply_markup=a)
        bot.register_next_step_handler(message, notestep1)

    # Если выбран второй пункт меню, то присылается таблица в формате .xlsx
    elif message.text == "Get Excel table with data":
        for i in persons:
            if i.user_id == user_id:
                asd = excel.get_xl(i.headache_data) # Функция get_xl конвертирует датафрэйм в excel файл
                bot.send_document(message.chat.id, asd)
                bot.register_next_step_handler(message, menu_items)
                break
            else:
                continue
    else:
        bot.send_message(message.chat.id, "No such command in the list...", reply_markup=menu_markup)
        bot.register_next_step_handler(message, menu_items)

# Вводится дата болезни и запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
def notestep1(message):
    user_id = message.from_user.id
    _date = message.text
    try:
        # Проверка на корректность введенных данных
        datetime.datetime.strptime(_date, "%d.%m.%Y")
        for i in persons:
            if i.user_id == user_id:
                i.note[0] = _date # запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
                break

        # Предлагается ввести время болезни
        bot.send_message(message.chat.id, "Enter the time you had it in format <b>HH:MM</b>\n"
                                          "H - hours, M - minutes", parse_mode='html', reply_markup=a)
        bot.register_next_step_handler(message, notestep2)
    except:
        bot.send_message(message.chat.id, "You entered wrong date, try again", reply_markup=a)
        bot.register_next_step_handler(message, notestep1)

# Вводится время болезни и запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
def notestep2(message):
    user_id = message.from_user.id
    _time = message.text

    try:
        # Проверка на корректность введенных данных
        datetime.datetime.strptime(_time, "%H:%M")
        for i in persons:
            if i.user_id == user_id:
                i.note[1] = _time # запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
                break

        # Предлагается ввести данные об ауре
        bot.send_message(message.chat.id, "Did you have an Aura?", parse_mode='html', reply_markup=yn_markup)
        bot.register_next_step_handler(message, notestep3)
    except:
        bot.send_message(message.chat.id, "You entered wrong time, try again", reply_markup=a)
        bot.register_next_step_handler(message, notestep2)

# Вводятся данные об ауре и запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
def notestep3(message):
    user_id = message.from_user.id
    _aura = message.text

    # Проверка на корректность введенных данных
    if _aura == "Yes" or _aura == "No":
        for i in persons:
            if i.user_id == user_id:
                i.note[2] = _aura # запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
                break

        # Предлагается ввести данные об обезболивающем
        bot.send_message(message.chat.id, "Did you take an anaesthetic?", reply_markup=yn_markup)
        bot.register_next_step_handler(message, notestep4)
    else:
        bot.send_message(message.chat.id, "No such answer in the list", reply_markup=yn_markup)
        bot.register_next_step_handler(message, notestep3)

# Вводятся данные об обезболивающем и запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
def notestep4(message):
    _anaes = message.text
    user_id = message.from_user.id

    # Если пользователь принимал обезболивающее, то запись добавляется в датафрэйм
    if _anaes == "Yes":
        for i in persons:
            if i.user_id == user_id:
                i.note[3] = _anaes
                break
        # Задается вопрос об обезболивающем
        bot.send_message(message.chat.id, "What anaesthetic?", reply_markup=treatments_markup)
        bot.register_next_step_handler(message, notestep5)

    # Если не принимал, то запись добавляется в датафрэйм
    elif _anaes == "No":
        for i in persons:
            if i.user_id == user_id:
                i.note[3] = _anaes
                i.note[4] = '-'
                i.note[5] = '-'
                i.add_item(i.headache_data, i.note)
                break

        # Возвращение пользователя в главное меню
        bot.send_message(message.chat.id, "Thanks, I added a note!\n")
        bot.send_message(message.chat.id, f"Select <b>Make a note</b> to tell about your headache\n\n"
                                          f"Select <b>Get Excel table with data</b> to get the info about your headaches",
                         parse_mode="html", reply_markup=menu_markup)
        bot.register_next_step_handler(message, menu_items)
    else:
        bot.send_message(message.chat.id, "No such answer in the list", reply_markup=yn_markup)
        bot.register_next_step_handler(message, notestep4)

# Вводятся данные о типе обезболивающего и запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
def notestep5(message):
    user_id = message.from_user.id
    _an = message.text

    # Проверка на корректность введенных данных
    if _an == "Pentalgin" or _an == "Citramon" or _an == "Nurofen" or _an == "Aspirin" or _an == "Paracetamol" or _an == "Analgin":
        for i in persons:
            if i.user_id == user_id:
                i.note[4] = _an , # запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
                break

        # Задается вопрос о дозировке
        bot.send_message(message.chat.id, "At what dosage?", reply_markup=doze_markup)
        bot.register_next_step_handler(message, notestep6)
    else:
        bot.send_message(message.chat.id, "No such anaesthetic in the list")
        bot.register_next_step_handler(message, notestep5)


# Вводятся данные о дозировке и запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
def notestep6(message):
    _doze = message.text
    user_id = message.from_user.id

    # Проверка на корректность введенных данных
    if _doze == "1/2 of a tablet" or _doze == "1 tablet" or _doze == "2 tablets" or _doze == "3 tablets":
        for i in persons:
            if i.user_id == user_id:
                i.note[5] = _doze # запись добавляется в датафрэйм, относящийся к пользователю, отправившему сообщение
                i.add_item(i.headache_data, i.note)
                break

        # Возвращение пользователя в главное меню
        bot.send_message(message.chat.id, "Thanks, I added a note!\n")
        bot.send_message(message.chat.id, f"Select <b>Make a note</b> to tell about your headache\n\n"
                                          f"Select <b>Get Excel table with data</b> to get the info about your headaches",
                         parse_mode="html", reply_markup=menu_markup)
        bot.register_next_step_handler(message, menu_items)
    else:
        bot.send_message(message.chat.id, "No such answer in the list", reply_markup=doze_markup)
        bot.register_next_step_handler(message, notestep6)


def start_bot():
    bot.polling(none_stop = True)

