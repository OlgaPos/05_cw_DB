from abc import ABC, abstractmethod

import requests


class Engine(ABC):
    @abstractmethod
    def get_request(self, keyword):
        """Запрашивает вакансии, в том числе через API"""
        pass


class HeadHunter(Engine):
    URL = 'https://api.hh.ru/vacancies'

    def get_request(self, keyword) -> list:
        """Скачивает данные с сайта HH по ключевому слову"""
        data = []
        response = requests.get(url=self.URL, params={"text": f"{keyword}", "per_page": 100, "page": 0})
        if response.status_code == 200:
            data = response.json()
        else:
            print("Что-то пошло не так")  # mozhno ubrat' ili peredelat' test
        return data

    @staticmethod
    def select_vacancies(employers_list, data) -> list:
        selected_vacancies = []
        for vacancy in data['items']:
            employer_name = vacancy.get("employer", {}).get("name", "")
            # print(employer_name)
            # vacancy_id = vacancy.get("id")
            # print(vacancy_id)
            if employer_name in employers_list:
                selected_vacancies.append(vacancy)
        return selected_vacancies

    @staticmethod
    def get_short_vacancies(selected_vacancies) -> list:
        """Возвращает список с короткими вакансиями"""
        hh_vacancies = []
        count = 0
        requirements = ''
        description = ''
        for i in selected_vacancies:
            if i["snippet"]["requirement"] is None:
                description = "Нет деталей"
            elif "<highlighttext>" and "</highlighttext>" in i["snippet"]["requirement"]:
                requirements = i["snippet"]["requirement"].replace("<highlighttext>", "") \
                    .replace("</highlighttext>", "")
            if i["snippet"]["responsibility"] is None:
                description = "Нет деталей"
            elif "<highlighttext>" and "</highlighttext>" in i["snippet"]["responsibility"]:
                description = i["snippet"]["responsibility"].replace("<highlighttext>", "") \
                    .replace("</highlighttext>", "")
            if i["salary"] is None:
                salary_from = 0
                salary_currency = ""
            elif i["salary"].get('from') is None:
                salary_from = 0
                salary_currency = ""
            else:
                salary_from = i["salary"].get('from')
                salary_currency = i["salary"].get('currency')
            hh_vacancy = {"vacancy_id": i["id"], "position": i["name"], "requirements": requirements,
                          "position_description": description, "city": i["area"]["name"], "salary_from": salary_from,
                          "currency": salary_currency, "employer_id": i["employer"]["id"],
                          "employer_name": i["employer"]["name"], "url": i["url"]
                          }
            # "employer_id": i["employer"]["id"], "employer_url": i["employer"]["url"],
            count += 1
            # print(hh_vacancy)
            hh_vacancies.append(hh_vacancy)
        # print(count)
        return hh_vacancies
