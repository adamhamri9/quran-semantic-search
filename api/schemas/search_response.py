from pydantic import BaseModel
from typing import Optional, List

class ContextLink(BaseModel):
    surah: Optional[int] = None
    ayah: Optional[int] = None
    similarity: Optional[float] = None
    note: str = "For reference only; may contain mistakes"
    error: Optional[str] = None

class SearchResult(BaseModel):
    surah: int
    ayah: int
    score: float
    text: Optional[str] = None
    translation: Optional[str] = None
    tafsir: Optional[str] = None
    context_links: Optional[List[ContextLink]] = None

class SearchResponse(BaseModel):
    query: str
    detected_lang: str
    results: List[SearchResult]
