import tokenizer
import search
import re
import time

_QUERY_LEGAL = re.compile(r'^[a-z|A-Z|\d| ]+$')

def ensure_legal(i: str) -> bool:
    if _QUERY_LEGAL.search(i) == None:
        return False
    return True

if __name__ == '__main__':
    tokenizer = tokenizer.Tokenizer()
    
    
    max_doc_id = 0
    with open("final.ids", 'r', encoding='utf-8') as file:
        first_line = file.readline()
        for last_line in file:
            pass
    lis = last_line.split(' ', 1)
    max_doc_id = int(lis[0])

    search = search.Search('final.index', 'final.ids', max_doc_id)

    while True:
        i = input('\n\n[Type "q" to quit]\n>> Query: ')
        print()

        # Ensure that query is alphanumeric
        if not ensure_legal(i):
            print('[ERROR] Query must contain only alphanumeric characters.')
            continue
        if i == 'q':
            break

        # Tokenize just like how we did for indexing
        query_tokens = tokenizer.tokenize_query(i)

        # Time and do search
        start = time.time()
        results = search.search(query_tokens)
        end = time.time()
        print('[Query took {:.3f} seconds]'.format(end - start))

        # Print the results
        if results is None:
            print('No results found!')
        else:
            print('Results:')
            for url in results:
                print(url)

        print()