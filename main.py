import spacy

from fastapi import FastAPI
from starlette.background import BackgroundTask
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from operator import itemgetter
import json, csv
import logging
from datetime import datetime


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["45.32.89.216", "192.168.219.108"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_lg")
konlp = spacy.load("ko_core_news_lg")

def write_req_res(data, filepath):
    with open(filepath, 'a') as f:
        if len(data) > 0:
            keys = data[0].keys()
            dict_writer = csv.DictWriter(f, fieldnames=keys)
            dict_writer.writerows(data)    

class Input(BaseModel):
    id_: str
    question: str
    keywords: str

@app.post("/similarity/sentence")
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

@app.get("/")
def test():
    return {"hello": "world"}


@app.post("/similarity/question/korean")
def check_word(input: Input):
    id_ = input.id_
    question = konlp(input.question)
    keywords = [konlp(word) for word in input.keywords.split(',')]

    # lemmatization
    lemmas = [token.lemma_ for token in question]
    question_token = [lemma.split("+")[0] for lemma in lemmas]
    vectors = [(word, konlp.vocab[word]) for word in question_token]

    question_info={
        "question": question.text,
        "is_valid": False,
        "included": [],
        "not_included":[]
    }
    data=[]
    record = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'id_': id_,
        'question': input.question,
        'keywords': input.keywords,
        'question_token': "",
        'keyword': "",
        'similarity': 0}
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

                new_record=record
                new_record["question_token"] = included["question_token"]
                new_record["keyword"] = included["keyword"]
                new_record["similarity"] = included["similarity"]

                data.append(record)
            else:
                question_info["not_included"].append(included)
    # write to qk_log.csv file
    if question_info["is_valid"] == False:
        data.append(record)

    # write_req_res(data, '/home/jiwon/myapi/logs/qk_log.csv')
    
    return question_info


@app.post("/similarity/question")
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
    record = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'id_': id_,
        'question': input.question,
        'keywords': input.keywords,
        'question_token': "",
        'keyword': "",
        'similarity': 0}
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

                new_record=record
                new_record["question_token"] = included["question_token"]
                new_record["keyword"] = included["keyword"]
                new_record["similarity"] = included["similarity"]

                data.append(record)
            else:
                question_info["not_included"].append(included)
    # write to qk_log.csv file
    if question_info["is_valid"] == False:
        data.append(record)

    write_req_res(data, '/home/jiwon/myapi/logs/qk_log.csv')
    
    return question_info