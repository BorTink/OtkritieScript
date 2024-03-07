from datetime import time, date

from pydantic import Basemodel


class Ride(Basemodel):
    employee_id: int
    ssp_current: int
    passenger_pd: str

    address_from: str
    address_to: str

    date: date
    request_time: time
    arriving_time: time
    city: str

    fare: str
    waiting_time_from: int
    ride_goal: str
    