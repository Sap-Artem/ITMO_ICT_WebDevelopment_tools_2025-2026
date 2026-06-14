# База данных и модели

## Подключение к базе данных

Подключение к PostgreSQL реализовано в файле `app/db/connection.py`.

```python
engine = create_engine(db_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
```

Данные для подключения берутся из `.env`-файла:

```env
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_NAME=personal_finance_db
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

---

## Основные таблицы

В проекте реализованы следующие таблицы:

- `user`
- `category`
- `tag`
- `transaction`
- `transactiontaglink`
- `budget`
- `financialgoal`

---

## Пользователь

```python
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str

    transactions: List["Transaction"] = Relationship(back_populates="user")
    budgets: List["Budget"] = Relationship(back_populates="user")
    goals: List["FinancialGoal"] = Relationship(back_populates="user")
```

Модель пользователя хранит логин, email и хэш пароля.  
Также пользователь связан с транзакциями, бюджетами и финансовыми целями.

---

## Категория

```python
class Category(CategoryBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    transactions: List["Transaction"] = Relationship(back_populates="category")
    budgets: List["Budget"] = Relationship(back_populates="category")
```

Категория используется для группировки транзакций и бюджетов.

---

## Транзакция

```python
class Transaction(TransactionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user: Optional[User] = Relationship(back_populates="transactions")
    category: Optional[Category] = Relationship(back_populates="transactions")
    tags: List[Tag] = Relationship(
        back_populates="transactions",
        link_model=TransactionTagLink
    )
```

Транзакция связана с пользователем, категорией и тегами.

---

## Many-to-many связь транзакций и тегов

```python
class TransactionTagLink(SQLModel, table=True):
    transaction_id: Optional[int] = Field(default=None, foreign_key="transaction.id", primary_key=True)
    tag_id: Optional[int] = Field(default=None, foreign_key="tag.id", primary_key=True)
    note: Optional[str] = None
    priority: Optional[int] = None
```

Для связи many-to-many между транзакциями и тегами используется ассоциативная таблица `TransactionTagLink`.

Дополнительно в ней хранятся поля:

- `note`;
- `priority`.

---

## Бюджет

```python
class Budget(BudgetBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user: Optional[User] = Relationship(back_populates="budgets")
    category: Optional[Category] = Relationship(back_populates="budgets")
```

Бюджет связан с пользователем и категорией.

---

## Финансовая цель

```python
class FinancialGoal(FinancialGoalBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    user: Optional[User] = Relationship(back_populates="goals")
```

Финансовая цель принадлежит конкретному пользователю.