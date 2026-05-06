# Практика 1.1

## Цель работы

Изучение основ FastAPI и реализация простого REST API.

---

## Реализованные модели

### Transaction
- id
- title
- amount
- transaction_type
- category
- user
- tags

### Category
- id
- name
- description
- transaction_type

---

## Реализованные методы API

### Transactions
- GET /transactions_list
- GET /transaction/{id}
- POST /transaction
- PUT /transaction/{id}
- DELETE /transaction/{id}

### Categories
- GET /categories_list
- GET /category/{id}
- POST /category
- PUT /category/{id}
- DELETE /category/{id}

---

## Пример JSON объекта

```json
{
  "id": 1,
  "title": "Salary",
  "amount": 120000
}
