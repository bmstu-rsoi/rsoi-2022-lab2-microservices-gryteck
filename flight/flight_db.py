import psycopg2
from psycopg2 import Error
import datetime

class FlightsDB:
    def __init__(self):
        self.connnection = psycopg2.connect(
            database="flights",
            user="user",
            password="password",
            host="10.5.0.2",
            port="5432"
        )
        self.cursor = self.connection.cursor()
        if not self.check_existing_table_airport():
            self.create_table_airport()
        if not self.check_existing_table_flight():
            self.create_table_flight()



    def check_existing_table_flight(self):
        self.cursor.execute(
            f"SELECT EXISTS (SELECT 1 AS result FROM pg_tables WHERE tablename = 'flight');")
        tableExists = self.cursor.fetchone()[0]
        return tableExists



    def check_existing_table_airport(self):
        self.cursor.execute(
            f"SELECT EXISTS (SELECT 1 AS result FROM pg_tables WHERE tablename = 'airport');")
        tableExists = self.cursor.fetchone()[0]
        return tableExists



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
                        price,
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
        cursor.execute(q)
        connection.commit()
        cursor.close()
        connection.close()



    def create_table_airport(self):
        p = '''
                    CREATE TABLE reservation
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
                        1,
                        'Пулково',
                        'Санкт-Петербург',
                        'Россия'
                    );
                    '''
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute(q)
        connection.commit()
        cursor.close()
        connection.close()



    def get_flights(self):
        result = list()
        try:
            connection = psycopg2.connect(self.DB_URL, sslmode="require")
            cursor = connection.cursor()
            cursor.execute("SELECT id, flight_number, datetime, from_airport_id, to_airport_id, price FROM ticket")
            record = cursor.fetchall()
            for i in record:
                i = list(i)
                result.append({'id': i[0], "flight_number": i[1], "datetime": i[2], "from_airport_id": i[3], "to_airport_id": i[4], "price": i[5]})
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
        return result



    def flight_exist(self, flight_number):
        query = f"SELECT EXISTS(SELECT * FROM flight WHERE flight_number = '{flight_number}');"
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
            d['flightNumber'] = flight_number
            d['fromAirport'] = flight_info[0]
            d['toAirport'] = flight_info[1]
            d['date'] = flight_info[2]
            d['price'] = flight_info[3]
            result = d
        return result



    def db_disconnect(self):
        self.cursor.close()
        self.connection.close()