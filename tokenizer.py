from bs4 import BeautifulSoup

class Tokenizer():
    stopwords = []
    file = open("stopwords.txt",'r')
    lines = file.read().split()
    for word in lines:
        stopwords.append(word)

    def tokenize(self, text: str) -> [str]:
        token_list = []
        soup = BeautifulSoup(text, features="html.parser")
        list = soup.get_text(strip=True,separator = '').split()

        for word in list:
            word = word.lower().strip("!@#$%^&*(),-_=+./:;''\\][`")
            if len(word) >3 :
                if word not in self.stopwords:
                    if word not in token_list:
                        token_list.append(word)
                        
        return token_list