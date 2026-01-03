import logging
import json
from typing import List, Optional
import faiss
import numpy as np

from api.schemas.search_response import ContextLink

logger = logging.getLogger("quran_context_builder")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("app.log", encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class QuranContextBuilder:
    def __init__(self, verses):
        try:
            self.verses = verses
            logger.info(f"Loaded {len(self.verses)} verses successfully.")
        except Exception as e:
            logger.error(f"Failed to load Quran file: {e}")
            self.verses = []

    def _find_global_index(self, surah: int, ayah: int) -> Optional[int]:
        try:
            for i, v in enumerate(self.verses):
                if v.get("surah") == surah and v.get("ayah") == ayah:
                    return i
            return None
        except Exception as e:
            logger.error(f"Error finding global index for {surah}:{ayah} - {e}")
            return None

    def build_context(
        self,
        surah: int,
        ayah: int,
        index: faiss.Index,
        window: int = 10,
        similarity_threshold: float = 0.7,
        max_links: int = 5
    ) -> List[ContextLink]:

        try:
            target_idx = self._find_global_index(surah, ayah)
            if target_idx is None:
                msg = f"Verse {surah}:{ayah} not found."
                logger.warning(msg)
                return [ContextLink(error=msg)]

            target_emb = np.array([index.reconstruct(target_idx)]).astype("float32")

            candidate_indices = [
                i for i, v in enumerate(self.verses)
                if v.get("surah") == surah
                and abs(v.get("ayah", 0) - ayah) <= window
                and i != target_idx
            ]

            if not candidate_indices:
                msg = f"No candidate verses found near {surah}:{ayah} within window {window}."
                logger.info(msg)
                return [ContextLink(error=msg)]

            try:
                candidate_embs = np.array([index.reconstruct(i) for i in candidate_indices]).astype("float32")
            except Exception as e:
                msg = f"Failed to reconstruct candidate embeddings: {e}"
                logger.error(msg)
                return [ContextLink(error=msg)]

            temp_index = faiss.IndexFlatIP(candidate_embs.shape[1])
            temp_index.add(candidate_embs)

            distances, indices = temp_index.search(target_emb, len(candidate_indices))

            linked = []
            for dist, idx in zip(distances[0], indices[0]):
                if dist < similarity_threshold:
                    continue
                cand_idx = candidate_indices[idx]
                linked.append({
                    "surah": self.verses[cand_idx].get("surah"),
                    "ayah": self.verses[cand_idx].get("ayah"),
                    "similarity": round(float(dist), 3),
                })

            linked.sort(key=lambda x: x["similarity"], reverse=True)

            if not linked:
                msg = f"No verses passed similarity threshold {similarity_threshold} for {surah}:{ayah}."
                logger.info(msg)
                return [ContextLink(error=msg)]

            return [ContextLink(**link) for link in linked[:max_links]]

        except Exception as e:
            msg = f"Unexpected error building context for {surah}:{ayah}"
            logger.error(f"{msg} - {e}")
            return [ContextLink(error=msg)]