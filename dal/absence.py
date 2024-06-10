import csv

from loguru import logger

import schemas
from utils import convert_xlsx_to_csv


class Absences:
    header_names = {
        '№': 'employee_id',
        'Дата начала': 'start_date',
        'Дата окончания': 'end_date'
    }

    @classmethod
    def get_absense_periods_for_processing(cls, id):
        # Получаем информацию о сотруднике по id
        logger.info('Получаем таблицу отсутствия')

        convert_xlsx_to_csv('Отсутствия АТД_{Месяц с загл. буквы} {год}')
        with open('Отсутствия АТД_{Месяц с загл. буквы} {год}.csv', newline='', encoding='1251') as csvfile:
            # TODO: Поменять название
            reader = csv.DictReader(csvfile, restval=None, restkey=None)
            res = []
            new_row = {}
            for row in reader:
                if int(row['№']) == id:
                    for key in cls.header_names.keys():
                        new_row[cls.header_names[key]] = row[key]

                    # Возвращаем информацию в виде схемы при наличии сотрудника с таким Табельным номером
                    res.append(schemas.Absence(**new_row))

            logger.info('Отсутствия были обработаны')

            return res
