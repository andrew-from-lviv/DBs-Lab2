import psycopg2

from src.config import *


class TwoPahaseCommit:
    def __init__(self):
        try:
            self.bank_connection = psycopg2.connect(host = HOST, user = USER,
                                                    password = PASSWORD, dbname = BANK_DB)
            self.booking_connection = psycopg2.connect(host=HOST, user=USER,
                                                       password=PASSWORD, dbname=HOTEL_DB)
            self.flight_connection = psycopg2.connect(host=HOST, user=USER,
                                                    password=PASSWORD, dbname=FLIGHT_DB)

        except Exception as e:
            print(e)

    def execute_commands(self, connections, commands):
        if len(connections) != len(commands):
            raise Exception("Some bad configuration")

        for i in range(0, len(connections)):
            connections[i].cursor().execute(commands[i])
            connections[i].tpc_prepare()

    def commit_transactions(self, transactions):
        for transaction in transactions:
            transaction.tpc_commit()


    def close_connections(self, connections):
        for connection in connections:
            connection.close()


    def rollback_transactions(self, connections):
        for conn in connections:
            conn.tpc_rollback()


    def do_work(self):
        try:
            connections, commands = self.setup_transaction()

            self.execute_commands(connections, commands)

            self.commit_transactions(connections)

            self.close_connections(connections)
        except Exception as e:
            print(e)
            self.rollback_transactions(connections)
            self.close_connections(connections)


    def setup_transaction(self):
        connections = []
        self.booking_connection.tpc_begin(self.booking_connection.xid(XID, 'trID', 'conn2'))
        connections.append(self.booking_connection)
        self.flight_connection.tpc_begin(self.flight_connection.xid(XID, 'trID', 'conn3'))
        connections.append(self.flight_connection)
        self.bank_connection.tpc_begin(self.bank_connection.xid(XID, 'trID', 'conn1'))
        connections.append(self.bank_connection)

        commands = [CREATE_HOTEL_BOOKING_COMMAND, CREATE_FLIGHT_COMMAND, TAKE_MONEY_COMMAND]

        return connections, commands


tpc = TwoPahaseCommit()
tpc.do_work()



