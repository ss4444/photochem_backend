

# Запуск проекта

1. Добавить файл .env и .env.local_docker в корень репозитория
2. Отметить папку **app** как SourceRoot
3. Выполнить команду `alembic upgrade head` - создание таблиц в бд
4. Запуск веб-сервера: `python cli.py auth`