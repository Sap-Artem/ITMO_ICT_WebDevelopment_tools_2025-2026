from logging.config import fileConfig
import os
import sys
from urllib.parse import quote_plus

from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv
from sqlmodel import SQLModel

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.db.models import *

load_dotenv(override=True)

config = context.config

db_user = os.getenv("DB_USER", "postgres").strip()
db_password_raw = os.getenv("DB_PASSWORD", "").strip()
db_host = os.getenv("DB_HOST", "127.0.0.1").strip()
db_name = os.getenv("DB_NAME", "").strip()

db_password = quote_plus(db_password_raw)
db_url = f"postgresql+psycopg://{db_user}:{db_password}@{db_host}:5432/{db_name}"

config.set_main_option("sqlalchemy.url", db_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()