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
    keywords = input.keywords.replace(" ","").split(",")
    keywords = [konlp(word) for word in keywords]

    # lemmatization
    lemmas = [token.lemma_ for token in question]
    question_token = [lemma.split("+")[0] for lemma in lemmas]
    vectors = [(word, konlp.vocab[word]) for word in question_token]

    question_info={
        "question": question.text,
        "valid": True,
        "keywords_result":[]
    }

    for keyword in keywords:
        keyword_result={
            "keyword": keyword.text,
            "result": {
                "included":[],
                "not_included":[]
            }
        }
        for word, vector in vectors:
            sim=vector.similarity(keyword)
            result={
                "question_token": word, 
                "similarity": round(sim,3)}
            if sim > 0.5:
                keyword_result["result"]["included"].append(result)
            else:
                if sim > 0.2:
                    keyword_result["result"]["not_included"].append(result)
        if len(keyword_result["result"]["included"])==0:
            question_info["valid"]=False
        question_info["keywords_result"].append(keyword_result)

    return question_info


@app.post("/similarity/question")
def check_word(input: Input):
    id_ = input.id_
    question = nlp(input.question)
    keywords = input.keywords.replace(" ","").split(",")
    keywords = [nlp(word) for word in keywords]

    # lemmatization
    question_token = [token.lemma_ for token in question]
    vectors = [(word, nlp.vocab[word]) for word in question_token]

    question_info={
        "question": question.text,
        "valid": True,
        "keywords_result":[]
    }

    # data=[]
    # record = {'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    #     'id_': id_,
    #     'question': input.question,
    #     'keywords': input.keywords,
    #     'question_token': "",
    #     'keyword': "",
    #     'similarity': 0}
    for keyword in keywords:
        keyword_result={
            "keyword": keyword.text,
            "result": {
                "included":[],
                "not_included":[]
            }
        }
        for word, vector in vectors:
            sim=vector.similarity(keyword)
            result={
                "question_token": word, 
                "similarity": round(sim,3)}
            if sim > 0.5:
                keyword_result["result"]["included"].append(result)
                # new_record=record
                # new_record["question_token"] = included["question_token"]
                # new_record["keyword"] = included["keyword"]
                # new_record["similarity"] = included["similarity"]
                # data.append(record)
            else:
                if sim > 0.2:
                    keyword_result["result"]["not_included"].append(result)
        if len(keyword_result["result"]["included"])==0:
            question_info["valid"]=False
        question_info["keywords_result"].append(keyword_result)

    # write to qk_log.csv file
    # if question_info["is_valid"] == False:
    #     data.append(record)

    # write_req_res(data, '/home/jiwon/myapi/logs/qk_log.csv')
    
    return question_info