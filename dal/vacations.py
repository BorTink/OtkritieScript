from connection import SqlitePool

import schemas


class Vacations:
    db, cur = SqlitePool.get_db_cur()

    @classmethod
    def create_vacations(cls):
        # Этот execute, где DROP TABLE можно убрать во время тестов, чтобы данные,
        # введеные в БД сохранялись при перезапуске программы
        cls.cur.execute("""
            DROP TABLE IF EXISTS vacations
        """)
        cls.cur.execute("""
            CREATE TABLE IF NOT EXISTS vacations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id INTEGER,
                start_date DATE,
                end_date DATE,
                FOREIGN KEY (employee_id) REFERENCES employee_info(id)
            );
        """)
        # Заполняем таблицу случайно сгенерированными данными об отпусках.
        # Для тестов необходимо подгонять под результат
        cls.cur.execute("""
        INSERT INTO vacations (employee_id, start_date, end_date)
        SELECT 
            employee_id,
            DATE('now', '+' || ROUND(RANDOM() * 365) || ' days') AS start_date,
            DATE('now', '+' || ROUND(RANDOM() * 30) || ' days') AS end_date
        FROM
            employee_info
        ORDER BY
            RANDOM()
        LIMIT 10;
        """)
        cls.db.commit()

    @classmethod
    def get_vacations_for_processing(cls, employee_id):
        # Получаем отпуски сотрудника по его id
        cls.cur.execute(f"""
            SELECT *
            FROM vacations
            WHERE employee_id = {employee_id}
        """)

        vacations = cls.cur.fetchall()

        # Возвращаем список всех его отпусков
        return [schemas.Vacation(**vacation) for vacation in vacations]
