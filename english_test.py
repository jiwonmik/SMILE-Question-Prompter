
import spacy
from spacy.vocab import Vocab
import json


"""
Tokenization
"""
# for token in doc:
#     print(token.text)

"""
POS Tagging
spaCy returns an object that carries information about POS, tags, and more
"""
# for token in doc:
#     print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
#             token.shape_, token.is_alpha, token.is_stop)


class Question_checker(object):
    def __init__(self, package, question: str, keywords: list):
        self.nlp = spacy.load(package)
        # `Doc`
        self.question = self.nlp(question)
        self.keywords = [self.nlp(word) for word in keywords]
    
    def is_valid_q(self):
        q_base_tokens = [word.lemma_ for word in self.question]

        # syntactic check
        not_included = []
        for keyword in self.keywords:
            if keyword[0].lemma_ not in q_base_tokens:
                not_included.append(keyword)
        print(not_included)
        if not not_included:
            print("Valid Question")
            return 
        
        # semantic check
        for word in not_included:
            for token in self.question:
                similarity=word[0].similarity(token)
                if similarity>0.2:
                    print(f"{word} similarity with {token}: ", similarity)


PKG = "en_core_web_sm"
question = "How can a man communicate with foreigners?"
keywords = ["How", "person", "men", "creating"]

question_checker = Question_checker(PKG, question, keywords)
question_checker.is_valid_q()




