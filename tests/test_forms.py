from app.forms import UserForm, SnippetCreateForm


def test_forms_user_email():
    """Тестируем форму логина пользователя"""
    user_data = {
        "email": "student@example.ru",
        "password": "пароль123"
    }
    try:
        form = UserForm(**user_data)
        if form.email == "student@example.ru":
            print("\nEmail правильный!")
        else:
            print("\nEmail не совпадает")

    except Exception as e:
        print(f"\nОшибка при создании формы: {e}")


def test_forms_snippets():
    """Тест для создания сниппета"""
    snippet_data = {
        "title": "Мой первый код",
        "code": "print('Привет, мир!')",
        "description": "Это мой первый сниппет"
    }
    try:
        form = SnippetCreateForm(**snippet_data)
        if len(form.code) > 0:
            print("\nКод не пустой!")
        else:
            print("\nКод пустой!")

    except Exception as e:
        print(f"\nОшибка: {e}")
