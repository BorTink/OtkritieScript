from connection import SqlitePool


class Vacations:
    db, cur = SqlitePool.get_db_cur()

    @classmethod
    def create_vacations(cls):
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