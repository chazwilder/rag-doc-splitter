from typing import List

from langchain_core.documents import Document
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter
from semantic_text_splitter import TextSplitter

def csharp_splitter(document: str) -> List[Document]: ...


def semantic_splitter(document: str) -> List[Document]: ...
