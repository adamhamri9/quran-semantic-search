import json
from pathlib import Path

RAW_QURAN_PATH = Path("data/raw/quran-tanzil.txt")
RAW_TAFSIR_PATH = Path("data/raw/ar_al-mukhtasar.json")
OUTPUT_PATH = Path("data/processed/quran.json")


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
    tafsir = json.loads(RAW_TAFSIR_PATH.read_text(encoding="utf-8"))

    verses = []
    idx = 0

    with RAW_QURAN_PATH.open(encoding="utf-8") as f:
        for line in f:
            parsed = parse_tanzil_line(line)
            if parsed is None:
                continue

            surah, ayah, text = parsed
            tafsir_text = tafsir[idx] if idx < len(tafsir) else ""

            verses.append({
                "id": idx,
                "surah": surah,
                "ayah": ayah,
                "text": text,
                "tafsir": tafsir_text,
                "embedding_text": f"آية: {text} تفسير: {tafsir_text}"
            })

            idx += 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(verses, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )


if __name__ == "__main__":
    prepare_quran()