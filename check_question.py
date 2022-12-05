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
    lexems = [(word, nlp.vocab[word]) for word in question_token]
    print(">>>>>", question_token)
    print("================")
    # print(">>>>>>>", lexems)
    for word, vector in lexems:
        print(f"{word} similarity: {vector.similarity(keyword[0])}")


    similarity={"similarity":[],"similars":[]}
    # for token in question:
    #     s = token.similarity(keyword[0])

    for word, vector in lexems:
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