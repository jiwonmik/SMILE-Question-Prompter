import nltk
from nltk import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords

import re
from pattern.text.en import singularize

PLURAL_TAG = ["NNS", "NNPS"]


class Tokenizer(object):
    """
    split the document into sentences and tokenize each sentence
    """
    def __init__(self):
        self.splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def preprocessing(self,text):
        """
        in: "What can I say about this place."
        out : ['What', 'can', 'I', 'say', 'about', 'this', 'place', '.']
        """
        # split into single sentence
        sentences = self.splitter.tokenize(text)

        question_text=[]
        for sent in sentences:
            sent=re.sub("[^a-zA-Z]", " ", sent)   # remove all besides alphabets
            text=sent.lower()                    # lower   
            question_text.append(text)

        # tokenization in each sentences
        words = sum([self.tokenizer.tokenize(sent) for sent in question_text],[])

        # stop_words =set(stopwords.words('english'))
        # words=[w for w in words if w not in stop_words]

        return words

class LemmatizationWithPOSTagger(object):
    def __init__(self):
        pass
    def get_wordnet_pos(self,treebank_tag):
        """
        return WORDNET POS compliance to WORDENT lemmatization (a,n,r,v) 
        """
        if treebank_tag.startswith('J'):
            return wordnet.ADJ
        elif treebank_tag.startswith('V'):
            return wordnet.VERB
        elif treebank_tag.startswith('N'):
            return wordnet.NOUN
        elif treebank_tag.startswith('R'):
            return wordnet.ADV
        else:
            # As default pos in lemmatization is Noun
            return wordnet.NOUN

    def pos_tag(self,tokens):
        # find the pos tagginf for each tokens [('What', 'WP'), ('can', 'MD'), ('I', 'PRP') ....
        pos_tokens = nltk.pos_tag(tokens)
    
        processed=[]
        wn_tag = []
        for word, pos in pos_tokens:
            if pos in PLURAL_TAG:
                # convert plural to singular
                processed.append((word, singularize(word),pos))    
            else:
                wn_tag.append((word, self.get_wordnet_pos(pos)))
        
        # lemmatization using pos tag   
        # convert into feature set of [('What', 'What', ['WP']), ('can', 'can', ['MD']), ... ie [original WORD, Lemmatized word, POS tag]
        for word, pos in wn_tag:
            processed.append((word, lemmatizer.lemmatize(word, pos),pos))

        return processed

    def get_keywords(self,tokens):
        return [token[1] for token in tokens]

"""
Check if the question is a valid one.
"""
def check_question(keywords, text):
    if all(word in text for word in keywords):
        print("valid question")
    else:
        print("unvalid question")

# example text
text = "How can people from different countries communicate?"
keywords=["How", "person", "men", "creating"]

lemmatizer = WordNetLemmatizer()
tokenizer = Tokenizer()
lemmatization_using_pos_tagger = LemmatizationWithPOSTagger()

#step 1 split document into sentence followed by tokenization
tokens = tokenizer.preprocessing(text)
print("====================")
#print(f"tokens:", tokens)

#step 2 lemmatization using pos tagger 
lemma_pos_token = lemmatization_using_pos_tagger.pos_tag(tokens)
# print(f"Tokens with pos tag:", lemma_pos_token)

#step 3 get keywords from the sentence
preprocessed_text = lemmatization_using_pos_tagger.get_keywords(lemma_pos_token)
print(f"Preprocessed text: ", preprocessed_text)
print("====================")

"""
현재 문제: keyword가 기본형이고 text에서 변형 단어가 쓰이면 ok, 하지만 그 반대면 확인 불가,,
=> keywords 입력으로 받을 때 NOUN/ADJ/VERB/ADV 구분해서 받기?
"""
# step 4 preprocess keywords
keywords=[w.lower() for w in keywords]
keyword_pos_token=lemmatization_using_pos_tagger.pos_tag(keywords)
print(f"Keyword with pos tag: ",keyword_pos_token)

preprocessed_keyword=lemmatization_using_pos_tagger.get_keywords(keyword_pos_token)
print(f"Preprocessed keywords: ", preprocessed_keyword)
print("====================")

# check if the question is a valid one
check_question(preprocessed_keyword, preprocessed_text)
