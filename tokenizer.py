from bs4 import BeautifulSoup

## please pip install nltk

from nltk.tokenize import word_tokenize,RegexpTokenizer
from nltk.stem import PorterStemmer,WordNetLemmatizer

ps = PorterStemmer()
lm = WordNetLemmatizer()
rtk = RegexpTokenizer(r'\w+')

class Tokenizer():
    stopwords = []
    file = open("stopwords.txt",'r')
    lines = file.read().split()
    for word in lines:
        stopwords.append(word)

    def tokenize_index(self, text: str, encoding: str) -> [str]:
        token_list = []
        soup = BeautifulSoup(text, features="lxml", from_encoding=encoding)
        ## using nltk tokenizer
        ## for debugging ( some words are joined togather my the parser )
        # print(soup.text.split())
        list = rtk.tokenize(soup.text)
        for word in list:
            if word in self.stopwords:
                continue
            ## using nltk Porter Stemmer
            ## not sure if we should use only lower case as "Apple" is different from "apple"
            word = ps.stem(word.lower())
            if len(word)in range(2,25):
                if word not in self.stopwords and not word.isnumeric():
                    # print(word)
                    token_list.append(word)
        return token_list

    def tokenize_query(self, text: str) -> [str]:
        list = rtk.tokenize(text)
        token_list = []
        for word in list:
            if word in self.stopwords:
                continue
            word = ps.stem(word.lower())
            if len(word)in range(2,25):
                if word not in self.stopwords and not word.isnumeric():
                    token_list.append(word)
            # print(word)
        return token_list