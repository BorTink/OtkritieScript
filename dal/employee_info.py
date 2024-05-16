import schemas
from connection import SqlitePool


class EmployeeInfo:
    db, cur = SqlitePool.get_db_cur()  # Получаем переменные для БД

    @classmethod
    def create_employee_info(cls):
        # Этот execute, где DROP TABLE можно убрать во время тестов, чтобы данные,
        # введеные в БД сохранялись при перезапуске программы
        cls.cur.execute("""
            DROP TABLE IF EXISTS employee_info
        """)
        cls.cur.execute("""
            CREATE TABLE IF NOT EXISTS employee_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employment_status TEXT,
            employment_start_date DATE,
            employment_end_date DATE NULL,
            grade TEXT,
            remote_work_days TEXT,
            registered_address TEXT,
            actual_residence_address TEXT
        )
        """)
        # Заполняем таблицу случайно сгенерированными данными о сотруднике.
        # Для тестов необходимо подгонять под результат
        cls.cur.execute("""
            INSERT INTO employee_info (
                employment_status, 
                employment_start_date, 
                employment_end_date, 
                grade, 
                remote_work_days, 
                registered_address, 
                actual_residence_address
                )
            VALUES
                ('Active', '2020-01-01', NULL, 3, 'Monday,Wednesday,Friday', '123 Main St, City1, Country1', 
                '456 Elm St, City2, Country2'),
                ('Active', '2019-05-15', NULL, 1, 'Tuesday,Thursday', '789 Oak St, City3, Country3', 
                '321 Maple St, City4, Country4'),
                ('Inactive', '2018-08-20', '2022-03-01', 3, 'Monday,Wednesday,Friday', '987 Pine St, City5, 
                Country5', '654 Birch St, City6, Country6'),
                ('Active', '2021-03-10', NULL, 2, 'Tuesday,Thursday', '147 Walnut St, City7, Country7', 
                '258 Cedar St, City8, Country8'),
                ('Active', '2017-11-25', NULL, 3, 'Monday,Wednesday,Friday', '369 Chestnut St, City9, 
                Country9', '741 Spruce St, City10, Country10'),
                ('Inactive', '2019-09-30', '2023-02-15', 1, 'Tuesday,Thursday', '963 Pineapple St, City11, 
                Country11', '852 Banana St, City12, Country12'),
                ('Active', '2022-06-05', NULL, 3, 'Monday,Wednesday,Friday', '159 Grape St, City13, 
                Country13', '753 Orange St, City14, Country14'),
                ('Active', '2020-12-12', NULL, 1, 'Tuesday,Thursday', '852 Apple St, City15, Country15', 
                '963 Pear St, City16, Country16'),
                ('Inactive', '2018-04-18', '2024-01-20', 3, 'Monday,Wednesday,Friday', '357 Peach St, City17, 
                Country17', '468 Plum St, City18, Country18'),
                ('Active', '2023-09-22', NULL, 1, 'Tuesday,Thursday', '579 Berry St, City19, Country19', 
                '684 Watermelon St, City20, Country20');
        """)
        cls.db.commit()

    @classmethod
    def get_employee_info_for_processing(cls, id):
        # Получаем информацию о сотруднике по id
        cls.cur.execute(f"""
            SELECT *
            FROM employee_info
            WHERE id = {id}
            LIMIT 1
        """)

        employee = cls.cur.fetchone()

        if employee:
            # Возвращаем информацию в виде схемы
            return schemas.EmployeeInfo(**employee)
        else:
            return None
