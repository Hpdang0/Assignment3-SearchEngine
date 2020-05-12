import re

import tokenizer
import search

_QUERY_LEGAL = re.compile(r'^[a-z|A-Z|\d| ]+$')

def ensure_legal(i: str) -> bool:
    if _QUERY_LEGAL.search(i) == None:
        return False
    return True

if __name__ == '__main__':
    tokenizer = tokenizer.Tokenizer()
    search = search.Search('final.index', 'final.ids')
    
    while True:
        i = input('>> Query: ')
        print()

        # Ensure that query is alphanumeric
        if not ensure_legal(i):
            print('[ERROR] Query must contain only alphanumeric characters.\n')
            continue

        # Tokenize just like how we did for indexing
        query_tokens = tokenizer.tokenize_query(i)

        # Search for results and print
        print('Results:')
        for url in search.search(query_tokens):
            print(url)