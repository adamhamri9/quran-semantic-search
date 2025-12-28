import json
from pathlib import Path

RAW_TRANSLATIONS_DIR = Path("data/raw/translations")
RAW_TAFSIR_DIR = Path("data/raw/tafsir")
OUTPUT_DIR = Path("data/processed/translations")

def get_tafsir_data(lang_code):
    for tafsir_file in RAW_TAFSIR_DIR.glob(f"{lang_code}_*.json"):
        return json.loads(tafsir_file.read_text(encoding="utf-8"))
    return {}

def prepare_translations():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    for trans_file in RAW_TRANSLATIONS_DIR.glob("*.json"):
        lang_code = trans_file.name.split('_')[0]
        tafsir_data = get_tafsir_data(lang_code)
        trans_data = json.loads(trans_file.read_text(encoding="utf-8"))
        
        processed_verses = []

        for key, value in trans_data.items():
            surah, ayah = map(int, key.split(':'))
            translation_text = value.get('t', '')
            
            tafsir_entry = tafsir_data.get(key, "")
            if isinstance(tafsir_entry, dict):
                tafsir_text = tafsir_entry.get("text", "")
            else:
                tafsir_text = str(tafsir_entry)

            processed_verses.append({
                "surah": surah,
                "ayah": ayah,
                "translation": translation_text,
                "tafsir": tafsir_text,
                "embedding_text": f"Translation: {translation_text} Tafsir: {tafsir_text}"
            })

        output_path = OUTPUT_DIR / f"{lang_code}_quran.json"
        output_path.write_text(
            json.dumps(processed_verses, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )

if __name__ == "__main__":
    prepare_translations()