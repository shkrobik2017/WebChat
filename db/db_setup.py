from db.db_singleton import PostgresDB
from settings import settings


DB = PostgresDB(
    dsn=f"postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
        f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
)

