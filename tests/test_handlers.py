from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_api_health():
    """Тест работоспособности роутеров API"""
    response = client.get("/")

    print(f"\nСтатус код: {response.status_code}")

    if response.status_code == 200:
        print("✓ Наше приложение работает!")
    else:
        print("✗ Что-то пошло не так...")

    assert response.status_code != 500

