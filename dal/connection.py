import pathlib
import sqlite3 as sq


class SqlitePool:
    db = None
    cur = None

    @classmethod
    def start_connection(cls):  # Создается подключение к файлу tg.db
        cls.db = sq.connect(str(pathlib.Path(__file__).parent.parent) + '/tg.db', isolation_level=None)
        cls.db.row_factory = sq.Row
        cls.cur = cls.db.cursor()

    @classmethod
    def get_db_cur(cls):
        # Функция для получения переменных db и cur.
        # Нужно для того, чтобы эти переменные были едины для всех файлов в dal
        return cls.db, cls.cur

