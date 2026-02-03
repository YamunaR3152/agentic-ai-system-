from pathlib import Path

DATA_FOLDER = Path(__file__).resolve().parent.parent / "data"

def load_texts():
    docs = []

    if not DATA_FOLDER.exists():
        print("⚠️ Data folder not found")
        return docs

    for file in DATA_FOLDER.glob("*.txt"):
        try:
            text = file.read_text(encoding="utf-8")
            docs.append({"source": file.name, "text": text})
            print(f"📄 Loaded local file: {file.name}")
        except Exception as e:
            print("Error reading file:", e)

    return docs
