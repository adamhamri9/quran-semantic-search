import json
from pathlib import Path

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer


QURAN_PATH = Path("data/processed/quran.json")
OUTPUT_DIR = Path("data/embeddings")

MODEL_NAME = "intfloat/multilingual-e5-base"
BATCH_SIZE = 32
NORMALIZE = True

FAISS_INDEX_NAME = "quran.faiss"
EMBEDDINGS_NAME = "quran.npy"


def load_embedding_texts():
    quran = json.loads(QURAN_PATH.read_text(encoding="utf-8"))
    texts = [v["embedding_text"] for v in quran]
    return texts


def build_embeddings(texts):
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(
        texts,
        batch_size=BATCH_SIZE,
        convert_to_numpy=True,
        normalize_embeddings=NORMALIZE,
        show_progress_bar=True
    )
    return embeddings


def build_faiss_index(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)
    return index


def save_outputs(embeddings, index):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    np.save(OUTPUT_DIR / EMBEDDINGS_NAME, embeddings)
    faiss.write_index(index, str(OUTPUT_DIR / FAISS_INDEX_NAME))


def main():
    texts = load_embedding_texts()
    embeddings = build_embeddings(texts)
    index = build_faiss_index(embeddings)
    save_outputs(embeddings, index)


if __name__ == "__main__":
    main()
