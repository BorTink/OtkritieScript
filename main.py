import dal
from dal.connection import SqlitePool

db, cur = SqlitePool.start_connection()

dal.Rides.create_rides()
dal.EmployeeInfo.create_employee_info()
dal.Vacations.create_vacations()
dal.SickDays.create_sick_days()
