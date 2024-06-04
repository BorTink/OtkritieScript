from pydantic import BaseModel


class SickDays(BaseModel):
    # Будет единая таблица пропусков.
    # TODO: Переформатировать (совместить) все таблицы "отсутствия"
    # "Отсутствия АТД_{Месяц с загл. буквы} {год}.xlsx"
    id: int  # Столбец A (1) "№"
    employee_id: int  # Нет id, есть ФИО: Столбец B (2) "ФИО". Для получения табельного, можно связывать с employee_info
    start_date: str  # Столбец C (3) "Дата начала"
    end_date: str  # Столбец D (4) "Дата окончания"
