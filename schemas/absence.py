from pydantic import BaseModel


class Absence(BaseModel):
    # "Отсутствия АТД_{Месяц с загл. буквы} {год}.xlsx"
    employee_id: int  # Столбец A (1) "№"
    # Если будет некорректон работать, то есть ФИО: Столбец B (2) "ФИО".
    # Для получения табельного, можно связывать с employee_info
    start_date: str  # Столбец C (3) "Дата начала"
    end_date: str  # Столбец D (4) "Дата окончания"
