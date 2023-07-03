from typing import List
from sqlalchemy import select
from ..models import Vacancy
from ..types import DAOVacancyData, WorkScheduleEnum, EmploymentEnum
from geopy.distance import geodesic as GD
from operator import attrgetter


class DAOVacancyMixin:
    sql_manager = None

    async def get_vacancy_by_id(self, vacancy_id: int) -> DAOVacancyData:
        """
        Возвращает 1 вкансию по ее id
        :param vacancy_id:
        :return:
        """
        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                stmt = select(Vacancy).where(Vacancy.id == vacancy_id).where(
                    Vacancy.deleted_at is not None)
                result = await session.scalars(stmt)
                tmp = result.first()
                if tmp:
                    vacancy = tmp

                    return DAOVacancyData(
                        id=vacancy.id,
                        employer_id=vacancy.employer_id,
                        audience_id=vacancy.audience_id,
                        name=vacancy.name,
                        work_schedule=vacancy.work_schedule,
                        employment=vacancy.employment,
                        salary=vacancy.salary,
                        geolocation=vacancy.geolocation,
                        is_open=vacancy.is_open,
                        date_start=vacancy.date_start,
                        date_end=vacancy.date_end
                    )

    async def get_vacancy_by_geolocation(self, longitude: float = None, latitude: float = None) -> List[DAOVacancyData]:
        """
        возвращает список вакансий, по широте и долготе
        в определенном радиусе (можно в конфиг пробросить и вытаскивать потом из него)
        произвести сортировку вакансий по возрастанию расстояния от соискателя - первым делом показываем самые ближние

        запилить датакласс под широту и долготу? и под вакансии тож надо бы

        :param longitude:
        :param latitude:
        :return:
        """
        vacancies_list = []
        await self.sql_manager.create_async_session()
        async with self.sql_manager.async_session() as session:
            async with session.begin():
                stmt = select(Vacancy).where(Vacancy.deleted_at is not None)
                vacancies = await session.scalars(stmt)

                for vacancy in vacancies:
                    vacancy_data = DAOVacancyData(
                        id=vacancy.id,
                        employer_id=vacancy.employer_id,
                        audience_id=vacancy.audience_id,
                        name=vacancy.name,
                        work_schedule=vacancy.work_schedule,
                        employment=vacancy.employment,
                        salary=vacancy.salary,
                        geolocation=vacancy.geolocation,
                        is_open=vacancy.is_open,
                        date_start=vacancy.date_start,
                        date_end=vacancy.date_end,
                    )

                    if longitude and latitude:
                        candidate_geolocation = f"{longitude}, {latitude}"
                        vacancy_geolocation = vacancy.geolocation
                        distance_from_candidate_to_vacancy = GD(candidate_geolocation, vacancy_geolocation).km
                        vacancy_data.distance_from_candidate_to_vacancy = distance_from_candidate_to_vacancy
                    vacancies_list.append(vacancy_data)

        if longitude and latitude:
            vacancies_list = sorted(vacancies_list, key=attrgetter("distance_from_candidate_to_vacancy"))

        return vacancies_list
        # заглушка
        # vacancy_data = [
        #     {
        #         "id": "1",
        #         "name": "сетевой инженер",
        #         "work_schedule": WorkScheduleEnum.remote.value,
        #         "employment": EmploymentEnum.full_time.value,
        #         "salary": 150_000.50,
        #     },
        #     {
        #         "id": "2",
        #         "name": "грузчик",
        #         "work_schedule": WorkScheduleEnum.flexible.value,
        #         "employment": EmploymentEnum.internship.value,
        #         "salary": 15_000.75,
        #     },
        #     {
        #         "id": "3",
        #         "name": "админ",
        #         "work_schedule": WorkScheduleEnum.flexible.value,
        #         "employment": EmploymentEnum.internship.value,
        #         "salary": 15_000.75,
        #     },
        #     {
        #         "id": "4",
        #         "name": "разраб",
        #         "work_schedule": WorkScheduleEnum.flexible.value,
        #         "employment": EmploymentEnum.internship.value,
        #         "salary": 15_000.75,
        #     },
        #     {
        #         "id": "5",
        #         "name": "страдатель фигней",
        #         "work_schedule": WorkScheduleEnum.flexible.value,
        #         "employment": EmploymentEnum.internship.value,
        #         "salary": 15_000.75,
        #     },
        #     {
        #         "id": "6",
        #         "name": "отпускник",
        #         "work_schedule": WorkScheduleEnum.flexible.value,
        #         "employment": EmploymentEnum.internship.value,
        #         "salary": 15_000.75,
        #     },
        #     {
        #         "id": "7",
        #         "name": "еще грузчик",
        #         "work_schedule": WorkScheduleEnum.flexible.value,
        #         "employment": EmploymentEnum.internship.value,
        #         "salary": 15_000.75,
        #     },
        # ]
        # return vacancy_data

    async def insert_vacancy(self,vacancy:DAOVacancyData):
        pass