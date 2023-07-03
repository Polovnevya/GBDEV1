request1 = (f'SELECT vacancies.id, vacancies.name, COUNT(candidates.id)\n'
            f'FROM employers\n'
            f'JOIN vacancies ON employers.id = vacancies.employer_id\n'
            f'JOIN feedback ON vacancies.id = feedback.vacancy_id\n'
            f'JOIN candidates ON feedback.candidate_id = candidates.id\n'
            # f'WHERE employers.tg_id = {callback.from_user.id}\n'
            # f'GROUP BY vacancies.id'
            )

# Количество опубликованных постов с вакансией--
request2 = (f'SELECT vacancies.id, vacancies.name, COUNT(posts.id)\n'
            f'FROM posts\n'
            f'JOIN vacancies ON posts.vacancy_id = vacancies.id\n'
            f'JOIN employers ON employers.id = vacancies.employer_id\n'
            # f'WHERE employers.tg_id = {callback.from_user.id}\n'
            # f'GROUP BY vacancies.id'
            )


request3 = (
    f'WITH\n'
    f'number_responses AS (\n'
        f'SELECT vacancies.id, COUNT(candidates.id) AS count_responses\n'
        f'FROM employers\n'
        f'JOIN vacancies ON employers.id = vacancies.employer_id\n'
        f'JOIN feedback ON vacancies.id = feedback.vacancy_id\n'
        f'JOIN candidates ON feedback.candidate_id = candidates.id\n'
        f'WHERE employers.tg_id = 3\n'
        f'GROUP BY vacancies.id),\n'
    f'number_posts AS (\n'
        f'SELECT vacancies.id AS id, vacancies.name AS name, COUNT(posts.id) AS count_posts\n'
        f'FROM posts\n'
        f'JOIN vacancies ON posts.vacancy_id = vacancies.id\n'
        f'JOIN employers ON employers.id = vacancies.employer_id\n'
        f'WHERE employers.tg_id = 3\n'
        f'GROUP BY vacancies.id)\n'
    f'SELECT number_posts.id, number_posts.name, number_posts.count_posts, number_responses.count_responses\n'
    f'FROM number_posts LEFT OUTER JOIN number_responses ON number_posts.id=number_responses.id;')
