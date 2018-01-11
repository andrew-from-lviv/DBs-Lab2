HOST = 'localhost'
USER = 'postgres'
PASSWORD = '[Ak95Vm96]'
FLIGHT_DB = 'KLMDB'
HOTEL_DB = 'BookingDB'
BANK_DB = 'BankDB'
XID = 1

TAKE_MONEY_COMMAND = "update public.Account set Amount = Amount - 100 where ClientName = 'vasia'";
CREATE_FLIGHT_COMMAND = "INSERT INTO public.Flights( ClientName, FlightNumber, \"From\", \"To\", DateTime) VALUES('vasia_test_fail_all', 'KLM 730', 'LVI', 'WAR', '2017-05-05'); ";
CREATE_HOTEL_BOOKING_COMMAND = "INSERT INTO public.hotelbookings(clientname, hotelname, arrival, departure)	VALUES('vasia_test_fail_all', 'ibis', '2017-05-05', '2017-05-07'); ";