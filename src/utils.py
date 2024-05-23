from typing import Dict, List

from bson.raw_bson import RawBSONDocument
from langchain_core.documents import Document
from loggy import logger


def splitter_idx(
    document: RawBSONDocument, chunks: List[str | Document]
) -> List[Dict[str, str]]:
    idx = 0
    base_id = str(document["_id"])
    file_name = document["file_name"]
    child_documents = []

    for chunk in chunks:
        logger.debug(f"file: {file_name}, index: {idx}, chunk: {chunk}")
        if isinstance(chunk, Document):
            child_documents.append(
                {
                    "idx_id": f"{file_name}::{idx}",
                    "parent_id": base_id,
                    "content": chunk.page_content,
                }
            )
        else:
            child_documents.append(
                {
                    "idx_id": f"{file_name}::{idx}",
                    "parent_id": base_id,
                    "content": chunk,
                }
            )
        idx += 1
    return child_documents
