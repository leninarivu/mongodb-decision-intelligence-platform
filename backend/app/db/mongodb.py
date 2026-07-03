import logging

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorDatabase

from app.core.config import Settings, get_settings

MongoDocument = dict[str, object]

logger = logging.getLogger(__name__)


class MongoDBConnectionManager:
    def __init__(self) -> None:
        self._client: AsyncIOMotorClient[MongoDocument] | None = None
        self._database: AsyncIOMotorDatabase[MongoDocument] | None = None
        self._settings: Settings | None = None

    async def connect(self, settings: Settings | None = None) -> None:
        if self._client is not None:
            return

        resolved_settings = settings or get_settings()
        client: AsyncIOMotorClient[MongoDocument] = AsyncIOMotorClient(
            resolved_settings.mongodb_uri,
            serverSelectionTimeoutMS=3000,
        )
        try:
            await client.admin.command("ping")
        except Exception:
            client.close()
            raise

        self._client = client
        self._database = client[resolved_settings.mongodb_database]
        self._settings = resolved_settings

        logger.info("Connected to MongoDB Atlas")
        logger.info("Database: %s", resolved_settings.mongodb_database)
        logger.info("Customer Profile: %s", resolved_settings.customer_profile)

    async def close(self) -> None:
        if self._client is None:
            return

        self._client.close()
        self._client = None
        self._database = None
        self._settings = None

    @property
    def database_name(self) -> str:
        settings = self._settings or get_settings()
        return settings.mongodb_database

    @property
    def customer_profile(self) -> str:
        settings = self._settings or get_settings()
        return settings.customer_profile

    def get_database(self) -> AsyncIOMotorDatabase[MongoDocument]:
        if self._database is None:
            raise RuntimeError("MongoDB database is not initialized")

        return self._database

    def get_collection(self, collection_name: str) -> AsyncIOMotorCollection[MongoDocument]:
        return self.get_database()[collection_name]

    async def ping(self) -> bool:
        if self._client is None:
            return False

        try:
            await self._client.admin.command("ping")
        except Exception:
            return False

        return True


mongodb_manager = MongoDBConnectionManager()


async def connect_mongodb() -> None:
    await mongodb_manager.connect()


async def close_mongodb() -> None:
    await mongodb_manager.close()


def get_mongodb() -> AsyncIOMotorDatabase[MongoDocument]:
    return mongodb_manager.get_database()


async def ping_mongodb() -> bool:
    return await mongodb_manager.ping()
