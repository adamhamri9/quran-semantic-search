# Quran Semantic Search API

🚧 Status: Work in Progress (Learning Project / Functional MVP)

---

## Overview
Quran Semantic Search API implements **meaning-based semantic retrieval** over Qur'anic text using vector embeddings.  
The system is designed to handle **multilingual queries** while prioritizing **accuracy and context preservation** at the ayah level.

Key design principles:

- **Arabic-first retrieval** for all queries to maximize semantic fidelity.
- **Controlled fallback** to target language indices only when confidence scores are low.
- Explicit separation of indexing, retrieval, and ranking stages to simplify experimentation and maintain modularity.
- System favors **correctness and reproducibility** over recall or flashy optimizations.

---

## Goals
- Understand and implement multilingual semantic embeddings for NLP.
- Explore semantic search with FAISS and assess retrieval quality across languages.
- Design a modular and scalable retrieval pipeline.
- Serve clean, consistent API responses via FastAPI.

---

## Core Features
- Ayah-level semantic search across Qur'anic text.
- **Arabic-first retrieval with multilingual fallback**:
  - For English and French queries, Arabic index is used first due to better semantic quality.
  - If final similarity score < 0.5, fallback to language-specific index.
  - Other languages use their own index if available; otherwise fallback to Arabic index.
- Separate FAISS indices per language.
- Async search pipeline for scalable request handling.
- **Interactive API Documentation** via Scalar.
- **Context Links**: Semantic linking of related verses within a local window (±10 ayahs) to provide "contextual continuity" beyond simple keyword matching.
- Optional inclusion of ayah text, translation, and tafsir.
- **Resource caching**:
  - FAISS indices, embeddings, and translations.
  - AI model used for embeddings is also cached for faster reuse.
  - Original Qur'an verses are cached to reduce repeated I/O.

---

## Tech Stack
- **Python** – orchestration, pipeline logic.
- **FAISS** – similarity search with configurable index types.
- **Sentence Transformers** – multilingual embedding generation.
- **FastAPI** – async API layer with explicit request/response contracts.

---

## Supported Languages
- Arabic (primary)
- English
- French
- Indonesian
- Turkish
- Urdu  
Additional languages can be embedded and indexed independently.

---

## Project Structure

A detailed breakdown of the project's directory layout:

```text
.
├── api/                            # Application Interface & Logic
│   ├── main.py                     # FastAPI entry point & route definitions
│   ├── schemas/                    # Pydantic models for request/response validation
│   └── services/                   # Core business logic
│       └── search/
│           ├── retriever.py        # Handles FAISS index loading & vector search
│           ├── context.py          # Builds semantic context links between ayahs
│           └── service.py          # Orchestrates search & context building
├── data/                           # Data Storage (Git-ignored large files)
│   ├── raw/                        # Original source files (Tanzil Quran, translations)
│   ├── processed/                  # Normalized JSON data ready for embedding
│   └── embeddings/                 # Generated FAISS indices & pickle files
├── scripts/                        # ETL Data Pipeline Scripts
│   ├── prepare_quran.py            # Cleans & structures raw Quran text
│   ├── prepare_translations.py     # Aligns translations with Arabic text
│   ├── embed_quran.py              # Generates vector embeddings for Arabic
│   └── embed_translations.py       # Generates embeddings for other languages
├── config.py                       # Centralized configuration (Paths, Constants)
├── setup.py                        # Automated setup script (Runs full pipeline)
└── requirements.txt                # Python dependencies
```

---

## Data Sources
- Qur'an text: [Tanzil Project](https://tanzil.net/docs/download/)
- Translations & Tafsir: [Tarteel QUL Project](https://tarteel.io)

---

## Design Decisions
1. **Arabic-first retrieval for English/French queries**  
   - Observed lower semantic quality when directly using non-Arabic indices.  
   - Fallback mechanism ensures retrieval accuracy without discarding other languages.  

2. **Fallback strategy for missing language indices**  
   - Queries in unsupported languages default to Arabic index using a dictionary mapping.  
   - Ensures functional retrieval without building every language index upfront.

3. **Deferred query expansion**  
    - Postponed to preserve retrieval quality and because of limited personal time.
    - See [Issue #2](https://github.com/adamhamri9/quran-semantic-search/issues/2).

4. **Context Links**  
   - Dynamically links semantically related verses within a surrounding window.
   - Solves the issue of isolated results by suggesting relevant neighboring ayahs.
   - See [Issue #1](https://github.com/adamhamri9/quran-semantic-search/issues/1).

---

## Running the Project

1. **Clone the repository**
```bash
git clone https://github.com/adamhamri9/quran-semantic-search
cd quran-semantic-search
````

2. **Run the setup script**

```bash
python setup.py
```

* Creates virtual environment.
* Installs all dependencies.
* Prepares Qur'an and translation data.
* Generates embeddings and FAISS indices.
* Prompts for target language codes to avoid unnecessary resource usage.

⚠️ Note: Embedding generation may take time depending on hardware.

3. **Start the API**

```bash
uvicorn api.main:app
```

* **API Endpoint**: [http://127.0.0.1:8000/search](http://127.0.0.1:8000/search)
* **Interactive Docs**: [http://127.0.0.1:8000/scalar](http://127.0.0.1:8000/scalar)

---

## Disclaimer

⚠️ This project is for **educational and experimental purposes**.
Architecture is carefully designed, but the API is **not production-ready**.
