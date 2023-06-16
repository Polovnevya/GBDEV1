import enum
from dataclasses import dataclass


# dataclasses
@dataclass
class DAOFeedback:
    candidate_id: int
    id_vacancy: int


@dataclass
class DAOVacancy:
    id: int
    name: str
    work_schedule: str
    employment: str
    salary: float


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
    male = "жен."
    female = "муж."


class EducationEnum(enum.Enum):
    secondary = "среднее образование"
    vocational = "средннее профессиональное образование"
    higher = "высшее образование"


class AgeCategoriesEnum(enum.Enum):
    junior = "от 18 до 25"
    middle = "от 25 до 40"
    senior = "от 40 до 60"
