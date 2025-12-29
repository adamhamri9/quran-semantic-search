from pydantic import BaseModel
from typing import Optional, List

class SearchResult(BaseModel):
    surah: int
    ayah: int
    score: float
    text: Optional[str] = None
    translation: Optional[str] = None
    tafsir: Optional[str] = None

class SearchResponse(BaseModel):
    query: str
    detected_lang: str
    results: List[SearchResult]