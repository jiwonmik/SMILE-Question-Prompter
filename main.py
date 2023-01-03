import spacy

from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from operator import itemgetter
import json

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_lg")

class Input(BaseModel):
    question: str
    keyword: str

@app.post("/sentence_similarity")
def check_sentence(input: Input):
    question = nlp(input.question)
    
    keyword = nlp(input.keyword)

    similarity={
        "similarity": round(question.similarity(keyword),3)
    }

    return similarity

@app.post("/word_similarity")
def check_word(input: Input):
    question = nlp(input.question)
    keyword = nlp(input.keyword)

    question_token = [token.lemma_ for token in question]
    vectors = [(word, nlp.vocab[word]) for word in question_token]

    similarity={"similarity":[],"similars":[]}

    for word, vector in vectors:
        sim = vector.similarity(keyword[0])
        similarity["similarity"].append({"word": word, "similarity": round(sim, 3)})

        if sim > 0.1:
            similarity["similars"].append({"word": word, "similarity": round(sim,3)})

    most_similar=sorted(similarity["similars"], key=itemgetter('similarity'), reverse=True)[0]
    similarity["most_similar"]={
        "word": most_similar["word"],
        "similarity": most_similar["similarity"]
    }
    return similarity

@app.post("/check_question")
def check_word(input: Input):
    question = nlp(input.question)
    keywords = [nlp(word) for word in input.keyword.split(',')]

    # lemmatization
    question_token = [token.lemma_ for token in question]
    vectors = [(word, nlp.vocab[word]) for word in question_token]

    question_info={
        "question": question.text,
        "is_valid": False,
        "included": [],
        "not_included":[]
    }

    for word, vector in vectors:
        for keyword in keywords:
            sim=vector.similarity(keyword)
            included = { 
                "question_token": word, 
                "keyword": keyword.text,
                "similarity": round(sim,3)}
            if sim > 0.5:
                question_info["is_valid"]=True
                question_info["included"].append(included)
                break
            else:
                question_info["not_included"].append(included)


    return question_info
