# REST сервис для управления CAT параметрами

## Варианты запуска:

- Запуск всех сервисов с помощью `docker-compose -f docker-compose-full.yml up`
- Отдельный запуск app и celery,redis,postgres:
    - Запускаем сервисы celery, redis, postgres - `docker-compose up`
    - Активируем виртуальное окружение
    - Устанавливаем зависимости через `poetry install`
    - Запускаем приложение `python manage.py runserver`

**Важно!** Перед запуском всех сервисов необходимо создать `.env` файл. [Настройка .env файла](docs/setup_env_file.md)

**Важно!** Если вы запускаете все сервисы с помощью `docker-compose-full.yml`, то в `.env` файле должны быть указанны
параметры `DB_HOST`, `CELERY_BROKER_URL`, `CELERY_RESULT_BACKEND` в качестве названия сервисов `docker-compose-full.yml`
файла. Если же вы запускаете, только celery, redis, postgres, то эти параметры должны уже содержать url адрес (например
127.0.0.1)

## Дополнительная документация:

- [Доступные маршруты](docs/routes.md)
- [Настройка .env файла](docs/setup_env_file.md)
- [Дополнительная информация](docs/additional.md)