import psycopg2
from psycopg2.extensions import connection, ISOLATION_LEVEL_READ_COMMITTED

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

    def do_work(self):
        try:
            self.setup_transaction()

            self.flight_connection.cursor().execute(CREATE_FLIGHT_COMMAND)
            self.flight_connection.tpc_prepare()

            self.booking_connection.cursor().execute(CREATE_HOTEL_BOOKING_COMMAND)
            self.booking_connection.tpc_prepare()

            self.bank_connection.cursor().execute(TAKE_MONEY_COMMAND)
            self.bank_connection.tpc_prepare()

            self.bank_connection.tpc_commit()
            self.booking_connection.tpc_commit()
            self.flight_connection.tpc_commit()

            self.flight_connection.close()
            self.booking_connection.close()
            self.bank_connection.close()
        except Exception as e:
            print(e)
            self.flight_connection.tpc_rollback()
            self.bank_connection.tpc_rollback()
            self.booking_connection.tpc_rollback()


    def setup_transaction(self):
        self.bank_connection.tpc_begin(self.bank_connection.xid(XID, 'trID', 'conn1'))
        self.booking_connection.tpc_begin(self.booking_connection.xid(XID, 'trID', 'conn2'))
        self.flight_connection.tpc_begin(self.flight_connection.xid(XID, 'trID', 'conn3'))



