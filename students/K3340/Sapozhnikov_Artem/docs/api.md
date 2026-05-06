# API приложения

Все основные методы, кроме регистрации и входа, требуют авторизации через Bearer Token.

---

## Auth

| Метод | Endpoint | Назначение |
|---|---|---|
| POST | `/auth/register` | Регистрация пользователя |
| POST | `/auth/login` | Авторизация и получение JWT |
| GET | `/auth/me` | Получение текущего пользователя |
| POST | `/auth/change-password` | Смена пароля |

---

## Users

| Метод | Endpoint | Назначение |
|---|---|---|
| GET | `/users/` | Получение списка пользователей |
| GET | `/users/{user_id}` | Получение пользователя по id |

---

## Categories

| Метод | Endpoint | Назначение |
|---|---|---|
| GET | `/categories/` | Получение списка категорий |
| GET | `/categories/{category_id}` | Получение категории |
| POST | `/categories/` | Создание категории |
| PATCH | `/categories/{category_id}` | Обновление категории |
| DELETE | `/categories/{category_id}` | Удаление категории |

---

## Tags

| Метод | Endpoint | Назначение |
|---|---|---|
| GET | `/tags/` | Получение списка тегов |
| GET | `/tags/{tag_id}` | Получение тега |
| POST | `/tags/` | Создание тега |
| PATCH | `/tags/{tag_id}` | Обновление тега |
| DELETE | `/tags/{tag_id}` | Удаление тега |

---

## Transactions

| Метод | Endpoint | Назначение |
|---|---|---|
| GET | `/transactions/` | Получение списка транзакций текущего пользователя |
| GET | `/transactions/{transaction_id}` | Получение транзакции с вложенными объектами |
| POST | `/transactions/` | Создание транзакции |
| PATCH | `/transactions/{transaction_id}` | Обновление транзакции |
| DELETE | `/transactions/{transaction_id}` | Удаление транзакции |

Пример создания транзакции:

```json
{
  "title": "Покупка продуктов",
  "amount": 3500,
  "transaction_type": "expense",
  "comment": "Супермаркет",
  "category_id": 1
}
```

---

## Transaction Tag Links

| Метод | Endpoint | Назначение |
|---|---|---|
| GET | `/transaction-tag-links/` | Получение связей транзакций и тегов |
| POST | `/transaction-tag-links/` | Привязка тега к транзакции |

Пример тела запроса:

```json
{
  "transaction_id": 1,
  "tag_id": 1,
  "note": "регулярная трата",
  "priority": 1
}
```

---

## Budgets

| Метод | Endpoint | Назначение |
|---|---|---|
| GET | `/budgets/` | Получение бюджетов пользователя |
| GET | `/budgets/{budget_id}` | Получение бюджета |
| POST | `/budgets/` | Создание бюджета |
| PATCH | `/budgets/{budget_id}` | Обновление бюджета |
| DELETE | `/budgets/{budget_id}` | Удаление бюджета |
| GET | `/budgets/{budget_id}/status` | Проверка статуса бюджета |

Пример создания бюджета:

```json
{
  "title": "Бюджет на еду",
  "limit_amount": 15000,
  "spent_amount": 3500,
  "category_id": 1
}
```

---

## Goals

| Метод | Endpoint | Назначение |
|---|---|---|
| GET | `/goals/` | Получение финансовых целей |
| GET | `/goals/{goal_id}` | Получение цели |
| POST | `/goals/` | Создание цели |
| PATCH | `/goals/{goal_id}` | Обновление цели |
| DELETE | `/goals/{goal_id}` | Удаление цели |

Пример создания цели:

```json
{
  "title": "Накопить на ноутбук",
  "target_amount": 150000,
  "current_amount": 30000,
  "deadline": "2026-12-31"
}
```