from pathlib import Path
from dataclasses import dataclass

@dataclass(frozen=True)
class Config:
    # Root Directory (Base Path)
    BASE_DIR = Path(__file__).resolve().parent

    # --- Models & Settings ---
    MODEL_NAME = "intfloat/multilingual-e5-base"
    BATCH_SIZE = 32
    NORMALIZE = True

    # --- Raw Data Paths ---
    RAW_QURAN_PATH = BASE_DIR / "data/raw/quran-tanzil.txt"
    RAW_TAFSIR_DIR = BASE_DIR / "data/raw/tafsir"
    RAW_TRANSLATIONS_DIR = BASE_DIR / "data/raw/translations"

    # --- Processed Data Paths ---
    PROCESSED_QURAN_FILE = BASE_DIR / "data/processed/quran.json"
    PROCESSED_TRANS_DIR = BASE_DIR / "data/processed/translations"

    # --- Output & Embeddings ---
    EMBEDDINGS_DIR = BASE_DIR / "data/embeddings"
    TRANS_EMBEDDINGS_DIR = EMBEDDINGS_DIR / "translations"
    
    FAISS_INDEX_PATH = EMBEDDINGS_DIR / "quran.faiss"
    EMBEDDINGS_FILE_PATH = EMBEDDINGS_DIR / "quran.npy"
    
    # --- Helper to get translation index path by language code ---
    @staticmethod
    def get_translation_index_path(lang_code: str):
        return Config.TRANS_EMBEDDINGS_DIR / lang_code / "index.faiss"
