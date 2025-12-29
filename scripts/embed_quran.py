import json
from logging import config
from config import Config
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

QURAN_PATH = Config.PROCESSED_QURAN_FILE
OUTPUT_DIR = Config.EMBEDDINGS_DIR

def load_embedding_texts():
    quran = json.loads(QURAN_PATH.read_text(encoding="utf-8"))
    texts = [v["embedding_text"] for v in quran]
    return texts


def build_embeddings(texts):
    model = SentenceTransformer(Config.MODEL_NAME)
    embeddings = model.encode(
        texts,
        batch_size=Config.BATCH_SIZE,
        convert_to_numpy=True,
        normalize_embeddings=Config.NORMALIZE,
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
    np.save(Config.EMBEDDINGS_FILE_PATH, embeddings)
    faiss.write_index(index, str(Config.FAISS_INDEX_PATH))


def main():
    texts = load_embedding_texts()
    embeddings = build_embeddings(texts)
    index = build_faiss_index(embeddings)
    save_outputs(embeddings, index)


if __name__ == "__main__":
    main()
