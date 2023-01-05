import spacy

from fastapi import FastAPI
from starlette.background import BackgroundTask
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from operator import itemgetter
import json, csv
import logging
from datetime import datetime


origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_lg")

def write_req_res(data, filepath):
    with open(filepath, 'a') as f:
        keys = data[0].keys()
        dict_writer = csv.DictWriter(f, fieldnames=keys)
        dict_writer.writerows(data)    

class Input(BaseModel):
    id_: str
    question: str
    keywords: str

@app.post("/sentence_similarity")
def check_sentence(input: Input):
    id_ = input.id_
    question = nlp(input.question)
    keywords = nlp(input.keywords)

    data = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'id_': id_,
        'question': question.text,
        'keywords': keywords.text,
        'similarity': round(question.similarity(keywords),3)}
    #  write to sw_log.csv file
    write_req_res(data, '/home/jiwon/myapi/logs/sw_log.csv')

    return data

@app.post("/check_question")
def check_word(input: Input):
    id_ = input.id_
    question = nlp(input.question)
    keywords = [nlp(word) for word in input.keywords.split(',')]

    # lemmatization
    question_token = [token.lemma_ for token in question]
    vectors = [(word, nlp.vocab[word]) for word in question_token]

    question_info={
        "question": question.text,
        "is_valid": False,
        "included": [],
        "not_included":[]
    }
    data=[]
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
                record = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                        'id_': id_,
                        'question': question.text,
                        'keywords': ','.join([k.text for k in keywords]),
                        'question_token': included["question_token"],
                        'keyword': included["keyword"],
                        'similarity': included["similarity"]}
                data.append(record)
            else:
                question_info["not_included"].append(included)
    # write to qk_log.csv file
    write_req_res(data, '/home/jiwon/myapi/logs/qk_log.csv')
    
    return question_info