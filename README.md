# Quran Semantic Search API  
**Educational & Engineering-Focused Project**

🚧 **Status:** Work in Progress (Learning Project / Functional MVP)

---

## Overview

This project explores how **semantic search** can be applied to the Qur'an by retrieving verses based on **meaning rather than keywords**.

It combines:
- Original Qur'anic text
- Translations
- Tafsir
- Multilingual embeddings
- FAISS-based similarity search

The API is designed primarily for **learning and experimentation**, while maintaining clean architecture and sound engineering practices.

---

## Goals

- Understand how semantic embeddings work in NLP
- Experiment with multilingual semantic search
- Design a scalable retrieval pipeline using FAISS
- Serve semantic search results through a clean FastAPI interface

---

## Core Features

- Semantic search over Qur'anic verses
- Arabic-first retrieval with multilingual fallback
- Separate FAISS indices per language
- Optional inclusion of:
  - Ayah text
  - Translation
  - Tafsir
- Async search pipeline
- Resource caching (indices, embeddings, translations)

---

## Supported Languages

- Arabic (primary)
- English
- French  
- Indonesian
- Turkish
- Urdu
- Additional languages can be embedded and indexed independently

---

## Tech Stack

- **Python**
- **FAISS** – vector similarity search
- **Sentence Transformers** – multilingual embeddings
- **FastAPI** – API layer

---

## Data Sources

- **Qur'an text:** Tanzil Project  
- **Translations & Tafsir:** Tarteel QUL project

---

## Design Notes

- This project prioritizes **search quality and clarity of results**
- Query expansion is intentionally **deferred** and planned for a separate experimental branch
- The current retrieval quality is considered strong without expansion

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/adamhamri9/quran-semantic-search
cd quran-semantic-search
````

### 2. Run the setup script

This script will:

* Create a virtual environment
* Install all required dependencies
* Prepare Qur'an and translation data
* Generate embeddings and FAISS indices

```bash
python setup.py
```

⚠️ **Important notes:**

* The **initial setup may take some time**, especially during the embedding generation step, depending on your hardware.
* After embedding the **original Arabic Qur'an text**, the setup script will **prompt you to enter target language codes**.

  * This allows you to generate embeddings **only for the languages you need**.
  * It helps avoid unnecessary resource usage if you only want a single language (e.g. `en`) instead of all supported languages.

### 3. Start the API

```bash
uvicorn api.main:app
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

## Disclaimer

⚠️ This is an educational project.  
While the architecture is carefully designed, the API is **not intended for production use**.
