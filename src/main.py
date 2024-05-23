import json

from dotenv import load_dotenv

from .db import MongoConnection
from .splitters import csharp_splitter, semantic_splitter, sql_splitter

load_dotenv()

import os

# Due to the sensitivity of company data, I are not able to share the function map.
FUNCTION_MAP = json.loads(os.getenv("FUNCTION_MAP", "{}"))
SPLITTER_MAP = {
    "csharp_splitter": csharp_splitter,
    "sql_splitter": sql_splitter,
    "semantic_splitter": semantic_splitter,
}


def main():
    cli = MongoConnection()
    docs = cli.get_documents(manual="CODEBASE")
    for doc in docs[:2]:
        chunks = SPLITTER_MAP[FUNCTION_MAP[doc["manual"]]](doc["content"])
        cli.save_documents(doc, chunks)


main()
