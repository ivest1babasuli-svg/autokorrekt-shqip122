from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from difflib import SequenceMatcher
import re

app = FastAPI()

# -------- Allow CORS --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- Load dictionary --------
def load_words(path: str):
    with open(path, encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

dictionary = load_words("dictionary.txt")
dictionary_set = set(dictionary)

# -------- Similarity function --------
def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

# -------- Autocorrect logic --------
def autocorrect(text: str):
    words = text.split()
    output = []
    corrections = []
    improvements = []

    for i, orig_word in enumerate(words):
        m = re.match(r"^(\W*)([\w\u00C0-\u017F]+)(\W*)$", orig_word, flags=re.UNICODE)
        if m:
            prefix, core, suffix = m.group(1), m.group(2), m.group(3)
        else:
            output.append(orig_word)
            continue

        lower = core.lower()

        if lower in dictionary_set:
            corrected_core = lower
        else:
            best_word = dictionary[0]
            best_score = 0.0
            for d in dictionary:
                s = similarity(lower, d)
                if s > best_score:
                    best_score = s
                    best_word = d
            corrected_core = best_word

        if i == 0 or core[0].isupper():
            corrected_core = corrected_core.capitalize()

        corrected_word = f"{prefix}{corrected_core}{suffix}"
        output.append(corrected_word)

        if lower != corrected_core.lower():
            corrections.append({"old": core, "new": corrected_core})

    return {
        "result": " ".join(output),
        "corrections": corrections,
        "improvements": improvements,
    }

# -------- API endpoint --------
@app.get("/autocorrect")
def correct(text: str):
    return autocorrect(text)

# -------- FRONTEND (THIS IS THE KEY PART) --------
# Serve EVERYTHING inside "static/" as the website root "/"
app.mount("/", StaticFiles(directory="static", html=True), name="static")
