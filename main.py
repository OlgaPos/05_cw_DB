from config import config
from dbmanager import DBManager
from hh import HeadHunter
from utils import create_employers_list, create_database, save_data_to_database, create_tables_in_database


def main():
    # Создаём список работодателей из json-файла работодателей
    employers_list = create_employers_list("employers.json")
    # print(employers_list)

    # Запрашивает у пользователя ключевое слово, по которому будет производиться поиск.
    keyword = input('Здравствуйте! Введите ключевое слово для поиска вакансий: \n')

    hh = HeadHunter()
    hh_data = hh.get_request(keyword)
    # print(hh_data)
    selected_vacancies = hh.select_vacancies(employers_list, hh_data)
    # print(selected_vacancies)
    short_vacancies = hh.get_short_vacancies(selected_vacancies)
    # print(short_vacancies)

    params = config()

    create_database("hh_vacancies", params)
    create_tables_in_database("hh_vacancies", params)
    save_data_to_database(short_vacancies, "hh_vacancies", params)

    db = DBManager("hh_vacancies", params)

    print(f"Результат получен.")
    while True:
        user_input = input("\nВы хотите посмотреть детальную информацию? Y/N\n")
        if user_input.lower() == "y":

            while True:
                print(f"Что Вы хотите посмотреть?:\n\
                    1 - Количество вакансий по работодателю\n\
                    2 - Все вакансии\n\
                    3 - Среднюю зарплату по вакансиям\n\
                    4 - Вакансии, у которых зарплата выше средней по найденным вакансиям\n\
                    5 - Вакансии, в названии которых содержится ключевое слово")

                user_input = int(input("Введите ваш выбор\n"))
                if user_input == 1:
                    print("Количество вакансий по работодателю\n")
                    print(db.get_companies_and_vacancies_count())
                    break
                elif user_input == 2:
                    print("Все вакансии\n")
                    print(db.get_all_vacancies())
                    break
                elif user_input == 3:
                    print("Средняя зарплата по вакансиям\n")
                    print(db.get_avg_salary())
                    break
                elif user_input == 4:
                    print("Вакансии, у которых зарплата выше средней по найденным вакансиям\n")
                    print(db.get_vacancies_with_higher_salary())
                    break
                elif user_input == 5:
                    keyword2 = str(input("Введите ключевое слово\n"))
                    print(f"Вакансии, в названии которых содержится {keyword2}\n")
                    print(db.get_vacancies_with_keyword(keyword2))
                    break
                else:
                    print("Нет такого варианта. Выберете ещё раз.\n")
                    continue

        elif user_input.lower() == "n":
            print(f"До свидания. Приходите ещё.")
            break
        else:
            print("Нет такого варианта. Повторите пожалуйста ваш выбор.\n")
            continue


if __name__ == '__main__':
    main()
