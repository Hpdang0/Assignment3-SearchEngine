import re

from bs4 import BeautifulSoup

## please pip install nltk

from nltk.tokenize import word_tokenize,RegexpTokenizer
from nltk.stem import PorterStemmer,WordNetLemmatizer
from collections import defaultdict

ps = PorterStemmer()
lm = WordNetLemmatizer()
rtk = RegexpTokenizer(r'\w+')

# These values will be added to the tokens as frequency
WEIGHT_P = 1
WEIGHT_H02 = 2
WEIGHT_H36 = 1.4
WEIGHT_BOLD = 1.3
WEIGHT_ITALICIZED = 1.2
WEIGHT_LIST = 1
WEIGHT_HYPERLINK = 1.5

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
                freq[word] += mod

    def tokenize_index(self, text: str, encoding: str) -> [str]:
        frequency = defaultdict(int)
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
            if word in self.stopwords or word.isnumeric() or not word.isalpha():
                continue
            ## using nltk Porter Stemmer
            ## not sure if we should use only lower case as "Apple" is different from "apple"
            stemmed = ps.stem(word.lower())
            if len(word)in range(2,25):
                stemmed_frequency[stemmed] += freq

        # print(stemmed_frequency)
        return stemmed_frequency

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