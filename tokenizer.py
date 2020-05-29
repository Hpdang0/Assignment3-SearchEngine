import re

from bs4 import BeautifulSoup

## please pip install nltk

from nltk.tokenize import word_tokenize,RegexpTokenizer
from nltk.stem import PorterStemmer,WordNetLemmatizer
from collections import defaultdict

ps = PorterStemmer()
lm = WordNetLemmatizer()
rtk = RegexpTokenizer(r'[a-zA-Z0-9]+')

# These values will be added to the tokens as frequency
WEIGHT_H02 = 1
WEIGHT_H36 = 2
WEIGHT_BOLD = 3
WEIGHT_HYPERLINK = 4
WEIGHT_ITALICIZED = 5
WEIGHT_LIST = 6
WEIGHT_NORMAL = None

_ALPHA_NUM = r'^[a-zA-Z0-9]*$' 
ALPHA_NUM = re.compile(_ALPHA_NUM)

class pair(list):
    def __init__(self):
        super().__init__([0, ''])

class Tokenizer():
    stopwords = []
    file = open("stopwords.txt",'r')
    lines = file.read().split()
    for word in lines:
        stopwords.append(word)

    def parse_for(self, freq, soup, query, mod):
        for iter in soup.find_all(query):
            text = iter.get_text(strip=True,separator = ' ')
            for word in text.split():
                # print(word, mod)
                freq[word][0] += 1
                freq[word][1] += str(mod)

    def tokenize_index(self, text: str, encoding: str) -> [str]:
        frequency = defaultdict(pair)
        soup = BeautifulSoup(text, features="lxml", from_encoding=encoding)
        ## using nltk tokenizer
        ## for debugging ( some words are joined togather my the parser )
        # print(soup.text.split())

        # Check if a content block is provided to us, and if so, look for commin html tags in it
        content = soup.find(id='content')
        if content is None:
            content = soup.find(id='main')

        if content is not None:
            # print('Implicit Parsing...\n')
            self.parse_for(frequency, content, 'p', WEIGHT_P)
            self.parse_for(frequency, content, re.compile(r'^h[0-2]$'), WEIGHT_H02)
            self.parse_for(frequency, content, re.compile(r'^h[3-6]$'), WEIGHT_H36)
            self.parse_for(frequency, content, re.compile(r'^(b|strong)$'), WEIGHT_BOLD)
            self.parse_for(frequency, content, re.compile(r'^(i|em)$'), WEIGHT_ITALICIZED)
            self.parse_for(frequency, content, re.compile(r'^(li)$'), WEIGHT_LIST)
            self.parse_for(frequency, content, 'a', WEIGHT_HYPERLINK)
                
       # If not, look for commmon html tags in entire soup
        else:
            # print('Explicit parsing...\n')
            self.parse_for(frequency, soup, 'p', WEIGHT_P)
            self.parse_for(frequency, soup, re.compile(r'^h[0-2]$'), WEIGHT_H02)
            self.parse_for(frequency, soup, re.compile(r'^h[3-6]$'), WEIGHT_H36)
            self.parse_for(frequency, soup, re.compile(r'^(b|strong)$'), WEIGHT_BOLD)
            self.parse_for(frequency, soup, re.compile(r'^(i|em)$'), WEIGHT_ITALICIZED)
            self.parse_for(frequency, soup, 'a', WEIGHT_HYPERLINK)
            

        # If we managed to find absolutely no html tags, just extract the entire body
        if len(frequency) == 0 and soup is not None:
            # print('Full parsing...\n')
            for word in soup.get_text(strip=True,separator = ' ').split():
                frequency[word] += 1

        stemmed_frequency = defaultdict(int)
        for word, freq in frequency.items():
            if word in self.stopwords or ALPHA_NUM.search(word) is None or word.isnumeric() or self.is_hex(word):
                continue
            ## using nltk Porter Stemmer
            ## not sure if we should use only lower case as "Apple" is different from "apple"
            stemmed = ps.stem(word.lower())
            if len(word)in range(2,25):
                stemmed_frequency[stemmed.rstrip()] += freq

        # print(stemmed_frequency)
        return stemmed_frequency

    def is_hex(self, s):
        for c in s:
            if not c.isnumeric() and c not in 'abcdefABCDEF':
                return False

        return True

    def tokenize_query(self, text: str) -> [str]:
        stemmed_query = []
        for word in text.split():
            if word in self.stopwords or ALPHA_NUM.search(word) is None or word.isnumeric() or self.is_hex(word):
                continue
            ## using nltk Porter Stemmer
            ## not sure if we should use only lower case as "Apple" is different from "apple"
            stemmed = ps.stem(word.lower())
            if len(word)in range(2,25):
                stemmed_query.append(stemmed)
        print('query: ' + "'" + stemmed + "'")
        return stemmed_query