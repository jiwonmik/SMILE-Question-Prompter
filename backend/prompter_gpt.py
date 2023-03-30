import os
import openai
from config import API_KEY

openai.api_key = API_KEY

model_id = "gpt-3.5-turbo"


def getGPTResponse(prompter_input):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful question evaluator that will check if question a valid question that includes all the keywords suggested. All the tokens from question sentence will be compared with each keywords and if any question token is a similar word with a keyword, it is determined the keyword is included in the question.",
            },
            {
                "role": "user",
                "content": "question: How many people had gone through computer training?, keywords: individuals, computers",
            },
            {
                "role": "assistant",
                "content": 'Prompter Check: Valid. your question is a valid question. 1. The keyword "individuals" is a similar word to "people" in the question. 2. The keyword "computers" is a similar word to "computer"',
            },
            {
                "role": "user",
                "content": "question: How many people had gone through computer training?, keywords: fast",
            },
            {
                "role": "assistant",
                "content": 'Prompter Check: Invalid. your question is not a valid question. 1. The keyword "fast" is not similar to any word in your question. ',
            },
            {"role": "user", "content": prompter_input},
        ],
    )

    response_text = response["choices"][0]["message"]["content"]
    print(response_text)
    return response_text
