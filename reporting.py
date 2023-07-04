import psycopg2
from config.config import load_config


class Reporting:

    def __init__(self):
        self.database = load_config().db.database
        self.user = load_config().db.db_user
        self.password = load_config().db.db_password
        self.host = load_config().db.db_host

    def get_cursor(self):
        con = psycopg2.connect(database=self.database,
                               user=self.user,
                               password=self.password,
                               host=self.host)
        cursor = con.cursor()
        return cursor

    def get_reporting(self, my_request):
        self.my_request = my_request
        sample_cursor = Reporting()
        cursor = sample_cursor.get_cursor()
        cursor.execute(my_request)
        return cursor.fetchall()
