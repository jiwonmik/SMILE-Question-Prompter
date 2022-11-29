import spacy

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import json

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_sm")

class Input(BaseModel):
    question: str
    keyword: str

@app.post("/sentence_similarity")
def check_sentence(input: Input):
    question = nlp(input.question)
    #question_token = [token for token in question]
    
    keyword = nlp(input.keyword)

    similarity={
        "similarity": question.similarity(keyword)
    }

    return similarity

@app.post("/word_similarity")
def check_word(input: Input):
    question = nlp(input.question)
    keyword = nlp(input.keyword)

    similarity={}
    for token in question:
        similarity["similarity"] = (token.text,token.similarity(keyword[0]))
    most_similar={"most_similars": []}
    for token in question:
        s = token.similarity(keyword[0])
        if s > 0.2:
            most_similar["most_similars"].append({"word": token.text, "similarity": s})
    return most_similar