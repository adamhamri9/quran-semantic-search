import json
import sys
from config import Config
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

PROCESSED_TRANS_DIR = Config.PROCESSED_TRANS_DIR
OUTPUT_DIR = Config.TRANS_EMBEDDINGS_DIR

def load_embedding_texts(trans_file):
    data = json.loads(trans_file.read_text(encoding="utf-8"))
    texts = [f"passage: {v['embedding_text']}" for v in data]
    return texts


def build_embeddings(texts, model):
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


def main(target_langs=None):
    if not PROCESSED_TRANS_DIR.exists():
        return

    model = SentenceTransformer(Config.MODEL_NAME)
    
    for trans_file in PROCESSED_TRANS_DIR.glob("*.json"):
        lang_code = trans_file.name.split('_')[0]
        
        if target_langs and lang_code not in target_langs:
            continue
        process_file(trans_file, model)


if __name__ == "__main__":
    args = sys.argv[1:]
    main(target_langs=args if args else None)