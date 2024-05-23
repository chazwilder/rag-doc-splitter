import json

from dotenv import load_dotenv

from db import MongoConnection
from splitters import csharp_splitter, semantic_splitter, sql_splitter
from utils import splitter_idx

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
    docs = cli.get_documents()
    for doc in docs:
        splitter_chunks = SPLITTER_MAP[FUNCTION_MAP[doc["manual"]]](
            f'{doc["content"]} \n\n\n\nSUMMARY: {doc.get("summary", "")}'
        )
        formatted_chunks = splitter_idx(doc, splitter_chunks)
        cli.save_documents(doc, formatted_chunks)


if __name__ == "__main__":
    main()
