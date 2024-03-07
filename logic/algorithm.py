from loguru import logger
from tzwhere import tzwhere
import pytz

import dal


class Algorithm:
    def check_ride(self):
        rides_for_processing = dal.Rides.get_rides_for_processing()

        for ride in rides_for_processing:
            self.fix_timezone(ride)
            self.fix_assistant(ride)

            employee_info = dal.EmployeeInfo.get_employee_info_for_processing(rides_for_processing.employee_id)
            if not employee_info:
                logger.error(f'Сотрудника с id = {rides_for_processing.employee_id} не существует')
                return None

    @staticmethod
    def fix_timezone(ride):
        ride_coords = ride.coordinates_to.split(', ')
        tz = tzwhere.tzwhere().tzNameAt(latitude=ride_coords[0], longitude=ride_coords[1])
        ride.request_time = ride.request_time.astimezone(pytz.timezone(tz))
        ride.arriving_time = ride.arriving_time.astimezone(pytz.timezone(tz))

    @staticmethod
    def fix_assistant(ride):
        if ride.passenger_pd.split()[1] == 'A':
            logger.info('Данную поездку заказывал ассистент. Заменяем того, кому заказали, на имя заказчика')
            ride.passenger_pd = ride.username
