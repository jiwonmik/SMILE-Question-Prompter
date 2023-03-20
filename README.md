# NLP-for-SMILE
This is a simple API for developing **😊[SMILE](https://portal.smile-pi.org/smile/) Question Prompter** 

### ☝️ Requirements
```
spacy
fastapi
```

## ✨ spaCy
### 💻 Settings
#### 1.  Install spaCy
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

### 💻 How to use - Gunicorn Service
