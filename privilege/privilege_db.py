import psycopg2
from psycopg2 import Error
import datetime

class PrivilegeDB:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="privileges",
            user="program",
            password="test",
            host="10.5.0.2",
            port="5432"
        )
        self.cursor = self.connection.cursor()
        if not self.check_existing_table_privilege():
            self.create_table_privilege()
        if not self.check_existing_table_privilege_history():
            self.create_table_privilege_history()



    def check_existing_table_privilege(self):
        self.cursor.execute(
            f"SELECT EXISTS (SELECT 1 AS result FROM pg_tables WHERE tablename = 'privilege');")
        tableExists = self.cursor.fetchone()[0]
        return tableExists



    def check_existing_table_privilege_history(self):
        self.cursor.execute(
            f"SELECT EXISTS (SELECT 1 AS result FROM pg_tables WHERE tablename = 'privilege_history');")
        tableExists = self.cursor.fetchone()[0]
        return tableExists



    def create_table_privilege(self):
        q1 = '''
                    CREATE TABLE privilege
                    (
                        id       SERIAL PRIMARY KEY,
                        username VARCHAR(80) NOT NULL UNIQUE,
                        status   VARCHAR(80) NOT NULL DEFAULT 'BRONZE'
                        CHECK (status IN ('BRONZE', 'SILVER', 'GOLD')),
                        balance  INT
                    );
                '''
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute(q1)
        cursor.execute(q2)
        connection.commit()
        cursor.close()
        connection.close()

    def create_table_privilege_history(self):
        q2 = '''
                    CREATE TABLE privilege_history
                    (
                        id             SERIAL PRIMARY KEY,
                        privilege_id   INT REFERENCES privilege (id),
                        ticket_uid     uuid        NOT NULL,
                        datetime       TIMESTAMP   NOT NULL,
                        balance_diff   INT         NOT NULL,
                        operation_type VARCHAR(20) NOT NULL
                            CHECK (operation_type IN ('FILL_IN_BALANCE', 'DEBIT_THE_ACCOUNT'))
                    );
                '''
        connection = psycopg2.connect(self.DB_URL, sslmode="require")
        cursor = connection.cursor()
        cursor.execute(q1)
        cursor.execute(q2)
        connection.commit()
        cursor.close()
        connection.close()
    
    def get_privilege(self, username):
        query = f"SELECT id FROM privilege WHERE username='{username}'"
        self.cursor.execute(query)
        user_id = self.cursor.fetchone()[0]
        query = f"SELECT status, balance FROM privilege WHERE username='{username}'"
        self.cursor.execute(query)
        user_info = self.cursor.fetchone()
        query = f"SELECT ticket_uid, datetime, balance_diff, operation_type FROM privilege_history " \
                f"WHERE privilege_id='{user_id}' "
        self.cursor.execute(query)
        user_history = self.cursor.fetchall()
        response = {'balance': user_info[1], 'status': user_info[0], 'history': []}
        for i in user_history:
            d = dict()
            d['ticket_uid'] = i[0]
            d['date'] = i[1]
            d['balance_diff'] = i[2]
            d['operation_type'] = i[3]
            response['history'].append(d)
        return response



    def privilege_down(self, data):
        query = f"SELECT balance FROM privilege WHERE username='{data['username']}'"
        self.cursor.execute(query)
        balance_bonus = int(self.cursor.fetchone()[0])
        if data['price'] <= balance_bonus:
            new_balance_bonus = balance_bonus - int(data['price'])
            balance_diff = int(data['price'])
        else:
            new_balance_bonus = 0
            balance_diff = balance_bonus
        query = f"UPDATE privilege SET balance = {new_balance_bonus} WHERE username='{data['username']}';"
        self.cursor.execute(query)
        query = f"SELECT id FROM privilege WHERE username='{data['username']}'"
        self.cursor.execute(query)
        user_id = int(self.cursor.fetchone()[0])
        query = 'INSERT INTO privilege_history (privilege_id, ticket_uid, datetime, balance_diff, operation_type) ' \
                'VALUES (%s,%s,%s,%s,%s);'
        insert_data = (user_id, data['ticketUid'], '2021-10-08T19:59:19Z', balance_diff, 'DEBIT_THE_ACCOUNT')
        self.cursor.execute(query, insert_data)
        return str(balance_diff)



    def privilege_up(self, data):
        balance_diff = int(0.1 * int(data['price']))
        query = f"UPDATE privilege SET balance = balance+{balance_diff} WHERE username='{data['username']}';"
        self.cursor.execute(query)
        query = f"SELECT id FROM privilege WHERE username='{data['username']}'"
        self.cursor.execute(query)
        user_id = int(self.cursor.fetchone()[0])
        query = 'INSERT INTO privilege_history (privilege_id, ticket_uid, datetime, balance_diff, operation_type) ' \
                'VALUES (%s,%s,%s,%s,%s);'
        insert_data = (user_id, data['ticketUid'], '2021-10-08T19:59:19Z', balance_diff, 'FILL_IN_BALANCE')
        self.cursor.execute(query, insert_data)
        return



    def db_disconnect(self):
        self.cursor.close()
        self.connection.close()
