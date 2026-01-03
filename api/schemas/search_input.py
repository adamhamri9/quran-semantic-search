from pydantic import BaseModel, Field
from typing import Optional, List
from enum import Enum
from config import Config

def get_supported_languages():
    languages = {"auto": "auto", "ar": "ar"}
    
    if Config.PROCESSED_TRANS_DIR.exists():
        for file in Config.PROCESSED_TRANS_DIR.glob("*.json"):
            lang_code = file.stem.split('_')[0]
            languages[lang_code] = lang_code
            
    return Enum("SupportedLanguage", languages, type=str)

SupportedLanguage = get_supported_languages()


class SearchSettings(BaseModel):
    include_text: bool = Field(True, description="Include the original Arabic verse text")
    include_translation: bool = Field(True, description="Include the translation for the detected or specified language")
    translation_lang: SupportedLanguage = Field(SupportedLanguage.auto, description="Language code or 'auto' for automatic detection")
    include_tafsir: bool = Field(True, description="Include the Arabic tafsir (Al-Mukhtasar)")
    tafsir_lang: SupportedLanguage = Field(SupportedLanguage.auto, description="Language code or 'auto' for automatic detection")

class ExpansionSettings(BaseModel):
    force_query_expansion: bool = Field(False, description="Enable query expansion using synonyms/local embeddings")
    force_llm_query_expansion: bool = Field(False, description="Enable query expansion using an LLM")

class ContextSettings(BaseModel):
    enable_context_links: bool = Field(True, description="Enable retrieval of semantically similar verses as context")
    context_window: int = Field(10, ge=1, le=50, description="Window size around the target verse for context search")
    similarity_threshold: float = Field(0.7, ge=0.0, le=1.0, description="Minimum similarity score to consider a verse as context")
    max_context_links: int = Field(5, ge=1, le=20, description="Maximum number of context links to return")

class SearchInput(BaseModel):
    query: str = Field(..., min_length=2, description="Search query string")
    top_k: int = Field(5, ge=1, le=50, description="Number of results to return")
    settings: Optional[SearchSettings] = Field(default_factory=SearchSettings)
    expansion: Optional[ExpansionSettings] = Field(default_factory=ExpansionSettings)
    context: Optional[ContextSettings] = Field(default_factory=ContextSettings)