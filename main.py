import dal
from dal.connection import SqlitePool

db, cur = SqlitePool.start_connection()

dal.Rides.create_rides()
dal.EmployeeInfo.create_employee_info()
dal.Vacations.create_vacations()
dal.SickDays.create_sick_days()

# TODO: Придумать результат работы программы

# Создать отдельный файл csv (xlsx, xlx как угодно) и в него записывать:
# Причина невалидности (если можно, подсветить жирным) + Данные о поездке + Данные о пользователе
# + Данные об "отсутствии" (тип + период), если "отсутствие" стало причиной невалидности поездки


