import csv

from loguru import logger

import schemas
from utils import convert_xlsx_to_csv


class EmployeeInfo:
    header_names = {
        'Табельный номер': 'id',
        'ДатаПриемаНаРабот': 'employment_start_date',
        'Дата увольнения': 'employment_end_date',
        'Грейд': 'grade',
        'НЕТ_В_ТАБЛИЦЕ': 'remote_work_days',
        'Адрес регистрации': 'registered_address',
        'Адрес проживания': 'actual_residence_address'
    }

    @classmethod
    def get_employee_info_for_processing(cls, id):
        # Получаем информацию о сотруднике по id
        logger.info('Получаем таблицу сотрудников')

        convert_xlsx_to_csv('АТД_27.05.2024')
        with open('АТД_27.05.2024.csv', newline='', encoding='1251') as csvfile:  # TODO: Поменять название
            reader = csv.DictReader(csvfile, restval=None, restkey=None)
            new_row = {}
            for row in reader:
                if int(row['Табельный номер']) == id:
                    for key in cls.header_names.keys():
                        new_row[cls.header_names[key]] = row[key]

                    # Возвращаем информацию в виде схемы при наличии сотрудника с таким Табельным номером
                    logger.info('Сотрудник был получен')
                    return schemas.EmployeeInfo(**new_row)

            logger.error('Сотрудник не был найден')

            return None
