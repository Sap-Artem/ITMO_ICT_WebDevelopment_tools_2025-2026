# Авторизация и JWT

## Общая логика

В проекте реализована регистрация, авторизация и аутентификация пользователя по JWT-токену.

Для защиты API используется схема Bearer Token.

---

## Регистрация пользователя

Endpoint:

```text
POST /auth/register
```

Пример тела запроса:

```json
{
  "username": "artem",
  "email": "artem@mail.com",
  "password": "123456"
}
```

При регистрации пароль не сохраняется в открытом виде.  
Перед сохранением он хэшируется:

```python
password_hash=hash_password(user_data.password)
```

---

## Хэширование паролей

Хэширование реализовано через `passlib`.

```python
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)
```

---

## Авторизация пользователя

Endpoint:

```text
POST /auth/login
```

Для входа используется `OAuth2PasswordRequestForm`.

Пользователь отправляет:

```text
username
password
```

В случае успешной авторизации сервер возвращает JWT-токен:

```json
{
  "access_token": "...",
  "token_type": "bearer"
}
```

---

## Создание JWT-токена

```python
def create_access_token(subject: Any, expires_delta: Optional[timedelta] = None) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": str(subject),
        "exp": expire,
    }
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

В токен записывается:

- `sub` — id пользователя;
- `exp` — время истечения токена.

---

## Получение текущего пользователя

```python
def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
```

Функция:

1. получает JWT-токен;
2. декодирует его;
3. извлекает id пользователя;
4. ищет пользователя в базе данных;
5. возвращает текущего пользователя.

---

## Получение информации о себе

Endpoint:

```text
GET /auth/me
```

Запрос доступен только авторизованному пользователю.

---

## Смена пароля

Endpoint:

```text
POST /auth/change-password
```

Пример тела запроса:

```json
{
  "old_password": "123456",
  "new_password": "654321"
}
```

Перед сменой пароля проверяется старый пароль.