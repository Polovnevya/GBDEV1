import enum
from dataclasses import dataclass
from datetime import datetime


# dataclasses
@dataclass
class DAOFeedbackData:
    candidate_id: int
    vacancy_id: int


@dataclass
class DAOVacancyData:
    employer_id: int
    audience_id: int
    name: str
    work_schedule: str
    employment: str
    salary: float
    geolocation: str
    is_open: bool
    date_start: datetime
    date_end: datetime


@dataclass
class DAOCandidateData:
    first_name: str
    middle_name: str
    last_name: str
    gender: str
    age: str
    education: str
    phone: str
    tg_id: str
    id: int = None


@dataclass
class DAOEmployerData:
    company_name: str
    phone: str
    email: str
    tg_id: str

@dataclass
class ReportingPostsResponses:
    vacancy_id: int
    vacancy_name: str
    number_posts: int
    number_responses: int


@dataclass
class ReportingVacancy:
    vacancy_id: int
    vacancy_name: str
    male: int
    female: int
    junior: int
    middle: int
    senior: int
    secondary: int
    vocational: int
    higher: int


# enums

class EmploymentEnum(enum.Enum):
    full_time = "полная занятость"
    part_time = "частичная занятость"
    internship = "стажировка"
    single = "проектная работа/разовое задание"
    volunteering = "волонтёрство"


class WorkScheduleEnum(enum.Enum):
    full_day = "полный день"
    shift = "сменный"
    flexible = "гибкий"
    remote = "удаленная работа"


class GenderEnum(enum.Enum):
    male = "муж."
    female = "жен."


class EducationEnum(enum.Enum):
    secondary = "среднее образование"
    vocational = "средннее профессиональное образование"
    higher = "высшее образование"


class AgeCategoriesEnum(enum.Enum):
    junior = "от 18 до 25"
    middle = "от 25 до 40"
    senior = "от 40 до 60"


class AudienceEnum(enum.Enum):
    IT = "IT"
    unskilled_workers = "неквалифицированные работники"