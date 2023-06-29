import psycopg2


class Reporting:
    database = 'gbdev1',
    user = 'postgres',
    password = 'postgres',
    host = 'localhost'

    def get_cursor(self):
        con = psycopg2.connect(database=Reporting.database[0],
                               user=Reporting.user[0],
                               password=Reporting.password[0],
                               host=Reporting.host)
        cursor = con.cursor()
        return cursor

    def get_reporting(self, my_request):
        self.my_request = my_request
        sample_cursor = Reporting()
        cursor = sample_cursor.get_cursor()
        cursor.execute(my_request)
        return cursor.fetchall()


'''a = Reporting()
my_request = (f'SELECT vacancies.name, COUNT(posts.id)\n'
              f'FROM posts\n'
              f'JOIN vacancies ON posts.vacancy_id = vacancies.id\n'
              f'JOIN employers ON employers.id = vacancies.employer_id\n'
              f'WHERE employers.tg_id = 1052862634\n'
              f'GROUP BY vacancies.id')
print(a.get_reporting(my_request))'''
