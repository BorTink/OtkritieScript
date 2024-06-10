
""" создание файла с координатами аэорпортов
airports_file = open('apinfo.ru.csv', 'r', encoding='Windows-1251')
airports_file_lines = airports_file.readlines()
airports = [(i.split('|')[2], i.split('|')[4]) for i in airports_file_lines[1:]]
airports_file.close()

airports_new = open('airports_coords.txt', 'w')
content = ''
for i in airports:
    content += f'{i[0]}, {i[1]}\n'
airports_new.write(content)
"""

import pandas as pd


def convert_xlsx_to_csv(filename):
    excel_file = f'{filename}.xlsx'
    csv_file = f'{filename}.csv'
    df = pd.read_excel(excel_file)
    df.to_csv(csv_file, index=False, encoding='1251', sep=',')
