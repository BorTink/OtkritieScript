import pathlib
import sqlite3 as sq


class SqlitePool:
    db = None
    cur = None

    @classmethod
    def start_connection(cls):
        cls.db = sq.connect(str(pathlib.Path(__file__).parent.parent) + '/tg.db', isolation_level=None)
        cls.db.row_factory = sq.Row
        cls.cur = cls.db.cursor()

    @classmethod
    def get_db_cur(cls):
        return cls.db, cls.cur

