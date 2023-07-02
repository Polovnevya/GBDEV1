from .models import EducationEnum, AgeCategoriesEnum, GenderEnum, WorkScheduleEnum, EmploymentEnum
from datetime import datetime, timedelta

fixtures = {
    "candidate": [
        {
            "tg_id": 1,
            "first_name": "Иван",
            "middle_name": "Иванович",
            "last_name": "Иванов",
            "gender": GenderEnum.male,
            "age": AgeCategoriesEnum.junior,
            "education": EducationEnum.secondary,
            "phone": "9111111111"
        },
        {
            "tg_id": 2,
            "first_name": "Петр",
            "middle_name": "Петрович",
            "last_name": "Петров",
            "gender": GenderEnum.male,
            "age": AgeCategoriesEnum.senior,
            "education": EducationEnum.higher,
            "phone": "9222222222"
        }
    ],
    "employer": [
        {
            "user_name": "@GoodCompany",
            "tg_id": 3,
            "company_name": "хорошая компания",
            "email": "goodcompany@email.ru",
            "phone": "9333333333",
        },
        {
            "user_name": "@BadCompany",
            "tg_id": 4,
            "company_name": "плохая компания",
            "email": "badcompany@email.ru",
            "phone": "9444444444",
        },
    ],
    "audience": [
        {
            "name": "IT",
        },
        {
            "name": "неквалифицированные работники"
        },
    ],
    "vacancy": [
        {
            "name": "сетевой инженер",
            "employer_id": 1,
            "audience_id": 1,
            "work_schedule": WorkScheduleEnum.remote,
            "employment": EmploymentEnum.full_time,
            "salary": 150_000.50,
            "geolocation": "69.347654, 88.207752",
            "date_start": datetime(2023, 7, 2, 18, 42, 13, 933058),
            "date_end": datetime(2023, 7, 4, 18, 42, 13, 933058),
        },
        {
            "name": "грузчик",
            "employer_id": 2,
            "audience_id": 2,
            "work_schedule": WorkScheduleEnum.flexible,
            "employment": EmploymentEnum.internship,
            "salary": 15_000.75,
            "geolocation": "69.348269, 88.212360",
            "date_start": datetime(2023, 7, 2, 18, 42, 13, 933058),
            "date_end": datetime(2023, 7, 4, 18, 42, 13, 933058),
        },
    ],
    "feedback": [
        {
            "candidate_id": 1,
            "vacancy_id": 1,
        },
        {
            "candidate_id": 2,
            "vacancy_id": 2,
        },
    ],
    "channel": [
        {
            "name": "IT вакансии 1",
            "channel_id": -1001753724398,
        },
        {
            "name": "неквалифицированные вакансии",
            "channel_id": -1001829933123,
        },
    ],
    "channel_by_audiences": [
        {
            "channel_id": 1,
            "audience_id": 1,
        },
        {
            "channel_id": 1,
            "audience_id": 2,
        },
    ],
    "post": [
        {
            "vacancy_id": 1,
            "channel_id": 1,
            "message_id": 1,
        },
        {
            "vacancy_id": 2,
            "channel_id": 2,
            "message_id": 2,
        },
    ]
}
