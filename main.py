import nltk
from nltk import PorterStemmer, LancasterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet

# example text
# text = "For some quick analysis, creating a corpus could be overkill. If all you need is a word list, there are simpler ways to achieve that goal."
text= "women are strong."

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
        tokens = [self.tokenizer.tokenize(sent) for sent in sentences]

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
        # find the pos tagginf for each tokens [('What', 'WP'), ('can', 'MD'), ('I', 'PRP') ....
        pos_tokens = [nltk.pos_tag(token) for token in tokens]

        # doesn't have to be checked

        # doesn't have to be preprocessed

        # lemmatization using pos tagg   
        # convert into feature set of [('What', 'What', ['WP']), ('can', 'can', ['MD']), ... ie [original WORD, Lemmatized word, POS tag]
        pos_tokens = [[(word, lemmatizer.lemmatize(word,self.get_wordnet_pos(pos_tag)), [pos_tag]) for (word,pos_tag) in pos] for pos in pos_tokens]
        return pos_tokens[0]
    
    def get_keywords(self,tokens):
        return [token[1] for token in tokens]

lemmatizer = WordNetLemmatizer()
tokenizer = Tokenizer()
lemmatization_using_pos_tagger = LemmatizationWithPOSTagger()

#step 1 split document into sentence followed by tokenization
tokens = tokenizer.tokenize(text)

#step 2 lemmatization using pos tagger 
lemma_pos_token = lemmatization_using_pos_tagger.pos_tag(tokens)
print("====================")
print(f"tokens with pos tag:", lemma_pos_token)

#step 3 get keywords from the sentence
preprocessed_text = lemmatization_using_pos_tagger.get_keywords(lemma_pos_token)
print(f"Preprocessed text: ", preprocessed_text)
print("====================")


