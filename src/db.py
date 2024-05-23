from typing import List

from bson.raw_bson import RawBSONDocument
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

import os

MONGO_URI: str | None = os.getenv("MONGO_URI")
MONGO_DATABASE: str | None = os.getenv("MONGO_DATABASE")
MONGO_COLLECTION: str | None = os.getenv("MONGO_COLLECTION")
MONGO_CORPUS: str | None = os.getenv("CORPUS_COLLECTION")


class MongoConnection:
    documents: List

    def __init__(
        self,
        database: str = MONGO_DATABASE,
        collection: str = MONGO_COLLECTION,
        corpus: str = MONGO_CORPUS,
    ):
        self.client: MongoClient = MongoClient(MONGO_URI)
        self.db = self.client[database]
        self.collection = self.db[collection]
        self.corpus = self.db[corpus]

    def get_documents(self) -> List[RawBSONDocument]:
        return list(self.collection.find({"splitted": False}))

    def update_document(self, document):
        self.collection.update_one({"_id": document["_id"]}, {"splitted": True})

    def save_documents(self, document: RawBSONDocument):
        self.corpus.insert_one(document)
