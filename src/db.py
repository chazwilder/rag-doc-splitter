from typing import List

from bson.raw_bson import RawBSONDocument
from dotenv import load_dotenv
from pymongo import MongoClient

from loggy import logger

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
        """
        Initializes a new instance of the MongoConnection class.

        Parameters:
        database (str): The name of the MongoDB database to connect to. Defaults to the value of MONGO_DATABASE environment variable.
        collection (str): The name of the MongoDB collection to use. Defaults to the value of MONGO_COLLECTION environment variable.
        corpus (str): The name of the MongoDB corpus collection to use. Defaults to the value of MONGO_CORPUS environment variable.
        """
        self.client: MongoClient = MongoClient(MONGO_URI)
        self.db = self.client[database]
        self.collection = self.db[collection]
        self.corpus = self.db[corpus]
        logger.debug(f"Connected to MongoDB database: {database}")

    def get_documents(self, **kwargs) -> List[RawBSONDocument]:
        """
        Retrieves documents from the MongoDB collection that have not been split.

        Returns:
        List[RawBSONDocument]: A list of RawBSONDocument objects where the 'splitted' field is set to False.
        """
        if kwargs:
            query = {
                "manual": kwargs.get("manual", None),
                "splitted": False,
                "manual": {"$exists": True},
            }
        else:
            query = {
                "splitted": False,
                "manual": {"$exists": True},
            }
        return list(self.collection.find(query).sort("file_name", 1))

    def update_document(self, document):
        """
        Updates a document in the MongoDB collection.

        This method sets the 'splitted' field of the specified document to True.

        Parameters:
        document (dict): The document to update. It must contain the '_id' field to identify the document in the collection.

        Returns:
        None
        """
        self.collection.update_one(
            {"_id": document["_id"]}, {"$set": {"splitted": True}}
        )
        logger.debug(f"Updated document: {document['_id']}")

    def save_documents(self, document: RawBSONDocument, chunks: List[RawBSONDocument]):
        """
        Saves a document to the MongoDB corpus collection.

        This method inserts the specified document into the corpus collection.

        Parameters:
        document (RawBSONDocument): The document to be saved into the corpus collection.

        Returns:
        None
        """
        self.corpus.insert_many(chunks)
        logger.debug(
            f"Inserted {len(chunks)} documents into the corpus collection for file {document['file_name']}."
        )
        self.update_document(document)
