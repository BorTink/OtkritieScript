from connection import SqlitePool


class SickDays:
    db, cur = SqlitePool.get_db_cur()

    @classmethod
    def create_sick_days(cls):
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
