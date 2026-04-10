import os
from urllib.parse import quote_plus

from dotenv import load_dotenv
from sqlmodel import Session, create_engine

load_dotenv()

for key in [
    "PGPASSWORD", "PGSERVICE", "PGSERVICEFILE", "PGHOST", "PGHOSTADDR",
    "PGUSER", "PGDATABASE", "PGOPTIONS", "PGAPPNAME", "PGPASSFILE",
    "PGSSLMODE", "PGCLIENTENCODING"
]:
    os.environ.pop(key, None)

db_user = os.getenv("DB_USER", "postgres").strip()
db_password_raw = os.getenv("DB_PASSWORD", "").strip()
db_host = os.getenv("DB_HOST", "localhost").strip()
db_name = os.getenv("DB_NAME", "").strip()

print("DB_USER =", repr(db_user))
print("DB_PASSWORD =", repr(db_password_raw))
print("DB_HOST =", repr(db_host))
print("DB_NAME =", repr(db_name))

db_password = quote_plus(db_password_raw)
db_url = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}/{db_name}"

print("DB URL repr:", repr(db_url))

engine = create_engine(db_url, echo=True)


def get_session():
    with Session(engine) as session:
        yield session