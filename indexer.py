import os
from collections import defaultdict

import jsonparse
import tokenizer
import wordprocess

_CORPUS_PATH = '\\DEV'



if __name__ == '__main__':
    index = defaultdict(list)
    doc_ids = defaultdict(int)
    tokenizer = tokenizer.Tokenizer()

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