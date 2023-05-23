import psycopg2


class DBManager:

    def __init__(self, dbname, params):
        self.dbname = dbname
        self.params = params

    def _execute_query(self, query):
        """Возвращает результат запроса из БД"""
        conn = psycopg2.connect(dbname=self.dbname, **self.params)
        with conn.cursor() as cur:
            cur.execute(query)
            result = cur.fetchall()
        conn.close()
        return result

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        result = self._execute_query("SELECT employer_name, COUNT(*) AS vacancies FROM vacancies "
                                     "GROUP BY employer_name ORDER BY COUNT(*) DESC")

        return result

    def get_all_vacancies(self):
        """Получает список всех вакансий с указанием работодателя, названия вакансии, зарплаты и ссылки."""
        result = self._execute_query("SELECT employer_name, position_name, salary_from, currency, url FROM vacancies "
                                     "ORDER BY salary_from DESC")

        return result

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        result = self._execute_query("SELECT ROUND(AVG(salary_from)) FROM vacancies "
                                     "WHERE salary_from <> 0")

        return result

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        result = self._execute_query("SELECT * FROM vacancies "
                                     "WHERE salary_from > (SELECT AVG(salary_from) "
                                     "FROM vacancies WHERE salary_from <> 0) "
                                     "ORDER BY salary_from DESC")

        return result

    def get_vacancies_with_keyword(self, keyword2):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например “python”."""
        result = self._execute_query("SELECT * FROM vacancies "
                                     f"WHERE position_name LIKE '%{keyword2}%'")

        return result
