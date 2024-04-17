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






