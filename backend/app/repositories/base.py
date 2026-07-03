from collections.abc import Sequence

from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from app.db.mongodb import MongoDocument


class BaseRepository:
    collection_name: str

    def __init__(self, database: AsyncIOMotorDatabase[MongoDocument]) -> None:
        self._database = database

    @property
    def collection(self) -> AsyncIOMotorCollection[MongoDocument]:
        return self._database[self.collection_name]

    async def ensure_collection_exists(self) -> None:
        collection_names = await self._database.list_collection_names()
        if self.collection_name not in collection_names:
            await self._database.create_collection(self.collection_name)

    async def upsert_one(self, document: MongoDocument) -> None:
        document_id = document.get("_id")
        if document_id is None:
            raise ValueError("Seed documents must include an _id field")

        await self.collection.replace_one({"_id": document_id}, document, upsert=True)

    async def upsert_many(self, documents: Sequence[MongoDocument]) -> None:
        for document in documents:
            await self.upsert_one(document)

    async def find_by_id(self, document_id: str) -> MongoDocument | None:
        return await self.collection.find_one({"_id": document_id})

    async def count(self) -> int:
        return await self.collection.count_documents({})
