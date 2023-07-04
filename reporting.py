import psycopg2
from config.config import load_config


class Reporting:

    def __init__(self,
                 database=load_config().db.database,
                 db_user=load_config().db.db_user,
                 db_password=load_config().db.db_password,
                 db_host=load_config().db.db_host
                 ):
        self.database = database
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host

    def get_cursor(self):
        con = psycopg2.connect(database=self.database,
                               user=self.db_user,
                               password=self.db_password,
                               host=self.db_host)
        cursor = con.cursor()
        return cursor

    def get_reporting(self, my_request):
        self.my_request = my_request
        sample_cursor = Reporting()
        cursor = sample_cursor.get_cursor()
        cursor.execute(my_request)
        return cursor.fetchall()
