# TODO: Придумать результат работы программы

# Создать отдельный файл csv (xlsx, xlx как угодно) и в него записывать:
# Причина невалидности (если можно, подсветить жирным) + Данные о поездке + Данные о пользователе
# + Данные об "отсутствии" (тип + период), если "отсутствие" стало причиной невалидности поездки


import csv

import pandas as pd

from logic import Algorithm


# Загрузка Excel файла и сохранение его в формате CSV
excel_file = 'Поездки.xlsx'
csv_file = 'Поездки.csv'
df = pd.read_excel(excel_file)
df.to_csv(csv_file, index=False)


# Переменные errors и verdicts
errors, verdicts = Algorithm().check_rides()

# Чтение данных из CSV файла
with open(csv_file, newline='', encoding='1251') as csvfile:
    reader = csv.reader(csvfile)
    rows = list(reader)

# Добавление заголовков новых столбцов
header = rows[0]
header.append('Ошибки')
header.append('Вердикт')

# Добавление данных в строки
for i, (error_list, verdict) in enumerate(zip(errors, verdicts)):
    error_str = "; ".join(error_list)
    rows[i + 1].append(error_str)
    rows[i + 1].append(verdict)

# Запись данных в новый CSV файл
output_csv_file = 'Поездки_с_вердиктами.csv'
with open(output_csv_file, 'w', newline='', encoding='1251') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(rows)
