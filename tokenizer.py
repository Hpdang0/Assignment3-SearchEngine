import bs4

class Tokenizer():
    stopwords = []
    file = open("stopwords.txt",'r')
    lines = file.read().split()
    for word in lines:
        stopwords.append(word)

    def tokenize(self, content: str) -> [str]:
        token_list = []
        for word in content:
            word = word.lower().strip("!@#$%^&*(),-_=+./:;''\\][`")
            if len(word) >3 :
                if word not in self.stopwords:
                    if word not in token_list:
                        token_list.append(word)
        return token_list