import csv

import schemas


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
        with open('АТД_27.05.2024.xlsx', newline='') as csvfile:  # TODO: Поменять название
            reader = csv.DictReader(csvfile, restval=None, restkey=None)
            new_row = {}
            for row in reader:
                if int(row['Табельный номер']) == id:
                    for key in cls.header_names.keys():
                        new_row[cls.header_names[key]] = row[key]

                    # Возвращаем информацию в виде схемы при наличии сотрудника с таким Табельным номером
                    return schemas.EmployeeInfo(**new_row)

            return None
