import json
from pathlib import Path

import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

PROCESSED_TRANS_DIR = Path("data/processed/translations")
OUTPUT_DIR = Path("data/embeddings/translations")

MODEL_NAME = "intfloat/multilingual-e5-base"
BATCH_SIZE = 32
NORMALIZE = True


def load_embedding_texts(trans_file):
    data = json.loads(trans_file.read_text(encoding="utf-8"))
    texts = [f"passage: {v['embedding_text']}" for v in data]
    return texts


def build_embeddings(texts, model):
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


def save_outputs(lang_code, embeddings, index):
    lang_output_dir = OUTPUT_DIR / lang_code
    lang_output_dir.mkdir(parents=True, exist_ok=True)
    
    np.save(lang_output_dir / "embeddings.npy", embeddings)
    faiss.write_index(index, str(lang_output_dir / "index.faiss"))


def process_file(trans_file, model):
    lang_code = trans_file.name.split('_')[0]
    
    texts = load_embedding_texts(trans_file)
    embeddings = build_embeddings(texts, model)
    index = build_faiss_index(embeddings)
    save_outputs(lang_code, embeddings, index)


def main():
    if not PROCESSED_TRANS_DIR.exists():
        return

    model = SentenceTransformer(MODEL_NAME)
    
    for trans_file in PROCESSED_TRANS_DIR.glob("*.json"):
        process_file(trans_file, model)


if __name__ == "__main__":
    main()