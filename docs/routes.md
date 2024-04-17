# Маршруты приложения

- ### `GET` - `HOST/api/parameters/`

Возвращает список параметров формата:

```json
[
  {
    "id": "number",
    "cat_id": "string",
    "data_length": "string",
    "length": "string",
    "name": "string",
    "rus_name": "string | null",
    "scaling": "string",
    "range": "string",
    "spn": "number",
    "date": "string",
    "status_delete": "boolean"
  }
]
```

- ### `POST` - `HOST/api/parameters/create/`

**НЕОБХОДИМА АВТОРИЗАЦИЯ**

Создает новые параметры в модель BufferedParameterModel.

Принимает входные данные формата:

```json
[
  {
    "cat_id": "string",
    "data_length": "string",
    "length": "string",
    "name": "string",
    "rus_name?": "string",
    "scaling": "string",
    "range": "string",
    "spn": "number",
    "status_delete": "boolean"
  }
]
```

Возвращает данные формата:

```json
[
  {
    "id": "number",
    "cat_id": "string",
    "data_length": "string",
    "length": "string",
    "name": "string",
    "rus_name": "string | null",
    "scaling": "string",
    "range": "string",
    "spn": "number",
    "date": "string",
    "status_delete": "boolean"
  }
]
```

- ### `POST` - `HOST/api/parameters/to-delete/`

**НЕОБХОДИМА АВТОРИЗАЦИЯ**

Помечает список параметров на удаление.

**Важно!** Нельзя пометить параметр на удаление, если он уже был помечен, так же нельзя пометить параметр на удаление,
который не существует

Принимает входные данные:

```json
[
  {
    "id": "number"
  }
]
```

В случае успешного запроса возвращает данные:

```json
[
  {
    "id": "number"
  }
]
```

В случае проблем с валидацией возвращает данные:

```json
[
  {
    "id": [
      "string",
      "Сообщения об ошибках"
    ]
  }
]
```

- ### `POST` - `HOST/api/users/register/`

Регистрация нового пользователя

Принимает входные данные:

```json
  {
  "username": "string",
  "email": "string",
  "password": "string"
}
```

В случае успешного запроса возвращает данные:

```json
  {
  "id": "number",
  "username": "string",
  "email": "string",
  "password": "string"
}
```

В случае проблем с валидацией возвращает данные:

```json
  {
  "[field_name]": [
    "string",
    "Сообщения об ошибках"
  ]
}
```

- ### `GET, PUT, PATCH` - `HOST/api/users/profile/`

**НЕОБХОДИМА АВТОРИЗАЦИЯ**

#### `GET` - Получение информации о пользователе

Формат ответа:

```json
  {
  "id": "number",
  "username": "string",
  "email": "string"
}
```

#### `PUT, PATCH` - Обновление информации пользователя

Формат принимаемых данных

```json
  {
  "username": "string",
  "email": "string"
}
```

В случае проблем с валидацией возвращает данные:

```json
  {
  "[field_name]": [
    "string",
    "Сообщения об ошибках"
  ]
}
```

Формат ответа:

```json
  {
  "id": "number",
  "username": "string",
  "email": "string"
}
```

- ### `POST` - `HOST/api/users/token/`

Получение JWT токенов

Формат принимаемых данных:

```json
  {
  "username": "string",
  "password": "string"
}
```

Формат ответа в случае ошибок:

```json
{
  "detail": "string"
}
```

Успешный формат ответа:

```json
{
  "refresh": "string",
  "access": "string"
}
```

- ### `POST` - `HOST/api/users/token/refresh/`

Обновление access токена по refresh токену

Формат принимаемых данных:

```json
{
  "refresh": "string"
}
```

Формат ответа в случае ошибок:

```json
{
  "detail": "string",
  "code": "string"
}
```

Успешный формат ответа:

```json
{
  "access": "string"
}
```

- ### `POST` - `HOST/api/users/password/reset/`

Сброс пароля пользователя по email

Формат принимаемых данных

**Важно** Происходит валидация URL. Так же письмо не будет отправлено если пользователя с таким email не существует

```json
{
  "email": "string [Email на который будет отправлено письмо]",
  "next": "url string [Ссылка с которой будет совмещен токен для сброса пароля]"
}
```

Формат ответа в случае проблем с валидацией

```json
{
  "[field]": [
    "string [Сообщения об ошибках]"
  ]
}
```

Формат ответа

```json
{
  "email": "string",
  "message": "string"
}
```

- ### `POST` - `HOST/api/users/password/reset/complete/<uuid:token>/`

Завершающий этап сброса пароля по token

Формат принимаемых данных

```json
{
  "new_password": "string"
}
```

Формат ответа в случае проблем с валидацией

```json
{
  "[field]": [
    "string [Сообщения об ошибках]"
  ]
}
```

Успешный формат ответа

```json
  {
  "id": "number",
  "username": "string",
  "email": "string"
}
```

- ### `POST` - `HOST/api/users/password/change/`

**НЕОБХОДИМА АВТОРИЗАЦИЯ**

Изменение пароля авторизированного пользователя

Формат принимаемых данных

```json
{
  "old_password": "string",
  "new_password": "string"
}
```

Формат ответа в случае проблем с валидацией

```json
{
  "[field]": [
    "string [Сообщения об ошибках]"
  ]
}
```

Успешный формат ответа

```json
  {
  "id": "number",
  "username": "string",
  "email": "string"
}
```

- ### `GET` - `HOST/api/users/oauth/login/<str:backend>/`

Oauth авторизация через backend. Авторизация осуществляется на самом сервере

Доступны backend:

- google_oauth2

В случае успешной авторизации идет редирект на `HOST/api/users/oauth/complete/`

- ### `GET` - `HOST/api/users/oauth/complete/`

Генерирует URL и совершает redirect по нему





















