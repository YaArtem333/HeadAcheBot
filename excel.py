import xlsxwriter as xl # Библиотека для записи информации в excel файл
import pandas as pd # Библиотека для работы с данными
import os # Модуль для работы с операционной системой, в частности для отправки пользователю excel файла

# Создание пустой таблицы
def first_table():
    hd_table = pd.DataFrame({"Date": [],
                                      "Time": [],
                                      "Aura": [],
                                      "Anaesthetic": [],
                                      "Type": [],
                                      "Dosage": []})
    return hd_table

# Клсаа Person для хранения информации о пользоватлях
class Person:
    # Конструктор
    def __init__(self, user_id, hd):
        self.user_id = user_id
        self.headache_data = hd
        self.note = ['0','0','0','0','0','0']

    # Функция добавления элемента в датафрэйм
    def add_item(self, dataframe, notes_list):
        dataframe.loc[len(dataframe.index)] = [notes_list[0], notes_list[1], notes_list[2],
                                               notes_list[3], notes_list[4], notes_list[5]]

# Функция для конвертации датафрэйма в excel файл
def get_xl(dataframe):
    dataframe.to_excel('./Headaches.xlsx')
    xl = open(r'./Headaches.xlsx', 'rb')
    return xl
    xl.close()
    os.remove('./Headaches.xlsx')


