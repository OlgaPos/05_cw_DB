import json
from typing import Any, List, Dict
import psycopg2


def create_employers_list(json_file: str) -> list:
    """Получение списка работодателей из файла json"""
    with open(json_file, "r", encoding="UTF-8") as f:
        data = json.load(f)

    employers_list = []
    for i in data:
        employer_name = i.get("employer_name")
        employers_list.append(employer_name)
    return employers_list


def create_database(database_name: str, params: dict) -> None:
    """Создание БД для хранения данных о работодателях и вакансиях"""
    conn = psycopg2.connect(dbname="postgres", **params)
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute(f'DROP DATABASE IF EXISTS {database_name}')
    cur.execute(f'CREATE DATABASE {database_name}')

    cur.close()
    conn.close()


def create_tables_in_database(database_name: str, params: dict) -> None:
    """Создание таблиц в БД для хранения данных о работодателях и вакансиях"""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                employer_id int PRIMARY KEY,
                employer_name varchar
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE vacancies (
                vacancy_id int PRIMARY KEY,
                position_name varchar,
                requirements text,
                position_description text,
                city varchar,
                salary_from int,
                currency varchar(3),
                employer_name varchar,
                employer_id int REFERENCES employers(employer_id),
                url text
            )
        """)
    conn.commit()
    conn.close()


def save_data_to_database(data: List[Dict[str, Any]], database_name: str, params: Dict) -> None:
    """Сохранение данных в базу данных"""
    conn = psycopg2.connect(dbname=database_name, **params)
    with conn.cursor() as cur:
        employers_list = []
        for i in data:
            if i["employer_name"] in employers_list:   # Проверяет, что работодатель уже существует
                continue   # Пропустить, если работодатель уже существует
            employers_list.append(i["employer_name"])

            cur.execute(
                """
                INSERT INTO employers (employer_id, employer_name)
                VALUES (%s, %s)
                """,
                (i["employer_id"], i["employer_name"])
            )

    # with conn.cursor() as cur:
        for i in data:
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, position_name, requirements, position_description, city, salary_from,
                currency, employer_name, employer_id, url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (i["vacancy_id"], i["position"], i["requirements"], i["position_description"], i["city"],
                 i["salary_from"], i["currency"], i["employer_name"], i["employer_id"], i["url"])
            )
    print(employers_list)
    conn.commit()
    conn.close()
