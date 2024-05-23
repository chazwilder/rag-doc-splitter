from typing import Dict, List

from bson.raw_bson import RawBSONDocument


def splitter_idx(
    document: RawBSONDocument, chunks: List[str]
) -> List[Dict[str, str]]: ...
