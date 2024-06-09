import datetime

from loguru import logger  # Используем для логов эту библиотеку из-за красоты
from tzwhere import tzwhere  # Библиотека для определения часового пояса по координатам
import pytz  # Библиотека для преобразования часового пояса

from geocodes import Geocodes
import dal

# Моковый словарь тарифа такси к грейдам для тестов
grades_dict = {
    'Эконом': 1,
    'Комфорт': 2,
    'Комфорт+': 3,
    'Бизнес': 3,
    'Минивэн': 3,
    'Детский': 3
}


class Algorithm:  # TODO: Добавить выходные в подозрение
    def __init__(self):
        self.ride = None
        self.employee_info = None
        self.errors = []
        self.from_distance_to_registered = None
        self.from_distance_to_actual_residence = None
        self.to_distance_to_registered = None
        self.to_distance_to_actual_residence = None

    def check_ride(self):
        self.errors = []
        rides_for_processing = dal.Rides.get_rides_for_processing()

        # Получаем поездки и рассматриваем каждую по отдельности
        for ride in rides_for_processing:
            logger.info(f'Рассматриваем поездку с id = {self.ride.ride_id}')
            try:
                # Далее функции будут идти в соответствии с блок схемой алгоритма,
                # где каждая проверка - отдельная функция
                self.ride = ride
                self.fix_timezone()  # Изменяем таймзону с МСК на местную по координатам
                self.fix_assistant()  # Изменяем имя заказчика на имя пассажира, если заказывал ассистент
                self.get_employee_info()  # Получаем инфу о сотруднике

                # Далее идут проверки на то, что:
                self.check_passenger_user()  # Пассажир и заказчик совпадают
                self.check_employee_status()  # Работал ли человек в компании во время поездки
                self.validate_grade()  # Такси заказано по грейду

                self.check_absences()  # Поездка во время периода отсутствия
                # Таблица с удаленной работой не составлена, т.к. не ясен ее формат
                # TODO: сделать таблицу
                self.check_remote_work()  # Поездка не во время удаленки

                self.check_wait_time()  # Есть ли платное ожидание
                self.validate_ride_time()  # Дольше ли поездка 1.5 часов
                self.validate_ride_distance()  # Дальше ли она 20 км за МКАД

                self.fill_distances()  # Здесь мы заполняем расстояния
                # от точки старта/завершения поездки до дома/аэропорта/жд вокзала
                if self.check_if_night_time():  # Если ночное время, то проверяем на поездку ИЗ дома НЕ в аэропорт.
                    # Остальные будут валидны
                    if self.check_if_from_home() and not self.check_if_to_airport_railway():
                        logger.error('Подозрение на поездку из дома')
                        self.errors.append('Подозрение на поездку из дома')
                else:
                    # Отдельно проверка на домой/из дома
                    if self.check_if_from_home():
                        logger.error('Подозрение на поездку из дома')
                        self.errors.append('Подозрение на поездку из дома')
                    elif self.check_if_to_home():
                        logger.error('Подозрение на поездку до дома')
                        self.errors.append('Подозрение на поездку до дома')
                    else:
                        # Поездка не по грейду в/из аэропорта
                        if self.employee_info.grade < 3 and (
                                self.check_if_to_airport_railway or self.check_if_from_airport_railway):
                            logger.error('Неразрешенный трансфер')
                            self.errors.append('Неразрешенный трансфер')

            except Exception as exc:
                # Это требуется для некоторых начальных функций,
                # при определенном результате которых не возможна дальнейшая проверка
                logger.error(f'При обработке поездки с id = {self.ride.ride_id} произошла ошибка - {exc}')
                print(exc)

        return

    def fix_timezone(self):
        # Находим таймзону по координатам и переводим время в нее
        ride_coords = self.ride.coordinates_to.split(', ')
        tz = tzwhere.tzwhere().tzNameAt(latitude=ride_coords[0], longitude=ride_coords[1])
        self.ride.request_time = self.ride.request_time.astimezone(pytz.timezone(tz))
        self.ride.arriving_time = self.ride.arriving_time.astimezone(pytz.timezone(tz))

    def fix_assistant(self):
        # Если заказывал ассистент, то заменяем имя пассажира на заказчика
        if self.ride.passenger_pd.split()[1] == 'A':
            logger.info('Данную поездку заказывал ассистент. Заменяем того, кому заказали, на имя заказчика')
            self.ride.passenger_pd = self.ride.username

    def get_employee_info(self):
        self.employee_info = dal.EmployeeInfo.get_employee_info_for_processing(self.ride.employee_id)
        if not self.employee_info:
            logger.error(f'Сотрудника с id = {self.ride.employee_id} не существует')
            self.errors.append('Сотрудника не существует')
            raise Exception

        logger.info(f'Рассматриваем сотрудника с id = {self.employee_info.id}')

    def check_passenger_user(self):
        if int(self.ride.passenger_pd.split()[0]) != int(self.ride.employee_id):
            logger.error('ID заказчика и ID пассажира не совпадают')
            self.errors.append('Заказ другому человеку')

    def check_employee_status(self):
        # Если employment_end_date отсутствует, то значит сотрудник до сих пор числится в компании,
        # поэтому проверка двойная
        if (
                self.employee_info.employment_end_date
                and
                self.employee_info.employment_end_date < self.ride.date
        ):
            logger.error(f'Сотрудник уже не работает в компании')
            self.errors.append('Уволившийся сотрудник')

    def validate_grade(self):
        if grades_dict[self.ride.fare] > self.employee_info.grade:
            logger.error(f'Сотрудник заказал такси класса {self.ride.fare} '
                         f'не по своему грейду {self.employee_info.grade}')
            self.errors.append('Несоответствие грейду')

    def check_absences(self):
        absence = dal.Absences.get_absense_periods_for_processing(self.employee_info.id)

        for case in absence:
            if case.start_date <= self.ride.date <= case.end_date:
                logger.error(f'Сотрудник заказал такси во время отсутствия на работе')
                self.errors.append('Во время отсутствия')

    def check_remote_work(self):
        pass  # Заглушка, т.к. нет таблицы

    def check_wait_time(self):
        if self.ride.waiting_cost:
            logger.error('У поездки было платное ожидание')
            self.errors.append('Выяснить причину платного ожидания')

    def validate_ride_time(self):
        if self.ride.arriving_time - self.ride.request_time > datetime.timedelta(minutes=90):
            logger.error('Поездка заняла больше 1.5 часов')
            self.errors.append('Слишком долгая')

    def validate_ride_distance(self):
        pass  # Заглушка, т.к. пока не ясно, как найти расстояние от МКАД.
        # TODO: убрать заглушку по МКАДу

    def fill_distances(self):
        # Обращаемся к geocodes.py и получаем координаты места жительства и прописки.
        geocodes = Geocodes()
        registered_coords = geocodes.get_coords_from_address(self.employee_info.registered_address)
        actual_residence_coords = geocodes.get_coords_from_address(self.employee_info.actual_residence_address)

        # Расстояние от ТОЧКИ СТАРТА до МЕСТА ПРОПИСКИ
        self.from_distance_to_registered = geocodes.get_distance(
            self.ride.coordinates_from, registered_coords
        )
        # Расстояние от ТОЧКИ СТАРТА до МЕСТА ЖИТЕЛЬСТВА
        self.from_distance_to_actual_residence = geocodes.get_distance(
            self.ride.coordinates_from, actual_residence_coords
        )
        # Расстояние от КОНЕЧНОЙ ТОЧКИ до МЕСТА ПРОПИСКИ
        self.to_distance_to_registered = geocodes.get_distance(
            self.ride.coordinates_to, registered_coords
        )
        # Расстояние от КОНЕЧНОЙ ТОЧКИ до МЕСТА ЖИТЕЛЬСТВА
        self.to_distance_to_actual_residence = geocodes.get_distance(
            self.ride.coordinates_to, actual_residence_coords
        )

    def check_if_night_time(self):
        # Ночное время - это время с 22 до 5:30.
        if (self.ride.request_time.hour not in range(22, 4, -1) or
                self.ride.request_time.hour == 5 and self.ride.request_time.minute in range(0, 30)):
            return True
        else:
            return False

    def check_if_from_home(self):
        # Проверка на поездку из МЕСТА ЖИТЕЛЬСТВА/ПРОПИСКИ
        dist_to_home = min(self.from_distance_to_registered, self.from_distance_to_actual_residence)
        if dist_to_home < 500:
            logger.warning(f'Расстояние начальной точки до дома - {dist_to_home}. Подозрение на поездку из дома.')
            return True
        else:
            logger.info(f'Расстояние начальной точки до дома - {dist_to_home}. Поездка не из дома.')
            return False

    def check_if_to_home(self):
        # Проверка на поездку до МЕСТА ЖИТЕЛЬСТВА/ПРОПИСКИ
        dist_to_home = min(self.to_distance_to_registered, self.to_distance_to_actual_residence)
        if dist_to_home < 500:
            logger.warning(f'Расстояние конечной точки до дома - {dist_to_home}. Подозрение на поездку до дома.')
            return True
        else:
            logger.info(f'Расстояние конечной точки до дома - {dist_to_home}. Поездка не до дома.')
            return False

    def check_if_to_airport_railway(self):
        # Заглушка, потому что список аэропортов и ЖД находится в работе
        pass  # TODO: собрать список координат аэропортов / ЖД вокзалов

    def check_if_from_airport_railway(self):
        pass  # TODO: собрать список координат аэропортов / ЖД вокзалов

    def check_if_holiday(self):
        holidays_permanent = [datetime.date(datetime.date.today().year, i[0], i[1]) for i in [
            (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8),
            (2, 23), (3, 8), (5, 1), (5, 9), (6, 12), (11, 4)
        ]]
        holidays_2024_only = [datetime.date(2024, i[0], i[1]) for i in [
            (4, 29), (4, 30), (5, 10), (12, 30), (12, 31)
        ]]

        if self.ride.date in holidays_permanent + holidays_2024_only:
            logger.error('Дата поездки совпадает с датой одного из государственных праздников')
            self.errors.append('В государственный праздник')
