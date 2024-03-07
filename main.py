import pathlib
import sqlite3 as sq


def start_connection():
    db = sq.connect(str(pathlib.Path(__file__).parent.parent) + '/tg.db', isolation_level=None)
    db.row_factory = sq.Row
    cur = db.cursor()

    cur.execute("""
        DROP TABLE IF EXISTS restaurants
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS rides(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE,
        request_time TIME,
        arriving_time TIME,
        order_phone TEXT,
        order_method TEXT,
        day_of_ride TEXT,
        username TEXT,
        ride_group TEXT,
        
        ssp_current TEXT,
        ssp_during_order TEXT,
        passenger_phone TEXT,
        email TEXT,
        employee_id INTEGER,
        passenger_pd TEXT,
        
        ride_id INTEGER,
        city TEXT,
        address_from TEXT,
        address_stay TEXT,
        address_to TEXT,
        coordinates_from TEXT,
        coordinates_stay TEXT,
        coordinates_to TEXT,
        
        fare TEXT,
        commentary TEXT,
        ride_cost INTEGER,
        waiting_cost INTEGER,
        waiting_time_from INTEGER,
        
        waiting_time_stay INTEGER,
        ride_goal TEXT,        
        cost_of_toil_road INTEGER
        )
    """)

    cur.execute("""
        INSERT INTO rides (name, address, neighborhood, avg_cost, main_cuisine)
        VALUES
        ('rest_1', 'dfokdf', 'юг', 1000, 'итальянская')
    """)
    db.commit()
    return db, cur