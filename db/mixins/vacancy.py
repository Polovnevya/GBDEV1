from typing import List
from sqlalchemy import select
from ..models import Vacancy
from ..types import DAOVacancy, WorkScheduleEnum, EmploymentEnum



# TODO запилить реализацию
async def get_vacancy_by_id(self, vacancy_id: int) -> Vacancy:
    """
    Возвращает 1 вкансию по ее id
    :param vacancy_id:
    :return:
    """
    pass


# TODO запилить реализацию
async def get_vacancy_by_geolocation(self, longitude: float, latitude: float) -> List[DAOVacancy]:
    """
    возвращает список вакансий, по широте и долготе
    в определенном радиусе (можно в конфиг пробросить и вытаскивать потом из него)
    произвести сортировку вакансий по возрастанию расстояния от соискателя - первым делом показываем самые ближние

    запилить датакласс под широту и долготу? и под вакансии тож надо бы

    :param longitude:
    :param latitude:
    :return:
    """
    # заглушка
    vacancy_data = [
        {
            "id": "1",
            "name": "сетевой инженер",
            "work_schedule": WorkScheduleEnum.remote.value,
            "employment": EmploymentEnum.full_time.value,
            "salary": 150_000.50,
        },
        {
            "id": "2",
            "name": "грузчик",
            "work_schedule": WorkScheduleEnum.flexible.value,
            "employment": EmploymentEnum.internship.value,
            "salary": 15_000.75,
        },
        {
            "id": "3",
            "name": "админ",
            "work_schedule": WorkScheduleEnum.flexible.value,
            "employment": EmploymentEnum.internship.value,
            "salary": 15_000.75,
        },
        {
            "id": "4",
            "name": "разраб",
            "work_schedule": WorkScheduleEnum.flexible.value,
            "employment": EmploymentEnum.internship.value,
            "salary": 15_000.75,
        },
        {
            "id": "5",
            "name": "страдатель фигней",
            "work_schedule": WorkScheduleEnum.flexible.value,
            "employment": EmploymentEnum.internship.value,
            "salary": 15_000.75,
        },
        {
            "id": "6",
            "name": "отпускник",
            "work_schedule": WorkScheduleEnum.flexible.value,
            "employment": EmploymentEnum.internship.value,
            "salary": 15_000.75,
        },
        {
            "id": "7",
            "name": "еще грузчик",
            "work_schedule": WorkScheduleEnum.flexible.value,
            "employment": EmploymentEnum.internship.value,
            "salary": 15_000.75,
        },
    ]
    return vacancy_data