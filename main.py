from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from difflib import SequenceMatcher
from fastapi.responses import JSONResponse

app = FastAPI()

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
    corrections = []

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
            corrections.append({"old": word, "new": corrected})

        # capitalize first word always
        if i == 0:
            corrected = corrected.capitalize()
        # preserve capitalization for other words
        elif word[0].isupper():
            corrected = corrected.capitalize()

        output.append(corrected)

    return " ".join(output), corrections


# -------- API endpoint --------
@app.get("/autocorrect")
def correct(text: str):
    corrected_text, corrections = autocorrect(text)
    
    improvements = [
        "Teksti është përmirësuar duke përdorur gjuhën standarde shqipe."
    ]

    return JSONResponse(content={
        "result": corrected_text,
        "corrections": corrections,
        "improvements": improvements
    })


# -------- Serve frontend --------
app.mount("/", StaticFiles(directory="static", html=True), name="static")
