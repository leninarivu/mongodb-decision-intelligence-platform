from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import get_settings

MongoDocument = dict[str, object]

_client: AsyncIOMotorClient[MongoDocument] | None = None


async def connect_mongodb() -> None:
    global _client

    if _client is not None:
        return

    settings = get_settings()
    _client = AsyncIOMotorClient(settings.mongodb_uri, serverSelectionTimeoutMS=3000)
    await _client.admin.command("ping")


async def close_mongodb() -> None:
    global _client

    if _client is None:
        return

    _client.close()
    _client = None


def get_mongodb() -> AsyncIOMotorDatabase[MongoDocument]:
    if _client is None:
        raise RuntimeError("MongoDB client is not initialized")

    settings = get_settings()
    return _client[settings.mongodb_db]


async def ping_mongodb() -> bool:
    if _client is None:
        return False

    try:
        await _client.admin.command("ping")
    except Exception:
        return False

    return True
