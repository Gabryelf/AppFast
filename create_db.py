import pymysql

# Подключение к MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='sksmel544332',
    charset='utf8mb4'
)

try:
    with connection.cursor() as cursor:
        # Создаем базу
        cursor.execute("CREATE DATABASE IF NOT EXISTS app_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("✅ Database 'app_db' created/verified")

        # Показываем все базы
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        print(f"📋 Available databases: {databases}")

    connection.commit()
finally:
    connection.close()
