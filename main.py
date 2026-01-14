from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from difflib import SequenceMatcher
import os

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

# -------- Autocorrect logic --------
def autocorrect(text: str) -> str:
    words = text.split()
    output = []

    for i, word in enumerate(words):
        lower = word.lower()

        # already correct → keep
        if lower in dictionary_set:
            corrected = lower
        else:
            # find closest dictionary word
            best_word = dictionary[0]
            best_score = 0.0

            for d in dictionary:
                s = similarity(lower, d)
                if s > best_score:
                    best_score = s
                    best_word = d

            corrected = best_word

        # capitalize first word always
        if i == 0:
            corrected = corrected.capitalize()
        # preserve capitalization for other words
        elif word[0].isupper():
            corrected = corrected.capitalize()

        output.append(corrected)

    return " ".join(output)

# -------- API endpoint --------
@app.get("/autocorrect")
def correct(text: str):
    return {"result": autocorrect(text)}

# -------- Serve frontend --------
app.mount("/", StaticFiles(directory="static", html=True), name="static")
