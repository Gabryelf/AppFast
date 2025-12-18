import pytest
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch
from app.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def sample_user_data():
    return {
        "email": "test@user.com",
        "password": "123456",
        "first_name": "Test",
        "last_name": "Test",
        "nick_name": "Test"
    }


def test_register_user_success(test_client, sample_user_data):
    mock_session = Mock()

    mock_session.query.return_value.filter.return_value.first.return_value = None

    with patch('app.handlers.connect_db') as mock_connect_db, \
            patch('app.handlers.User') as MockUser, \
            patch('app.handlers.get_password_hash') as mock_hash, \
            patch('app.database.create_engine') as mock_engine, \
            patch('app.database.SessionLocal') as mock_session_local:
        def mock_db_generator():
            yield mock_session

        mock_connect_db.return_value = mock_db_generator()
        mock_new_user = Mock()
        mock_new_user.id = 1
        MockUser.return_value = mock_new_user

        mock_hash.return_value = "hashed_password_123"
        mock_session_local.return_value = mock_session
        mock_engine_instance = Mock()
        mock_engine.return_value = mock_engine_instance
        response = test_client.post("/register", json=sample_user_data)

    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["message"] == "User created successfully"

    mock_session.add.assert_called_once_with(mock_new_user)
    mock_session.commit.assert_called_once()

    print("Тест успешной регистрации пройден!")
