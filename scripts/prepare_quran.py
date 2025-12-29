import json
from config import Config

RAW_QURAN_PATH = Config.RAW_QURAN_PATH
RAW_TAFSIR_PATH = Config.RAW_TAFSIR_DIR / "ar_mukhtasar.json"
OUTPUT_PATH = Config.PROCESSED_QURAN_FILE

def parse_tanzil_line(line: str):
    line = line.strip()
    if not line or line.startswith("#"):
        return None

    parts = line.split("|", 2)
    if len(parts) != 3:
        return None

    surah, ayah, text = parts
    return int(surah), int(ayah), text.strip()

def prepare_quran():
    tafsir_data = json.loads(RAW_TAFSIR_PATH.read_text(encoding="utf-8"))

    verses = []

    with RAW_QURAN_PATH.open(encoding="utf-8") as f:
        for line in f:
            parsed = parse_tanzil_line(line)
            if parsed is None:
                continue

            surah, ayah, text = parsed
            
            key = f"{surah}:{ayah}"
            
            tafsir_entry = tafsir_data.get(key, "")
            if isinstance(tafsir_entry, dict):
                tafsir_text = tafsir_entry.get("text", "")
            else:
                tafsir_text = str(tafsir_entry)

            verses.append({
                "surah": surah,
                "ayah": ayah,
                "text": text,
                "tafsir": tafsir_text,
                "embedding_text": f"آية: {text} تفسير: {tafsir_text}"
            })

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(verses, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

if __name__ == "__main__":
    prepare_quran()