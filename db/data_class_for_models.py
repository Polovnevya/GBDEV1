from dataclasses import dataclass


@dataclass
class CandidateData:
    first_name: str
    middle_name: str
    last_name: str
    gender: str
    age: str
    education: str
    phone: str
    tg_id: str


data = {'first_name': 'Юрий',
        'middle_name': 'Андреевич',
        'last_name': 'Половнев',
        'gender': 'male',
        'age': 'senior',  # тут должны быть значения энамов, а не ключи
        'education': 'higher',
        'phone': '+79134903369',
        'tg_id': 618432846}

candidate_data = CandidateData(**data)
