from pydantic import BaseModel
from datetime import date, time


class Ride(BaseModel):
    date: date  # Ночной развоз указан
    request_time: time
    arriving_time: time
    order_phone: str
    order_method: str
    day_of_ride: str
    username: str
    ride_group: str
    ssp_current: str
    ssp_during_order: str
    passenger_phone: str
    email: str
    employee_id: int
    passenger_pd: str
    ride_id: int
    city: str
    address_from: str
    address_stay: str
    address_to: str
    coordinates_from: str
    coordinates_stay: str
    coordinates_to: str
    fare: str  # Почему-то минус иногда
    commentary: str
    ride_cost: int
    waiting_cost: int
    waiting_time_from: int
    waiting_time_stay: int
    ride_goal: str
    cost_of_toil_road: int


