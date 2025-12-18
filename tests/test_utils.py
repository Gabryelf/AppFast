from app.utils import format_date, get_password_hash


def test_formator_dates():
    """Тестируем форматирование дат"""

    date1 = "2025-12-11T14:30:00"
    result1 = format_date(date1)
    print(f"\nВход: {date1}")
    print(f"Выход: {result1}")
    assert "2025-12-11 14:30" in result1


def test_get_hashed_password():
    """Тестируем хеширования пароля"""
    password = "мой_пароль123"
    hashed = get_password_hash(password)
    print(f"\nПароль: {password}")
    print(f"\nХеш:    {hashed[:20]}...")

    if len(hashed) > 10:
        print("   ✅ Пароль захеширован!")
    else:
        print("   ❌ Хеш слишком короткий")

