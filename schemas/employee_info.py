from pydantic import BaseModel, Field
from typing import Optional


class EmployeeInfo(BaseModel):
    id: int
    employment_status: str
    employment_start_date: str
    employment_end_date: Optional[str] = None
    grade: str
    remote_work_days: str
    registered_address: str
    actual_residence_address: str
