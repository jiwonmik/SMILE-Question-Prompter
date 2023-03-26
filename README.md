# SMILE-Question-Prompter

This is a simple API for developing **😊[SMILE](https://portal.smile-pi.org/) Question Prompter.**

You can test with [demo page](https://nlp-for-smile.vercel.app/).

## 📑 Table of Contents

- [Features](#features)
- [Setup](#setup)
  - [Question Prompter API](#🔴-question-propmpter-api)
  - [Question Prompter Demo](#🌟-question-propmpter-demo)
- [Technologies](#technologies)

## ✨ Features

- API will check similarity between your every word from question sentence and keywords by its [word-vector from spacy](https://spacy.io/api/lexeme#similarity).

## Setup

## 🔴 Question Propmpter API

### ☝️ Requirements

```
spacy
fastapi
```

## ✨ spaCy

### 💻 Settings

#### 1. Install spaCy

See [here](https://spacy.io/usage) for installing spaCy

```shell
conda create -n nlp
conda activate nlp
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
conda activate nlp
```

Run the development server.

```shell
uvicorn main:app --reload
```

## 🌟 Question Propmpter Demo

You can check with [Demo Page](https://nlp-for-smile.vercel.app/).

```shell
git clone https://github.com/jiwonmik/NLP-for-SMILE.git
npm install
npm run dev
```
