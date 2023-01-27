from dataclasses import dataclass


@dataclass
class Vacancy:
    id: int
    title: str
    salary_from: int
    salary_to: int | None
    salary_currency: str
    salary_net: bool
    experience: str
    employment_mode: str
    employment_schedule: str
    company_name: str
    city: str
    address: str | None
    description: str
    tags: [str]

    def __str__(self):
        main = f'[{self.id}] {self.title}'

        salary_from = f'(от {self.salary_from}'
        if self.salary_to:
            salary_to = f'до {self.salary_to}'
        else:
            salary_to = ''
        if self.salary_net:
            salary_net = 'на руки)'
        else:
            salary_net = 'до вычета налогов)'

        salary = f'{salary_from} {salary_to} {self.salary_currency} {salary_net}'

        return f'{main} {salary} \n' \
               f'Опыт: {self.experience}, {self.employment_mode}, {self.employment_schedule} \n' \
               f'Компания: {self.company_name}, {self.city} {self.address if self.address else ""} \n' \
               f'Тэги: {", ".join(self.tags)}' \
               #f'Описание: {self.description} \n' \
