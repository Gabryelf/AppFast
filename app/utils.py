import hashlib


def get_password_hash(password: str) -> str:
    """Хэширование пароля"""
    return hashlib.sha256(password.encode()).hexdigest()


def format_images(images: list) -> str:
    """Форматирование списка изображений в JSON строку"""
    import json
    return json.dumps(images) if images else "[]"


def parse_images(images_json: str) -> list:
    """Парсинг JSON строки в список изображений"""
    import json
    try:
        return json.loads(images_json) if images_json else []
    except json.JSONDecodeError:
        return []
