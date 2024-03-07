from pydantic import BaseModel


class Vacation(BaseModel):
    id: int
    employee_id: int
    start_date: str
    end_date: str
