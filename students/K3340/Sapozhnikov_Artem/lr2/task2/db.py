import os

from dotenv import load_dotenv
from sqlmodel import create_engine, Session
from sqlalchemy import text


load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


def save_transaction(title, amount, comment, user_id=2, category_id=2):
    with Session(engine) as session:
        session.execute(
            text("""
                INSERT INTO "transaction"
                (title, amount, transaction_type, comment, user_id, category_id)
                VALUES (:title, :amount, :transaction_type, :comment, :user_id, :category_id)
            """),
            {
                "title": title[:255],
                "amount": amount,
                "transaction_type": "expense",
                "comment": comment,
                "user_id": user_id,
                "category_id": category_id,
            }
        )

        session.commit()