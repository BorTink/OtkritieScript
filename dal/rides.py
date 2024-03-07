from connection import SqlitePool


class Rides:
    db, cur = SqlitePool.get_db_cur()

    @classmethod
    def create_rides(cls):
        cls.cur.execute("""
                DROP TABLE IF EXISTS rides
            """)
        cls.cur.execute("""
                CREATE TABLE rides(
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

        cls.cur.execute("""
                INSERT INTO rides (
                    date, request_time, arriving_time, order_phone, order_method, day_of_ride, username, ride_group, 
                    ssp_current, ssp_during_order, passenger_phone, email, employee_id, passenger_pd, 
                    ride_id, city, address_from, address_stay, address_to, coordinates_from, coordinates_stay, 
                    coordinates_to, fare, commentary, ride_cost, waiting_cost, waiting_time_from, 
                    waiting_time_stay, ride_goal, cost_of_toil_road
                    )
                VALUES 
                    ('2024-03-07', '09:00:00', '09:30:00', '1234567890', 'app', 'Monday', 'user1', 'group1', 
                     'ssp1', 'ssp2', '9876543210', 'user1@example.com', 1, 'passenger1', 
                     1, 'City1', 'Address1', 'Stay1', 'Destination1', '1.2345,1.2345', '1.2345,1.2345', 
                     '1.2345,1.2345', '20.00', 'No comments', 50, 10, 5, 
                     15, 'Work', 100),
                    ('2024-03-08', '10:00:00', '10:30:00', '2345678901', 'phone', 'Tuesday', 'user2', 'group2', 
                     'ssp2', 'ssp3', '8765432109', 'user2@example.com', 2, 'passenger2', 
                     2, 'City2', 'Address2', 'Stay2', 'Destination2', '2.3456,2.3456', '2.3456,2.3456', 
                     '2.3456,2.3456', '25.00', 'Some comments', 60, 15, 10, 
                     20, 'Meeting', 120),
                    ('2024-03-09', '11:00:00', '11:30:00', '3456789012', 'web', 'Wednesday', 'user3', 'group3', 
                     'ssp3', 'ssp4', '7654321098', 'user3@example.com', 3, 'passenger3', 
                     3, 'City3', 'Address3', 'Stay3', 'Destination3', '3.4567,3.4567', '3.4567,3.4567', 
                     '3.4567,3.4567', '30.00', 'More comments', 70, 20, 15, 
                     25, 'Shopping', 140),
                    ('2024-03-10', '12:00:00', '12:30:00', '4567890123', 'app', 'Thursday', 'user4', 'group4', 
                     'ssp4', 'ssp5', '6543210987', 'user4@example.com', 4, 'passenger4', 
                     4, 'City4', 'Address4', 'Stay4', 'Destination4', '4.5678,4.5678', '4.5678,4.5678', 
                     '4.5678,4.5678', '35.00', 'Additional comments', 80, 25, 20, 
                     30, 'Entertainment', 160),
                    ('2024-03-11', '13:00:00', '13:30:00', '5678901234', 'phone', 'Friday', 'user5', 'group5', 
                     'ssp5', 'ssp6', '5432109876', 'user5@example.com', 5, 'passenger5', 
                     5, 'City5', 'Address5', 'Stay5', 'Destination5', '5.6789,5.6789', '5.6789,5.6789', 
                     '5.6789,5.6789', '40.00', 'Extra comments', 90, 30, 25, 
                     35, 'Other', 180),
                    ('2024-03-12', '14:00:00', '14:30:00', '6789012345', 'web', 'Saturday', 'user6', 'group6', 
                     'ssp6', 'ssp7', '4321098765', 'user6@example.com', 6, 'passenger6', 
                     6, 'City6', 'Address6', 'Stay6', 'Destination6', '6.7890,6.7890', '6.7890,6.7890', 
                     '6.7890,6.7890', '45.00', 'Final comments', 100, 35, 30, 
                     40, 'Vacation', 200),
                    ('2024-03-13', '15:00:00', '15:30:00', '7890123456', 'app', 'Sunday', 'user7', 'group7', 
                     'ssp7', 'ssp8', '3210987654', 'user7@example.com', 7, 'passenger7', 
                     7, 'City7', 'Address7', 'Stay7', 'Destination7', '7.8901,7.8901', '7.8901,7.8901', 
                     '7.8901,7.8901', '50.00', 'Last comments', 110, 40, 35, 
                     45, 'Visit', 220),
                    ('2024-03-14', '16:00:00', '16:30:00', '8901234567', 'phone', 'Monday', 'user8', 'group8', 
                     'ssp8', 'ssp9', '2109876543', 'user8@example.com', 8, 'passenger8', 
                     8, 'City8', 'Address8', 'Stay8', 'Destination8', '8.9012,8.9012', '8.9012,8.9012', 
                     '8.9012,8.9012', '55.00', 'Final remarks', 120, 45, 40, 
                     50, 'Business', 240),
                    ('2024-03-15', '17:00:00', '17:30:00', '9012345678', 'web', 'Tuesday', 'user9', 'group9', 
                     'ssp9', 'ssp10', '1098765432', 'user9@example.com', 9, 'passenger9', 
                     9, 'City9', 'Address9', 'Stay9', 'Destination9', '9.0123,9.0123', '9.0123,9.0123', 
                     '9.0123,9.0123', '60.00', 'Final notes', 130, 50, 45, 
                     55, 'Education', 260),
                    ('2024-03-16', '18:00:00', '18:30:00', '0123456789', 'app', 'Wednesday', 'user10', 'group10', 
                     'ssp10', 'ssp1', '0987654321', 'user10@example.com', 10, 'passenger10', 
                     10, 'City10', 'Address10', 'Stay10', 'Destination10', '10.1234,10.1234', '10.1234,10.1234', 
                     '10.1234,10.1234', '65.00', 'Final thoughts', 140, 55, 50, 
                     60, 'Others', 280);
            """)
        cls.db.commit()
