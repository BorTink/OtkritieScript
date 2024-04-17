import datetime

from loguru import logger
from tzwhere import tzwhere
import pytz

from geocodes import Geocodes
import dal

grades_dict = {
    'Эконом': 1,
    'Комфорт': 2,
    'Комфорт+': 3,
    'Бизнес': 3,
    'Минивэн': 3,
    'Детский': 3
}


class Algorithm:
    def __init__(self):
        self.ride = None
        self.employee_info = None
        self.errors = []
        self.from_distance_to_registered = None
        self.from_distance_to_actual_residence = None
        self.to_distance_to_registered = None
        self.to_distance_to_actual_residence = None

    def check_ride(self):
        rides_for_processing = dal.Rides.get_rides_for_processing()

        for ride in rides_for_processing:
            logger.info(f'Рассматриваем поездку с id = {self.ride.ride_id}')
            try:
                self.ride = ride
                self.fix_timezone()
                self.fix_assistant()
                self.get_employee_info()
                self.check_passenger_user()
                self.check_employee_status()
                self.validate_grade()
                self.check_vacation()
                self.check_sick_days()
                self.check_remote_work()  # TODO: сделать таблицу
                self.check_wait_time()
                self.validate_ride_time()
                self.validate_ride_distance()  # TODO: Сделать систему перевода адреса в коорды и расчет расстояния

                self.fill_distances()
                if self.check_if_night_time():  # TODO: Сделать систему перевода адреса в коорды и расчет расстояния
                    if self.check_if_from_home() and not self.check_if_to_airport_railway():
                        logger.error('Подозрение на поездку из дома')
                        self.errors.append('Подозрение на поездку из дома')
                else:
                    if self.check_if_from_home():
                        logger.error('Подозрение на поездку из дома')
                        self.errors.append('Подозрение на поездку из дома')
                    elif self.check_if_to_home():
                        logger.error('Подозрение на поездку до дома')
                        self.errors.append('Подозрение на поездку до дома')
                    else:
                        if self.employee_info.grade < 3 and (
                                self.check_if_to_airport_railway or self.check_if_from_airport_railway):
                            logger.error('Неразрешенный трансфер')
                            self.errors.append('Неразрешенный трансфер')

            except Exception as exc:
                print(exc)

    def fix_timezone(self):
        ride_coords = self.ride.coordinates_to.split(', ')
        tz = tzwhere.tzwhere().tzNameAt(latitude=ride_coords[0], longitude=ride_coords[1])
        self.ride.request_time = self.ride.request_time.astimezone(pytz.timezone(tz))
        self.ride.arriving_time = self.ride.arriving_time.astimezone(pytz.timezone(tz))

    def fix_assistant(self):
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
        if self.employee_info.employment_end_date < datetime.datetime.now():
            logger.error(f'Сотрудник уже не работает в компании')
            self.errors.append('Уволившийся сотрудник')

    def validate_grade(self):
        if grades_dict[self.ride.fare] > self.employee_info.grade:
            logger.error(f'Сотрудник заказал такси класса {self.ride.fare} '
                         f'не по своему грейду {self.employee_info.grade}')
            self.errors.append('Несоответствие грейду')

    def check_vacation(self):
        vacations = dal.Vacations.get_vacations_for_processing(self.employee_info.id)

        for vacation in vacations:
            if vacation.start_date <= self.ride.date <= vacation.end_date:
                logger.error(f'Сотрудник заказал такси во время отпуска')
                self.errors.append('Во время отпуска')

    def check_sick_days(self):
        sick_days = dal.SickDays.get_sick_days_for_processing(self.employee_info.id)

        for period in sick_days:
            if period.start_date <= self.ride.date <= period.end_date:
                logger.error(f'Сотрудник заказал такси во время больничного')
                self.errors.append('Во время болезни')

    def check_remote_work(self):
        pass  # Заглушка, т.к. забыл создать таблицу

    def check_wait_time(self):
        if self.ride.waiting_cost:
            logger.error('У поездки было платное ожидание')
            self.errors.append('Выяснить причину платного ожидания')

    def validate_ride_time(self):
        if self.ride.arriving_time - self.ride.request_time > datetime.timedelta(minutes=90):
            logger.error('Поездка заняла больше 1.5 часов')
            self.errors.append('Слишком долгая')

    def validate_ride_distance(self):
        pass  # Заглушка, т.к. нужно реализовать систему перевода адреса в координаты и подсчет расстояния

    def fill_distances(self):
        geocodes = Geocodes()
        registered_coords = geocodes.get_coords_from_address(self.employee_info.registered_address)
        actual_residence_coords = geocodes.get_coords_from_address(self.employee_info.actual_residence_address)

        self.from_distance_to_registered = geocodes.get_distance(
            self.ride.coordinates_from, registered_coords
        )
        self.from_distance_to_actual_residence = geocodes.get_distance(
            self.ride.coordinates_from, actual_residence_coords
        )
        self.to_distance_to_registered = geocodes.get_distance(
            self.ride.coordinates_to, registered_coords
        )
        self.to_distance_to_actual_residence = geocodes.get_distance(
            self.ride.coordinates_to, actual_residence_coords
        )

    def check_if_night_time(self):
        if (self.ride.request_time.hour in range(23, 5) or
                self.ride.request_time.hour == 5 and self.ride.request_time.minute in range(0, 30)):
            return True
        else:
            return False

    def check_if_from_home(self):
        dist_to_home = min(self.from_distance_to_registered, self.from_distance_to_actual_residence)
        if dist_to_home < 500:
            logger.warning(f'Расстояние начальной точки до дома - {dist_to_home}. Подозрение на поездку из дома.')
            return True
        else:
            logger.info(f'Расстояние начальной точки до дома - {dist_to_home}. Поездка не из дома.')
            return False

    def check_if_to_home(self):
        dist_to_home = min(self.to_distance_to_registered, self.to_distance_to_actual_residence)
        if dist_to_home < 500:
            logger.warning(f'Расстояние конечной точки до дома - {dist_to_home}. Подозрение на поездку до дома.')
            return True
        else:
            logger.info(f'Расстояние конечной точки до дома - {dist_to_home}. Поездка не до дома.')
            return False
