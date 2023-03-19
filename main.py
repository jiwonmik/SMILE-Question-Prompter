import spacy

from fastapi import FastAPI
from starlette.background import BackgroundTask
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_lg")
konlp = spacy.load("ko_core_news_lg")

class Input(BaseModel):
    question: str
    keywords: str

@app.post("/similarity/question/korean")
def check_word(input: Input):
    question = konlp(input.question)
    keywords = input.keywords.replace(" ", "").split(",")
    keywords = [konlp(word) for word in keywords]

    question_info = {
        "question": question.text,
        "valid": True,
        "keywords_result": []
    }

    # lemmatization
    lemmas = [token.lemma_ for token in question]
    question_token = [lemma.split("+")[0] for lemma in lemmas]
    vectors = [(word, konlp.vocab[word]) for word in question_token]

    for keyword in keywords:
        keyword_result = {
            "keyword": keyword.text,
            "result": {
                "included": [],
                "not_included": [],
                "identical": []
            },
        }
        for word, vector in vectors:
            # if it is exactly same word
            if keyword == word:
                keyword_result["result"]["identical"].append(word)
                continue
            # check similarity
            sim = vector.similarity(keyword)
            result = {
                "question_token": word,
                "similarity": round(sim, 3)}

            if sim > 0.5:
                keyword_result["result"]["included"].append(result)
            else:
                if sim > 0.2:
                    keyword_result["result"]["not_included"].append(result)

            if len(keyword_result["result"]["included"]) + len(keyword_result["result"]["identical"]) == 0:
                question_info["valid"] = False
            question_info["keywords_result"].append(keyword_result)

    return question_info


@app.post("/similarity/question")
def check_word(input: Input):
    question = nlp(input.question)
    keywords = input.keywords.replace(" ","").split(",")
    keywords = [nlp(word) for word in keywords]

    question_info = {
        "question": question.text,
        "valid": True,
        "keywords_result": []
    }

    # lemmatization
    question_token = [token.lemma_ for token in question]
    vectors = [(word, nlp.vocab[word]) for word in question_token]

    for keyword in keywords:
        keyword_result = {
            "keyword": keyword.text,
            "result": {
                "included": [],
                "not_included": [],
                "identical": []
            }
        }
        for word, vector in vectors:
            # if it is exactly same word
            if keyword.text == word:
                keyword_result["result"]["identical"].append(word)
                continue
            # check similarity
            sim = vector.similarity(keyword)
            result = {
                "question_token": word,
                "similarity": round(sim, 3)}
            if sim > 0.5:
                keyword_result["result"]["included"].append(result)
            else:
                if sim > 0.2:
                    keyword_result["result"]["not_included"].append(result)
        if len(keyword_result["result"]["included"]) + len(keyword_result["result"]["identical"]) == 0:
            question_info["valid"] = False
        question_info["keywords_result"].append(keyword_result)

    return question_info