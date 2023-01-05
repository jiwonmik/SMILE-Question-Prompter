import spacy

from fastapi import FastAPI, Request, Response
from starlette.background import BackgroundTask
from pydantic import BaseModel
from starlette.types import Message
from fastapi.middleware.cors import CORSMiddleware

from operator import itemgetter
import json
import logging

logger = logging.getLogger("main")
logging.basicConfig(level=logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_hander = logging.StreamHandler()
stream_hander.setFormatter(formatter)
logger.addHandler(stream_hander)

file_handler = logging.FileHandler('info.log', mode='w')
logger.addHandler(file_handler)

origins = ["*"]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

nlp = spacy.load("en_core_web_lg")

# def write_req_res(id, c1, c2, similarity):
#     data = {'id': id, 'c1': c1, 'c2': c2, 'similarity': similarity}
#     df = pd.DataFrame(data)
#     with open('/home/jiwon/log.csv', 'a') as f:
#         df.to_csv(f, header=False)

def log_info(req_body, res_body):
    logger.info(req_body)
    logger.info(res_body)

async def set_body(request: Request, body: bytes):
    async def receive() -> Message:
        return {'type': 'http.request', 'body': body}
    request._receive = receive

@app.middleware("http")
async def some_middleware(request: Request, call_next):
    req_body = await request.body()
    await set_body(request, req_body)
    response = await call_next(request)

    res_body = b''
    async for chunk in response.body_iterator:
        res_body += chunk

    task = BackgroundTask(log_info, req_body, res_body)
    return Response(content=res_body, status_code=response.status_code, 
        headers=dict(response.headers), media_type=response.media_type, background=task)

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
