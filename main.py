import nltk
from nltk import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords


import re


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
        # doesn't have to be checked
        skip_tokens=[".",",","?","'","\""]
        tokens=[token for token in tokens if token not in skip_tokens]

        # find the pos tagginf for each tokens [('What', 'WP'), ('can', 'MD'), ('I', 'PRP') ....
        pos_tokens = nltk.pos_tag(tokens)

        # lemmatization using pos tagg   
        # convert into feature set of [('What', 'What', ['WP']), ('can', 'can', ['MD']), ... ie [original WORD, Lemmatized word, POS tag]
        lemmatized = []
        for word, pos in pos_tokens:
            lemmatized.append((word, lemmatizer.lemmatize(word, self.get_wordnet_pos(pos)),pos))

        return lemmatized

        # doesn't have to be preprocessed
        # skip_tokens=["DT"]
        # temp=[]
        # for sent in pos_tokens:
        #     temp.append([tokens for tokens in sent if tokens[1] not in skip_tokens])
        # pos_tokens=temp

    def get_keywords(self,tokens):
        return [token[1] for token in tokens]

"""
Check if the question is a valid one.
"""
def check_question(keywords, text):
    if all(word in text[0] for word in keywords):
        print("valid question")
    else:
        print("unvalid question")

# example text
text = "For some quick analysis, creating a corpus could be overkill. If all you need is a word list, there are simpler ways to achieve that goal."
#text= "women are strong."

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
keywords=["quickly", "create", "simple", "innovates"]
keyword_pos_token=lemmatization_using_pos_tagger.pos_tag(keywords)
# print(f"Keyword with pos tag: ",keyword_pos_token)

preprocessed_keyword=lemmatization_using_pos_tagger.get_keywords(keyword_pos_token)
print(f"Preprocessed keywords: ", preprocessed_keyword)
print("====================")

# check if the question is a valid one
check_question(preprocessed_keyword, preprocessed_text)


