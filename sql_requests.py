# Количество откликов на вакансию
request1 = (f'SELECT vacancies.name, COUNT(posts.id)\n'
              f'FROM posts\n'
              f'JOIN vacancies ON posts.vacancy_id = vacancies.id\n'
              f'JOIN employers ON employers.id = vacancies.employer_id\n'
              #f'WHERE employers.tg_id = {callback.from_user.id}\n'
              #f'GROUP BY vacancies.id'
              )

# Количество опубликованных постов с вакансией--
request2 = (f'SELECT vacancies.name, COUNT(posts.id)\n'
               f'FROM posts\n'
               f'JOIN vacancies ON posts.vacancy_id = vacancies.id\n'
               f'JOIN employers ON employers.id = vacancies.employer_id\n'
               #f'WHERE employers.tg_id = {callback.from_user.id}\n'
               #f'GROUP BY vacancies.id'
               )
