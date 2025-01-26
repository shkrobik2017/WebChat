from threading import Lock
from tortoise import Tortoise
from typing import Optional


class PostgresDB:
    _instance: Optional['PostgresDB'] = None
    _lock: Lock = Lock()

    def __new__(cls, *args, **kwargs) -> 'PostgresDB':
        """
        Ensure that only one instance of PostgresDB is created (Singleton pattern).
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, dsn: str) -> None:
        """
        Initialize the database connection.

        Args:
            dsn (str): The database connection string.
        """
        if not hasattr(self, "_dsn"):
            self._dsn = dsn

    async def init_orm(self) -> None:
        """
        Initialize the ORM and generate database schemas.
        """
        await Tortoise.init(
            db_url=self._dsn,
            modules={"models": ["db.db_models"]},
        )
        await Tortoise.generate_schemas()

    async def close_orm(self) -> None:
        """
        Close all database connections.
        """
        await Tortoise.close_connections()


