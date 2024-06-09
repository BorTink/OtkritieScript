import csv

import schemas


class Absences:
    header_names = {
        '№': 'employee_id',
        'Дата начала': 'start_date',
        'Дата окончания': 'end_date'
    }

    @classmethod
    def get_absense_periods_for_processing(cls, id):
        # Получаем информацию о сотруднике по id
        with open('Отсутствия АТД_{Месяц с загл. буквы} {год}.xlsx', newline='') as csvfile:  # TODO: Поменять название
            reader = csv.DictReader(csvfile, restval=None, restkey=None)
            res = []
            new_row = {}
            for row in reader:
                if int(row['№']) == id:
                    for key in cls.header_names.keys():
                        new_row[cls.header_names[key]] = row[key]

                    # Возвращаем информацию в виде схемы при наличии сотрудника с таким Табельным номером
                    res.append(schemas.Absence(**new_row))

            return res
