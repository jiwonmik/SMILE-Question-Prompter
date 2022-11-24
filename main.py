import nltk
from nltk import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import stopwords

import re
from pattern.text.en import singularize

from gensim.models import KeyedVectors


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

        # delete duplicated words
        words = list(set(words))

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

    def convert_to_base(self,tokens):
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

def syntactic_check(keywords, text):
    not_included=[w for w in keywords if w not in text]
    if not_included:
        return not_included
    else:
        return False

def check_semantic(text):
    # loading the downloaded model
    model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True)
    # the model is loaded. It can be used to perform all of the tasks mentioned above.
    # print(model.vectors.shape)
    # (3000000, 300)

    question=set(preprocessed_text)
    for word in syntactic:
        similar_words=[w[0] for w in model.most_similar(positive=[word])]
        intersection=[common for common in similar_words if common in question]
        if not intersection:
            print(f"\"{word}\" is not in the question.")
            return False
    return True

"""
 check if the question is a valid one
"""
print(f"Question: {question}")
print(f"keywords: {keywords}")

# example text
question = "How can a man communicate with foreigners?"
keywords=["How", "person", "men", "creating"]

lemmatizer = WordNetLemmatizer()
tokenizer = Tokenizer()
lemmatization_using_pos_tagger = LemmatizationWithPOSTagger()

#step 1 split document into sentence followed by tokenization
tokens = tokenizer.preprocessing(question)
print("====================")
#print(f"tokens:", tokens)

#step 2 lemmatization using pos tagger 
lemma_pos_token = lemmatization_using_pos_tagger.convert_to_base(tokens)
# print(f"Tokens with pos tag:", lemma_pos_token)

#step 3 get keywords from the sentence
preprocessed_text = lemmatization_using_pos_tagger.get_keywords(lemma_pos_token)
print(f"Preprocessed text: ", preprocessed_text)
print("====================")

# step 4 preprocess keywords
keywords=[w.lower() for w in keywords]
keyword_pos_token=lemmatization_using_pos_tagger.convert_to_base(keywords)
print(f"Keyword with pos tag: ",keyword_pos_token)

preprocessed_keyword=lemmatization_using_pos_tagger.get_keywords(keyword_pos_token)
print(f"Preprocessed keywords: ", preprocessed_keyword)
print("====================")


# 1. CHECK syntactic similarity :
syntactic = syntactic_check(preprocessed_keyword, preprocessed_text)

if syntactic:
    print("\nHave to check semantic similarity")
    # 2. CHECK semantic similarity :
    if check_semantic(syntactic):
        print("valid question")
    else:
        print("unvalid question")
else:
    print("valid question")
