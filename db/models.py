from decimal import Decimal
from typing import List
from sqlalchemy import Enum, Float, Boolean, Table, Column
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, validates
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from sqlalchemy_utils import EmailType, PhoneNumberType
from validate_email import validate_email


class Base(DeclarativeBase):
    pass


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


class DateBaseModel:
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, onupdate=datetime.now, nullable=True)
    deleted_at: Mapped[datetime] = mapped_column(DateTime, nullable=True)


class ContactBaseModel:
    email: Mapped[EmailType] = mapped_column(EmailType, nullable=False, unique=True)
    phone: Mapped[PhoneNumberType] = mapped_column(
        PhoneNumberType(region="RU", check_region=True, max_length=12),
        nullable=False,
        unique=True,
    )

    @validates("email")
    def validate_email(self, key, address):
        if not validate_email(address):
            raise ValueError("failed email validation")
        return address


class Candidate(Base, DateBaseModel):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(primary_key=True)
    feedback: Mapped[List["Feedback"]] = relationship()
    user_name: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    chat_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    gender: Mapped[Enum] = mapped_column(Enum(GenderEnum), nullable=False)
    age: Mapped[Enum] = mapped_column(Enum(AgeCategoriesEnum), nullable=False)
    education: Mapped[Enum] = mapped_column(Enum(EducationEnum), nullable=False)
    phone: Mapped[PhoneNumberType] = mapped_column(
        PhoneNumberType(region="RU", check_region=True, max_length=12),
        nullable=False,
        unique=True,
    )

    def __repr__(self):
        return f"<id: {self.id}, user_name: {self.user_name}, user_id: {self.user_id}, " \
               f"chat_id: {self.chat_id}, first_name: {self.first_name}, middle_name: {self.last_name}, " \
               f"last_name: {self.last_name}, gender: {self.gender}, age: {self.age}, education: {self.education}, " \
               f"phone: {self.phone}, " \
               f"created_at: {self.created_at}, updated_at: {self.updated_at}, deleted_at: {self.updated_at}>"


class Audience(Base, DateBaseModel):
    __tablename__ = "audiences"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    vacancy: Mapped[List["Vacancy"]] = relationship()

    def __repr__(self):
        return f"<id: {self.id}, name: {self.name},  " \
               f"created_at: {self.created_at}, updated_at: {self.updated_at}, deleted_at: {self.updated_at}>"


class Employer(Base, ContactBaseModel, DateBaseModel):
    __tablename__ = "employers"

    id: Mapped[int] = mapped_column(primary_key=True)
    vacancy: Mapped[List["Vacancy"]] = relationship()
    user_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    chat_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    company_name = mapped_column(String(50), nullable=False)

    def __repr__(self):
        return f"<id: {self.id}, user_name: {self.user_name}, user_id: {self.user_id}, " \
               f"chat_id: {self.chat_id}, company_name: {self.first_name}, " \
               f"phone: {self.phone}, email: {self.email}, " \
               f"created_at: {self.created_at}, updated_at: {self.updated_at}, deleted_at: {self.updated_at}>"


class Vacancy(Base, DateBaseModel):
    __tablename__ = "vacancies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    feedback: Mapped[List["Feedback"]] = relationship()
    post: Mapped[List["Post"]] = relationship()
    name: Mapped[str] = mapped_column(String, nullable=False)
    employer_id: Mapped[int] = mapped_column(ForeignKey("employers.id"), nullable=False)
    audience_id: Mapped[int] = mapped_column(ForeignKey("audiences.id"), nullable=False)
    work_schedule: Mapped[Enum] = mapped_column(Enum(WorkScheduleEnum), nullable=False)
    employment: Mapped[Enum] = mapped_column(Enum(EmploymentEnum), nullable=False)
    salary: Mapped[Decimal] = mapped_column(Float, nullable=False)
    geolocation: Mapped[str] = mapped_column(String, nullable=False)
    is_open: Mapped[bool] = mapped_column(Boolean, default=True)
    date_start: Mapped[datetime] = mapped_column(DateTime)
    date_end: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self):
        return f"<id: {self.id}, vacancy_name: {self.name}, employer_id: {self.employer_id}, " \
               f"audience_id: {self.audience_id}, work_schedule: {self.work_schedule}, salary: {self.salary}, " \
               f"geolocation: {self.geolocation}, is_open: {self.is_open}, " \
               f" date_start: {self.date_start}, date_end: {self.date_end}, " \
               f"created_at: {self.created_at}, updated_at: {self.updated_at}, deleted_at: {self.updated_at}>"


class Feedback(Base, DateBaseModel):
    __tablename__ = "feedback"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), nullable=False)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"), nullable=False)

    def __repr__(self):
        return f"<id: {self.id}, candidate_id: {self.candidate_id}, vacancy_id: {self.vacancy_id}, " \
               f"created_at: {self.created_at}, updated_at: {self.updated_at}, deleted_at: {self.updated_at}>"


channel_to_audience = Table(
    "channel_to_audience",
    Base.metadata,
    Column("channel_id", ForeignKey("channels.id"), primary_key=True),
    Column("audience_id", ForeignKey("audiences.id"), primary_key=True),
)


class Channel(Base, DateBaseModel):
    __tablename__ = "channels"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    channel_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    audience: Mapped[List[Audience]] = relationship(secondary=channel_to_audience)

    def __repr__(self):
        return f"<id: {self.id}, name: {self.name}, channel_id: {self.channel_id}, audience: {self.audience.key}, " \
               f"created_at: {self.created_at}, updated_at: {self.updated_at}, deleted_at: {self.updated_at}>"


class Post(Base, DateBaseModel):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    message_id: Mapped[int] = mapped_column(unique=True, nullable=False)
    vacancy_id: Mapped[int] = mapped_column(ForeignKey("vacancies.id"), nullable=False)
    channel_id: Mapped[int] = mapped_column(ForeignKey("channels.id"), nullable=False)

    def __repr__(self):
        return f"<id: {self.id}, vacancy_id: {self.vacancy_id.key}, message_id: {self.massage_id} " \
               f"channel_id {self.channel_id}, " \
               f"created_at: {self.created_at}, updated_at: {self.updated_at}, deleted_at: {self.updated_at}>"
