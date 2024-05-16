import schemas
from connection import SqlitePool


class SickDays:
    db, cur = SqlitePool.get_db_cur()

    @classmethod
    def create_sick_days(cls):
        # Этот execute, где DROP TABLE можно убрать во время тестов, чтобы данные,
        # введеные в БД сохранялись при перезапуске программы
        cls.cur.execute("""
            DROP TABLE IF EXISTS sick_days
        """)
        cls.cur.execute("""
            CREATE TABLE IF NOT EXISTS sick_days (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                start_date DATE,
                end_date DATE,
                FOREIGN KEY (employee_id) REFERENCES employee_info(id)
            );
        """)
        # Заполняем таблицу случайно сгенерированными данными о больничных.
        # Для тестов необходимо подгонять под результат
        cls.cur.execute("""
            INSERT INTO sick_days (employee_id, start_date, end_date)
            SELECT 
                employee_id,
                DATE('now', '-' || ROUND(RANDOM() * 30) || ' days') AS start_date,
                DATE('now', '-' || ROUND(RANDOM() * 5) || ' days') AS end_date
            FROM
                employee_info
            ORDER BY
                RANDOM()
            LIMIT 10;
        """)
        cls.db.commit()

    @classmethod
    def get_sick_days_for_processing(cls, employee_id):
        # Получаем все больничные сотрудника по его id
        cls.cur.execute(f"""
            SELECT *
            FROM sick_days
            WHERE employee_id = {employee_id}
        """)

        sick_days = cls.cur.fetchall()

        return [schemas.SickDays(**sick) for sick in sick_days]
