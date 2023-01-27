from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

from models import Vacancy


class VacancyBuilder:

    def __init__(self, driver: webdriver, vacancy_id: int):
        self.driver: webdriver = driver
        self.vacancy_id: int = vacancy_id

    def _get_title(self) -> str:
        return self._xpath("//h1[@data-qa='vacancy-title']").text.strip()

    def _get_salaries(self) -> (int, int, str, bool):
        try:
            raw_salary = self._xpath("//span[@data-qa='vacancy-salary-compensation-type-gross']").get_attribute('innerHTML')
            salary_net = False
        except NoSuchElementException:
            raw_salary = self._xpath("//span[@data-qa='vacancy-salary-compensation-type-net']").get_attribute('innerHTML')
            salary_net = True

        tokens = raw_salary.replace('&nbsp;', '').split('<!-- -->')
        if len(tokens) == 1:
            tokens = raw_salary.replace('&nbsp;', '').split('<!---->')

        salary_from = int(tokens[1].strip())

        has_salary_to = True
        if '<span' in tokens[3]:
            has_salary_to = False

        if has_salary_to:
            salary_to = int(tokens[3].strip())
            salary_currency = tokens[5].split('<')[0].strip()
        else:
            salary_to = None
            salary_currency = tokens[3].split('<')[0].strip()

        return salary_from, salary_to, salary_currency, salary_net

    def _get_experience(self) -> str:
        return self._xpath("//span[@data-qa='vacancy-experience']").text.strip()

    def _get_employment_mode(self) -> (str, str):
        employment_text = self._xpath("//p[@data-qa='vacancy-view-employment-mode']").text
        return [t.strip() for t in employment_text.split(',')]

    def _get_company_name(self) -> str:
        return self._xpath("//a[@data-qa='vacancy-company-name']").text.strip()

    def _get_company_address(self) -> (str, str):
        try:
            return self._xpath("//p[@data-qa='vacancy-view-location']").text.strip(), None
        except NoSuchElementException:
            raw_address = self._xpath("//span[@data-qa='vacancy-view-raw-address']").text
            if ',' in raw_address:
                tokens = raw_address.split(',', 1)
                return tokens[0].strip(), tokens[1].strip()
            else:
                return raw_address.strip(), None

    def _get_description(self) -> str:
        return self._xpath("//div[@data-qa='vacancy-description']").text.strip()

    def _get_tags(self) -> [str]:
        tag_elements = self.driver.find_elements(by=By.XPATH, value="//span[@data-qa='bloko-tag__text']")
        return [t.text for t in tag_elements]

    def _xpath(self, xpath_str: str):
        return self.driver.find_element(by=By.XPATH, value=xpath_str)

    def build(self):
        self.driver.get(f'https://astana.hh.kz/vacancy/{self.vacancy_id}')

        salary_from, salary_to, salary_currency, salary_net = self._get_salaries()
        employment_mode, employment_schedule = self._get_employment_mode()
        city, address = self._get_company_address()

        vacancy: Vacancy = Vacancy(
            id=int(self.vacancy_id),
            title=self._get_title(),
            salary_from=salary_from,
            salary_to=salary_to,
            salary_currency=salary_currency,
            salary_net=salary_net,
            experience=self._get_experience(),
            employment_mode=employment_mode,
            employment_schedule=employment_schedule,
            company_name=self._get_company_name(),
            city=city,
            address=address,
            description=self._get_description(),
            tags=self._get_tags()
        )

        return vacancy
