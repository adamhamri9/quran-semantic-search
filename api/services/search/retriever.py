import logging
import json
from pathlib import Path
from langdetect import detect, DetectorFactory
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import time
import asyncio
from typing import List

from config import Config
from api.schemas.search_input import SearchInput
from api.schemas.search_response import SearchResult

DetectorFactory.seed = 0
logger = logging.getLogger("quran_retriever")
logger.setLevel(logging.INFO)  

file_handler = logging.FileHandler("app.log", encoding="utf-8")
file_handler.setLevel(logging.INFO) 
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class QuranRetriever:
    def __init__(self):
        self.model = SentenceTransformer(Config.MODEL_NAME)
        self.verses = json.loads(Config.PROCESSED_QURAN_FILE.read_text(encoding="utf-8"))
        self.resource_cache = {"index": {}, "translation_bundle": {}, "query_emb": {}}

    def _load_index(self, lang: str):
        if hasattr(lang, "value"):
            lang = lang.value
    
        if lang in self.resource_cache["index"]:
            return self.resource_cache["index"][lang]

        idx_path = Config.TRANS_EMBEDDINGS_DIR / lang / "index.faiss"
        if not idx_path.exists():
            logger.warning(f"Index for '{lang}' not found. Falling back to default Arabic index.")
            idx_path = Config.FAISS_INDEX_PATH

        try:
            index = faiss.read_index(str(idx_path))
            self.resource_cache["index"][lang] = index
            return index
        except Exception as e:
            logger.error(f"Failed to load index for {lang}: {e}")
            return None

    def _load_translation_bundle(self, lang: str):
        if hasattr(lang, "value"):
            lang = lang.value

        if lang in self.resource_cache["translation_bundle"]:
            return self.resource_cache["translation_bundle"][lang]

        data_path = Config.PROCESSED_QURAN_FILE if lang == "ar" else Config.PROCESSED_TRANS_DIR / f"{lang}_quran.json"
        if not data_path.exists():
            logger.warning(f"Translation/Tafsir file for '{lang}' not found.")
            return None

        try:
            bundle = json.loads(data_path.read_text(encoding="utf-8"))
            self.resource_cache["translation_bundle"][lang] = bundle
            return bundle
        except Exception as e:
            logger.error(f"Failed to load translation bundle for {lang}: {e}")
            return None

    def _get_resource(self, lang: str, resource_type: str):
        if resource_type == "index":
            return self._load_index(lang)
        elif resource_type == "translation_bundle":
            return self._load_translation_bundle(lang)
        else:
            return self._load_index(lang), self._load_translation_bundle(lang)

    def _get_query_embedding(self, query: str):
        if query in self.resource_cache["query_emb"]:
            return self.resource_cache["query_emb"][query]

        emb = self.model.encode(
            [f"query: {query}"],
            batch_size=Config.BATCH_SIZE,
            normalize_embeddings=Config.NORMALIZE,
            convert_to_numpy=True,
            show_progress_bar=False
        ).astype("float32")
        self.resource_cache["query_emb"][query] = emb
        return emb

    def _get_item_from_bundle(self, bundle, verse, field):
        if bundle is None:
            return f"{field} not found"
        item = next((t for t in bundle if t.get("surah") == verse["surah"] and t.get("ayah") == verse["ayah"]), None)
        if item is None:
            return f"{field} not found"
        return item.get(field) if isinstance(item, dict) else item

    async def _search_with_index(self, params: SearchInput, index) -> List[SearchResult]:
        try:
            start_time = time.time()
            query_vector = self._get_query_embedding(params.query)

            distances, indices = index.search(query_vector, params.top_k)
            results = []

            for dist, idx in zip(distances[0], indices[0]):
                if idx == -1 or idx >= len(self.verses):
                    continue

                verse = self.verses[idx]

                # Translation
                trans_item = None
                if params.settings.include_translation:
                    trans_bundle = self._get_resource(params.settings.translation_lang, "translation_bundle")
                    trans_item = self._get_item_from_bundle(trans_bundle, verse, "translation")

                # Tafsir
                tafsir_item = None
                if params.settings.include_tafsir:
                    tafsir_bundle = self._get_resource(params.settings.tafsir_lang, "translation_bundle")
                    tafsir_item = self._get_item_from_bundle(tafsir_bundle, verse, "tafsir")

                results.append(
                    SearchResult(
                        surah=verse["surah"],
                        ayah=verse["ayah"],
                        score=round(float(dist), 2),
                        text=verse.get("text") if params.settings.include_text else None,
                        translation=trans_item,
                        tafsir=tafsir_item
                    )
                )
            elapsed = time.time() - start_time
            logger.info(f"Search for query '{params.query}' took {elapsed:.3f}s")
            return results

        except Exception as e:
            logger.error(f"Error during search for query '{params.query}': {e}")
            return [] 
