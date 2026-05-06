# Отчеты

## Финансовая сводка

Endpoint:

```text
GET /reports/summary
```

Метод возвращает финансовую статистику текущего пользователя.

---

## Логика расчета

В отчете рассчитываются:

- сумма доходов;
- сумма расходов;
- итоговый баланс;
- количество транзакций;
- количество бюджетов;
- список превышенных бюджетов.

```python
total_income = sum(
    transaction.amount
    for transaction in transactions
    if transaction.transaction_type == TransactionType.income
)

total_expense = sum(
    transaction.amount
    for transaction in transactions
    if transaction.transaction_type == TransactionType.expense
)
```

---

## Пример ответа

```json
{
  "user_id": 1,
  "total_income": 120000,
  "total_expense": 3500,
  "balance": 116500,
  "transactions_count": 2,
  "budgets_count": 1,
  "exceeded_budgets": []
}
```

---

## Проверка превышения бюджета

Если `spent_amount` больше `limit_amount`, бюджет попадает в список `exceeded_budgets`.

```python
if budget.spent_amount > budget.limit_amount
```