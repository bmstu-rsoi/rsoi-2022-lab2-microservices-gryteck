import psycopg2
from psycopg2 import Error
import datetime

class FlightDB:
    def __init__(self):
        self.DB_URL = "postgres://xdhoxdcbsgxlxx:f4dfbfb50de63f82e758615d34aac4b999f7f6e3914347c3eeb5e8dc1d324e7e@ec2-54-194-180-51.eu-west-1.compute.amazonaws.com:5432/db3120dunkqj65"

        if not self.check_existing_table_airport():
            self.create_table_airport()
        if not self.check_existing_table_flight():
            self.create_table_flight()



    def check_existing_table_flight(self):
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        for table in cursor.fetchall():
            if table[0] == "flight":
                cursor.close()
                return True
        cursor.close()
        connection.close()
        return False


    def check_existing_table_airport(self):
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        for table in cursor.fetchall():
            if table[0] == "airport":
                cursor.close()
                return True
        cursor.close()
        connection.close()
        return False



    def create_table_flight(self):
        q1 = '''
                    CREATE TABLE flight
                    (
                        id              SERIAL PRIMARY KEY,
                        flight_number   VARCHAR(20)              NOT NULL,
                        datetime        TIMESTAMP WITH TIME ZONE NOT NULL,
                        from_airport_id INT REFERENCES airport (id),
                        to_airport_id   INT REFERENCES airport (id),
                        price           INT                      NOT NULL
                    );
                    '''
        q2 = '''
                    INSERT INTO flight
                    (
                        id,
                        flight_number,
                        datetime,
                        from_airport_id,
                        to_airport_id,
                        price
                    )
                    VALUES 
                    (
                        1,
                        'AFL031',
                        '2021-10-08 20:00',
                        1,
                        2,
                        1500
                    );
                    '''
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute(q1)
        cursor.execute(q2)
        connection.commit()
        cursor.close()
        connection.close()



    def create_table_airport(self):
        p = '''
                    CREATE TABLE airport
                    (
                        id      SERIAL PRIMARY KEY,
                        name    VARCHAR(255),
                        city    VARCHAR(255),
                        country VARCHAR(255)
                    );
                    '''
        p1 = '''
                    INSERT INTO airport
                    (
                        id,
                        name,
                        city,
                        country
                    )
                    VALUES 
                    (
                        1,
                        'Шереметьево',
                        'Москва',
                        'Россия'
                    );
                    '''        
        p2 = '''
                    INSERT INTO airport
                    (
                        id,
                        name,
                        city,
                        country
                    )
                    VALUES 
                    (
                        2,
                        'Пулково',
                        'Санкт-Петербург',
                        'Россия'
                    );
                    '''
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute(p)
        cursor.execute(p1)
        cursor.execute(p2)
        connection.commit()
        cursor.close()
        connection.close()



    def get_flights(self):
        result = list()
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute("SELECT id, flight_number, datetime, from_airport_id, to_airport_id, price FROM flight")
        record = cursor.fetchall()
        for i in record:
            i = list(i)
            result.append({'id': i[0], "flight_number": i[1], "datetime": i[2], "from_airport_id": i[3], "to_airport_id": i[4], "price": i[5]})
        return result



    def flight_exist(self, flight_number):
        query = f"SELECT EXISTS(SELECT * FROM flight WHERE flight_number = '{flight_number}');"
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        if result:
            query = f"SELECT " \
                    f"(SELECT city ||' '||name FROM airport WHERE flight.from_airport_id = airport.id) AS from_airport, " \
                    f"(SELECT city ||' '||name FROM airport WHERE flight.to_airport_id = airport.id) AS to_airport, " \
                    f"datetime, price FROM flight WHERE flight_number = '{flight_number}';"
            self.cursor.execute(query)
            flight_info = self.cursor.fetchone()
            d = dict()
            d['flight_number'] = flight_number
            d['from_airport'] = flight_info[0]
            d['to_airport'] = flight_info[1]
            d['date'] = flight_info[2]
            d['price'] = flight_info[3]
            result = d
        return result



    def db_disconnect(self):
        self.cursor.close()
        self.connection.close()