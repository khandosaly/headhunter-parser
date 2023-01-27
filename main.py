from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

from builders import VacancyBuilder
from models import Vacancy


def main():
    driver = webdriver.Chrome(service=Service('/usr/local/bin/chromedriver'))

    vacancy_ids = []

    for i in range(0, 40):
        driver.get(f'https://astana.hh.kz/search/vacancy?area=159&only_with_salary=true&page={i}')
        hrefs: [WebElement] = driver.find_elements(by=By.XPATH, value="//a[@data-qa='serp-item__title']")
        vacancy_ids.extend([x.get_attribute('href').split('vacancy/', 1)[1].split('?from')[0] for x in hrefs])

    vacancies = []

    for vacancy_id in vacancy_ids:
        builder = VacancyBuilder(driver=driver, vacancy_id=int(vacancy_id))
        vacancy: Vacancy = builder.build()
        vacancies.append(vacancy)
        print(vacancy)


if __name__ == '__main__':
    main()

