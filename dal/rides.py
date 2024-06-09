import csv

import schemas


class Rides:
    header_names = {
        'Дата заказа': 'date',  # Ночной развоз указан
        'Время заказа': 'request_time',
        'Рассчетное время подачи': 'arriving_time',
        'Кто заказал': 'order_phone',
        'Способ заказа': 'order_method',
        'День недели завершения заказа': 'day_of_ride',
        'Имя пользователя': 'username',
        'Группа': 'ride_group',
        'Актуальное подразделение': 'ssp_current',
        'Подразделение сотрудника на момент заказа': 'ssp_during_order',
        'Телефон': 'passenger_phone',
        'Электронная почта': 'email',
        'ID сотрудника': 'employee_id',
        'Кому заказали: ФИО': 'passenger_pd',
        'Идентификатор заказа': 'ride_id',
        'Город': 'city',
        'Адрес подачи': 'address_from',
        'Промежуточные адреса': 'address_stay',
        'Адрес назначения': 'address_to',
        'Координаты подачи': 'coordinates_from',
        'Координаты промежуточных адресов': 'coordinates_stay',
        'Координаты адреса назначения': 'coordinates_to',
        'Тариф': 'fare',  # Почему-то минус иногда
        'Комментарий': 'commentary',
        'Стоимость поездки': 'ride_cost',
        'Стоимость ожидания': 'waiting_cost',
        'Время ожидания в точке А': 'waiting_time_from',
        'Время ожидания в промежуточных точках': 'waiting_time_stay',
        'Цель поездки': 'ride_goal',
        'Стоимость платной дороги': 'cost_of_toil_road'
    }

    @classmethod
    def get_rides_for_processing(cls):
        # Получаем все поездки для обработки
        with open('Поездки.xlsx', newline='') as csvfile:  # TODO: Поменять название
            reader = csv.DictReader(csvfile, restval=None, restkey=None)
            res = []
            new_row = {}
            for row in reader:
                for key in cls.header_names.keys():
                    new_row[cls.header_names[key]] = row[key]
                # Добавляем в итоговый список поездок схему поездки
                res.append(schemas.Ride(**new_row))

            return res
