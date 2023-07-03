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

'''my_request = (f'SELECT vacancies.name, COUNT(posts.id)\n'
              f'FROM posts\n'
              f'JOIN vacancies ON posts.vacancy_id = vacancies.id\n'
              f'JOIN employers ON employers.id = vacancies.employer_id\n'
              f'WHERE employers.tg_id = 1052862634\n'
              f'GROUP BY vacancies.id')
print(a.get_reporting(my_request))'''
