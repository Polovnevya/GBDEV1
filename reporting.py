import psycopg2
import config


class Reporting:

    def __init__(self):
        self.database = config.config.load_config().db.database
        self.user = config.config.load_config().db.db_user
        self.password = config.config.load_config().db.db_password
        self.host = config.config.load_config().db.db_host

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
