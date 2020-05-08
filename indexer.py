import os
from collections import defaultdict
from tinydb import TinyDB, Query


import jsonparse
import tokenizer
import wordprocess

_CORPUS_PATH = '\\DEV'



if __name__ == '__main__':
    db = TinyDB('index.json') # this is the file with the index info
    db.purge() # THIS CLEARS THE FILE !!! (we probably want it to be blank a the start)
    index = defaultdict(list)
    doc_ids = defaultdict(int)
    tokenizer = tokenizer.Tokenizer()
    threshhold = 5 # this is how many documents we go before writing to the file and clearing our local index


    current_doc_id = 0

    for path, folder, filenames in os.walk(os.getcwd() + _CORPUS_PATH):
        current_doc_id += 1
        
        for filename in filenames:
            if filename.endswith('.gitignore'):
                continue
            
            # Parse JSON here
            url, content, encoding = jsonparse.parse(path + '\\' + filename)
            doc_ids[current_doc_id] = url

            # Tokenize Content
            tokens = tokenizer.tokenize(content)
            print(tokens)
            # Word Processing
            # tokens = wordprocess.process(tokens)

            # Indexing
            # for token in tokens:
                # index[token].append(current_doc_id)

            for token in tokens:
                index[token].append(current_doc_id)
            
        if current_doc_id >= threshhold:
            threshhold += current_doc_id
            for key in index.keys():
                db.insert({'token' : key, 'list': index[key]}) # the 'token' will help us when we're searching tokens later
            index.clear() # clearing the dict
    
    for key in index.keys(): # one last addition
        db.insert({'token' : key, 'list': index[key]})
    index.clear() # clearing the dict but it doesn't really matter at this point