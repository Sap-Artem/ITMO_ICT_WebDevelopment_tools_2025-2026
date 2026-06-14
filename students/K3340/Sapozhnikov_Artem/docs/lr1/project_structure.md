# Структура проекта

Проект имеет модульную структуру. Код разделен по слоям: ядро приложения, база данных, роутеры и схемы.

```text
app/
├── core/
│   ├── auth.py
│   ├── config.py
│   └── security.py
│
├── db/
│   ├── connection.py
│   └── models.py
│
├── routers/
│   ├── auth.py
│   ├── budgets.py
│   ├── categories.py
│   ├── goals.py
│   ├── reports.py
│   ├── tags.py
│   ├── transaction_tag_links.py
│   ├── transactions.py
│   └── users.py
│
├── schemas/
│   ├── budget.py
│   ├── category.py
│   ├── goal.py
│   ├── tag.py
│   ├── transaction.py
│   ├── transaction_tag_link.py
│   └── user.py
│
└── main.py
```

## Назначение папок

### `core`

Содержит код, связанный с безопасностью и авторизацией:

- создание JWT-токенов;
- декодирование JWT;
- хэширование паролей;
- получение текущего пользователя.

### `db`

Содержит подключение к базе данных и ORM-модели SQLModel.

### `routers`

Содержит API-маршруты приложения, разделенные по предметным областям.

### `schemas`

Содержит модели запросов и ответов API. Они отделены от ORM-моделей, чтобы не возвращать лишние поля, например `password_hash`.

### `main.py`

Главный файл приложения. В нем создается объект FastAPI и подключаются роутеры.