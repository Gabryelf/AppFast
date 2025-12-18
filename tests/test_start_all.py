from test_forms import test_forms_snippets, test_forms_user_email
from test_handlers import test_api_health
from test_utils import test_formator_dates, test_get_hashed_password

"""Последовательный запуск всех тестов"""
test1 = test_forms_snippets()
test2 = test_forms_user_email()
test3 = test_api_health()
test4 = test_formator_dates()
test5 = test_get_hashed_password()


def run_tests_all():
    test_files = [
        test1,
        test2,
        test3,
        test4,
        test5
    ]
    total_tests = 0
    passed_tests = 0

    for test_file in test_files:
        try:
            exec(open(test_file).read())
            passed_tests += 1
            print(f"\n{test_file} - ВЫПОЛНЕН УСПЕШНО")
        except Exception as e:
            print(f"\n{test_file} - ОШИБКА: {e}")

        total_tests += 1

        if passed_tests == total_tests:
            print("\nВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        else:
            print(f"\nЕсть проблемы в {total_tests - passed_tests} тестах")


if __name__ == "__main__":
    run_tests_all()

