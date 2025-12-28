# Quran Semantic Search API (Educational Project) purposes to understand NLP, embeddings, and search technologies, rather than being a production-ready API.

🚧 **Status:** Work in progress (MVP / Learning Experiment)

---

## Goal

The main goal is to **learn how semantic search works** by creating an API that can search Qur'anic ayat by **meaning**, combining the ayah text, tafsir, and translations for context.  

This project helps practice working with:

* Text preprocessing and cleaning
* Generating embeddings for multiple languages
* Serving search results via an API

---

## Multi-Language Embeddings

The project will generate **separate embeddings** for the following languages:

* Arabic (original Qur'an text)
* English
* Urdu
* Turkish
* Indonesian

Each language will have its own embedding, allowing semantic search queries in multiple languages. Embeddings can also be combined with tafsir to improve search relevance.

---

## Tech Stack

* **Python** – main programming language  
* **FAISS** – for fast similarity search over embeddings  
* **Sentence Transformers** – for generating semantic embeddings  
* **FastAPI** – for building the API endpoints  

---

## Data Sources

* **Qur'an text**: [Tanzil Project (used **without modification**)](https://tanzil.net/download/)
* **Tafsir & Translations**: [Tarteel QUL project](https://qul.tarteel.ai/resources/)  

> ⚠️ Note: This project is **educational**. The API is for learning and experimentation; it is **not production-ready**.

---

## Learning Points

This project helps to explore key concepts in semantic search and embeddings:

* Converting Qur'an text, tafsir, and translations into vector embeddings that capture semantic meaning  
* Using FAISS for fast similarity search  
* Combining ayah text, tafsir, and translations to improve search relevance  
* Handling text preprocessing, tokenization, and encoding issues  
* Serving embeddings via an API for real-time search
* Query expansion strategies: explored both rule-based expansion (using synonym dictionaries for Arabic) 
  and optional LLM-based expansion (for complex queries or multi-language support). 
