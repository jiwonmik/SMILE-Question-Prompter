import nltk
from nltk import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


class Tokenizer(object):
    """
    split the document into sentences and tokenize each sentence
    """
    def __init__(self):
        self.splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def tokenize(self,text):
        """
        in: "What can I say about this place."
        out : ['What', 'can', 'I', 'say', 'about', 'this', 'place', '.']
        """
        # split into single sentence
        sentences = self.splitter.tokenize(text)
        # tokenization in each sentences
        tokens = sum([self.tokenizer.tokenize(sent) for sent in sentences],[])

        return tokens

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
        pos_tokens = [nltk.pos_tag(tokens)]

        # doesn't have to be preprocessed
        # skip_tokens=["DT"]
        # temp=[]
        # for sent in pos_tokens:
        #     temp.append([tokens for tokens in sent if tokens[1] not in skip_tokens])
        # pos_tokens=temp

        # lemmatization using pos tagg   
        # convert into feature set of [('What', 'What', ['WP']), ('can', 'can', ['MD']), ... ie [original WORD, Lemmatized word, POS tag]
        pos_tokens = [[(word, lemmatizer.lemmatize(word,self.get_wordnet_pos(pos_tag)), [pos_tag]) for (word,pos_tag) in pos] for pos in pos_tokens]
        return pos_tokens
    
    def get_keywords(self,tokens):
        keywords=[]
        for sentence in tokens:
            keywords.append([token[1] for token in sentence])
        return keywords

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
tokens = tokenizer.tokenize(text)
print("====================")
#print(f"tokens:", tokens)

#step 2 lemmatization using pos tagger 
lemma_pos_token = lemmatization_using_pos_tagger.pos_tag(tokens)
#print(f"Tokens with pos tag:", lemma_pos_token)

#step 3 get keywords from the sentence
preprocessed_text = lemmatization_using_pos_tagger.get_keywords(lemma_pos_token)
print(f"Preprocessed text: ", preprocessed_text)
print("====================")

keywords=["quick", "create", "simple"]
keyword_pos_token=lemmatization_using_pos_tagger.pos_tag(keywords)
# print(f"Keyword with pos tag: ",keyword_pos_token)

preprocessed_keyword=lemmatization_using_pos_tagger.get_keywords(keyword_pos_token)[0]
print(f"Preprocessed keywords: ", preprocessed_keyword)
print("====================")

# check if the question is a valid one
check_question(preprocessed_keyword, preprocessed_text)
