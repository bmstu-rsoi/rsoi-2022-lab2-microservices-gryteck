import psycopg2
from psycopg2 import Error
import uuid

class TicketDB:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="postgres",
            # host="10.5.0.2",
            port="5433"
        )
        self.cursor = self.connection.curs()


        if not self.check_existing_table_tickets():
            self.create_table_tickets()



    def check_existing_table_tickets(self):
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute("""SELECT table_name FROM information_schema.tables
               WHERE table_schema = 'public'""")
        for table in cursor.fetchall():
            if table[0] == "ticket":
                cursor.close()
                return True
        cursor.close()
        connection.close()
        return False


    def create_table_tickets(self):
        q = '''
                    CREATE TABLE ticket
                    (
                        id            SERIAL PRIMARY KEY,
                        ticket_uid    uuid UNIQUE NOT NULL,
                        username      VARCHAR(80) NOT NULL,
                        flight_number VARCHAR(20) NOT NULL,
                        price         INT         NOT NULL,
                        status        VARCHAR(20) NOT NULL
                            CHECK (status IN ('PAID', 'CANCELED'))
                    );
                    '''
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute(q)
        connection.commit()
        cursor.close()
        connection.close()



    def get_tickets(self):
        result = list()
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute("SELECT id, ticket_uid, username, flight_number, price, status FROM ticket")
        record = cursor.fetchall()
        for i in record:
            i = list(i)
            result.append({'id': i[0], "ticket_Uid": i[1], "username": i[2], "flight_number": i[3], "price": i[4]})
        return result



    def get_ticket_by_uid(self, ticket_uid, username):
        query = f"SELECT EXISTS(SELECT * FROM ticket WHERE ticket_uid = '{ticket_uid}' AND username = '{username}');"
        self.cursor.execute(query)
        result = self.cursor.fetchone()[0]
        if not result:
            return result
        query = f"SELECT flight_number, status FROM ticket WHERE ticket_uid = '{ticket_uid}';"
        self.cursor.execute(query)
        tmp = self.cursor.fetchone()
        result = dict()
        result['flight_number'] = tmp[0]
        result['status'] = tmp[1]
        return result



    def buy_ticket(self, data):

        
        ticket_uid = str(uuid.uuid4())
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        insert_query = """ INSERT INTO ticket (ticket_uid, username, flight_number, price, status) VALUES (%s, %s, %s, %s, %s) """
        cursor.execute(insert_query, (ticket_uid, data['username'], data['flight_number'], data['price'], data['status']))
        connection.commit()
        return ticket_uid


    def return_ticket(self, ticket_Uid):
        result = ''
        try:
            connection = psycopg2.connect(self.DB_URL, sslmode="require")
            cursor = connection.cursor()
            q1 = ''' UPDATE ticket SET status = %s WHERE ticket_uid = %s; '''
            cursor.execute(q1, ('CANCELED', ticket_Uid))
            r = cursor.rowcount
            connection.commit()
            if r > 0:
                result = payment_uid[0]
        except (Exception, Error) as error:
            print("Ошибка при работе с PostgreSQL", error)
        finally:
            if connection:
                cursor.close()
                connection.close()
        return result


    def db_disconnect(self):
        self.cursor.close()
        self.connection.close()