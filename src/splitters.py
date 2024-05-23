from typing import List

import sqlparse
from langchain_core.documents import Document
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from semantic_text_splitter import TextSplitter


def csharp_splitter(document: str) -> List[Document]:
    """
    Splits a C# document into smaller chunks using a recursive character-based text splitter.

    Args:
        document (str): The C# document to be split.

    Returns:
        List[Document]: A list of Document objects, each representing a chunk of the original document.
    """
    c_splitter = RecursiveCharacterTextSplitter.from_language(
        language=Language.CSHARP, chunk_size=1024, chunk_overlap=0
    )
    return c_splitter.create_documents([document])


def semantic_splitter(document: str) -> List[str]:
    """
    Splits a document into smaller chunks using a semantic text splitter based on a specific model.

    Args:
        document (str): The document to be split.

    Returns:
        List[str]: A list of strings, each representing a chunk of the original document.
    """
    splitter = TextSplitter.from_tiktoken_model("gpt-3.5-turbo", 512)
    return splitter.chunks(document)


def sql_splitter(document: str) -> List[str]:
    """
    Splits an SQL document into individual SQL statements.

    This function uses the `sqlparse` library to split a given SQL document into
    a list of individual SQL statements. This can be useful for processing or
    analyzing each statement separately.

    Args:
        document (str): The SQL document to be split.

    Returns:
        List[str]: A list of strings, each representing an individual SQL statement
        from the original document.
    """
    return sqlparse.split(document)
