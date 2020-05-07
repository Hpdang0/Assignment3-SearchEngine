from bs4 import BeautifulSoup

## please pip install nltk

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

ps = PorterStemmer()

class Tokenizer():
    stopwords = []
    file = open("stopwords.txt",'r')
    lines = file.read().split()
    for word in lines:
        stopwords.append(word)

    def tokenize(self, text: str) -> [str]:
        token_list = []
        soup = BeautifulSoup(text, features="html.parser")
        ## using nltk tokenizer
        list = word_tokenize(soup.get_text(strip=True,separator = ''))
        for word in list:
            ## using nltk Porter Stemmer
            ## not sure if we should use only lower case as "Apple" is different from "apple"
            word = ps.stem(word.lower())
            if len(word) > 2 :
                if word not in self.stopwords:
                    if word not in token_list:
                        token_list.append(word)
        return token_list