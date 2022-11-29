import spacy

from fastapi import FastAPI
from pydantic import BaseModel

import json

app = FastAPI()

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
        similarity[token.text] = token.similarity(keyword[0])
    most_similar={}
    for token in question:
        s = token.similarity(keyword[0])
        if s > 0.2:
            most_similar[token.text] = s
    return most_similar