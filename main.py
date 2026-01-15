from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from difflib import SequenceMatcher
import os
import re

app = FastAPI()

# -------- Allow CORS --------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # allows all methods
    allow_headers=["*"],  # allows all headers
)

# -------- Load dictionary --------
def load_words(path: str):
    with open(path, encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]

dictionary = load_words("dictionary.txt")
dictionary_set = set(dictionary)  # fast lookup

# -------- Similarity function --------
def similarity(a: str, b: str) -> float:
    return SequenceMatcher(None, a, b).ratio()

# -------- Autocorrect logic (returns result, corrections, improvements) --------
def autocorrect(text: str):
    words = text.split()
    output = []
    corrections = []
    improvements = []

    for i, orig_word in enumerate(words):
        # Preserve leading/trailing punctuation (very simple handling)
        m = re.match(r"^(\W*)([\w\u00C0-\u017F]+)(\W*)$", orig_word, flags=re.UNICODE)
        if m:
            prefix, core, suffix = m.group(1), m.group(2), m.group(3)
        else:
            # no word characters found; keep as-is
            output.append(orig_word)
            continue

        lower = core.lower()

        # already correct → keep
        if lower in dictionary_set:
            corrected_core = lower
        else:
            # find closest dictionary word using similarity
            best_word = dictionary[0]
            best_score = 0.0

            for d in dictionary:
                s = similarity(lower, d)
                if s > best_score:
                    best_score = s
                    best_word = d

            corrected_core = best_word

        # preserve capitalization
        if i == 0:
            corrected_core = corrected_core.capitalize()
        elif core[0].isupper():
            corrected_core = corrected_core.capitalize()

        corrected_word = f"{prefix}{corrected_core}{suffix}"
        output.append(corrected_word)

        # record correction if changed (compare core lowercases)
        if lower != corrected_core:
            corrections.append({"old": core, "new": corrected_core})

    result = " ".join(output)
    return {"result": result, "corrections": corrections, "improvements": improvements}

# -------- API endpoint --------
@app.get("/autocorrect")
def correct(text: str):
    return autocorrect(text)

# -------- Serve frontend --------
app.mount("/", StaticFiles(directory="static", html=True), name="static")
