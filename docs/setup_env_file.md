# Настройка `.env`

## Необходимые параметры:

- ### DEBUG - `Boolean` - Default (`False`)

Режим работы Django

- ### DB_NAME - `String`

Имя для базы данных

- ### DB_USER - `String`

Имя пользователя базы данных

- ### DB_USER_PASSWORD - `String`

Пароль пользователя базы данных

- ### DB_PORT - `Integer`

Порт на котором работает бд

- ### DB_HOST - `String` - Default (`localhost`)

Хост на котором запущена база данных

- ### ACCESS_TOKEN_LIFETIME_STR - `String`

Строка с формата `number time`. Отвечает за время жизни токена

Доступные варианты `time`:

- `day(s)`
- `hour(s)`
- `minute(s)`
- `second(s)`

Примеры: `1 day`, `10 minutes`, `5 seconds`...

- ### PASSWORD_RESET_TOKEN_LIFETIME_STR - `String`

Строка с формата `number time`. Отвечает за время жизни токена для сброса пароля пользователя

Доступные варианты `time`:

- `day(s)`
- `hour(s)`
- `minute(s)`
- `second(s)`

Примеры: `1 day`, `10 minutes`, `5 seconds`...

- ### CELERY_BROKER_URL - `String`

URL для Celery Broker.

Пример: `redis://127.0.0.1`

- ### CELERY_RESULT_BACKEND - `String`

URL для Celery Result.

Пример: `redis://127.0.0.1`

- ### EMAIL_HOST - `String`

Хост через который будет осуществляться отправка писем

Пример: `smtp.gmail.com`

- ### EMAIL_PORT - `Integer`

Порт хоста через который будет осуществляться отправка писем

- ### EMAIL_HOST_USER - `String`

Email адрес хоста, который будет отправлять письма

- ### EMAIL_HOST_PASSWORD

Пароль от хоста, который будет отправлять письма

- ### ALLOWED_HOSTS - `List[String]`

Список хостов, которым разрешено обращаться к API.

Если список будет вида `["*"]` - доступ разрешен всем хостам.

**Важно** Редирект по Oauth, а так же ссылка для письма сброса пароля валидируются по этой переменной.
Если хоста не будет в `ALLOWED_HOST`, то и редиректа, а так же ссылки с этим хостом в письме не будет

- ### SOCIAL_AUTH_GOOGLE_OAUTH2_KEY - `String`

Ключ доступа приложения google. Необходим для oauth авторизации

- ### SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET - `String`

Секретный ключ приложения google. Необходим для oauth авторизации


