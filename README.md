# SMILE-Question-Prompter

In SMILE, the question prompter should check student's question if it includes all given keywords set by teachers or group leaders.

This is a server for **😊[SMILE](https://smile.seedsofempowerment.org/) Question Prompter.**

✨ [***SMILE has been updated to version 3! Check it out!***](https://smile.seedsofempowerment.org/)

You can test **Prompter** server using Spacy and OpenAI API with [demo page](https://smile-question-prompter.vercel.app/).

## 📑 Table of Contents

- [Features](#features)
- [Setup](#setup)
  - [Question Prompter API](#question-propmpter-api)
  - [Question Prompter Demo](#question-propmpter-demo)
- [Technologies](#technologies)

## Features

Enter `keywords` that should be included in the `questions`, and then enter your question. Then, check if your question is a valid one.

- If you click ✅ **check with spaCy**, API will get similarity between every word from question sentence and keywords by its [word-vector from spacy](https://spacy.io/api/lexeme#similarity), and chekc if your question is a valid question.
- If you click ✅ **check with [OpenAI](https://openai.com/blog/openai-api)**, API will ask OpenAI model `"gpt-3.5-turbo"` if your question is a valid question.

## Setup

## Question Propmpter API

### ☝️ Requirements

```
spacy
fastapi
openai
```

## ✨ spaCy

### 💻 Settings

#### 1. Install spaCy

See [here](https://spacy.io/usage) for installing spaCy

```shell
conda create -n smile
conda activate smile
conda install -c conda-forge spacy
```

#### 2. Download Trained Models for **Korean** and **English**

```shell
python -m spacy download en_core_web_lg
python -m spacy download ko_core_news_lg
```

Above two models are used like below.

```python
nlp = spacy.load("en_core_web_lg")
konlp = spacy.load("ko_core_news_lg")
```

### 💻 How to use - development server

Activate conda environment you just created.

```shell
conda activate smile
```

Run the development server.

```shell
uvicorn main:app --reload
```

## Question Propmpter Demo

You can check with [Demo Page](https://smile-question-prompter.vercel.app/).

```shell
git clone https://github.com/jiwonmik/SMILE-Question-Prompter.git
npm install
npm run dev
```

## Technologies
⚒️ **Backend** - Python, FastAPI, Nginx, spaCy, OpneAI API, Amazone Route 53, Gunicorn

🪄 **Frontend** - Vite + ReactJS, Typescript
