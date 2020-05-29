import os
from collections import defaultdict
import sys
import re

import jsonparse
import tokenizer
import indexfiler
from io import TextIOWrapper
import cache
import time
from similar import Similarity

CORPUS_PATH = '\\DEV'
LOW_VALUE_THRESHOLD = 20
SIMHASH_THRESH = 0.9

_FRAGMENT = r'[#].*'
FRAGMENT = re.compile(_FRAGMENT)

def merge_indexes():
    filer = indexfiler.IndexFiler()
    f = open("final.index", 'w')
    f.close()

    file_list = os.scandir('.') # list of files in the directory (their names)
    for file in file_list:
        count = 0
        if file.name.endswith('.index') and 'tmp_{}.index'.format(0) in file.name:
            print('Merging {} with final.index...'.format('tmp_{}.index'.format(current_tmp_index)))
            filer.new_combine('final.index', 'tmp_{}.index'.format(count), 'tmp_{}.index'.format(count + 1))
            count += 1

if __name__ == '__main__':
    # Class setup
    tokenizer = tokenizer.Tokenizer()
    filer = indexfiler.IndexFiler()
    cache = cache.Cache()
    
    # File Writing setup
    current_tmp_index = 0
    current_tmp_ids = 0
    write_threshhold = 12582944 # this is how many documents we go before writing to the file and clearing our local index
    # Helper variables
    index = defaultdict(list)
    doc_ids = defaultdict(int)
    frequency = defaultdict(int)
    unique_tokens = set()
    total_unique_tokens = 0
    filename = None
    
    current_doc_id = 1
    try:
        start = time.time()
        for path, folder, filenames in os.walk(os.getcwd() + CORPUS_PATH):
            for filename in filenames:
                rem_filename = filename
                if filename.endswith('.gitignore'):
                    continue

                # Parse JSON here
                url, content, encoding = jsonparse.parse(path + '\\' + filename)
                doc_ids[current_doc_id] = url

                if FRAGMENT.search(url) is not None:
                    continue

                # Tokenize Content
                frequency = tokenizer.tokenize_index(content, encoding)

                # -------------- Filtering done here
                # Determine if indexing is worthwhile
                low_value_page = False
                if sum(frequency.values()) < LOW_VALUE_THRESHOLD:
                    low_value_page = True
                    print('[SKIPPING] URL found to be of low value: \n{0} tokens\nURL: {1}'.format(sum(frequency.values()), url))

                # Compare similarity to last 5 pages we crawled in
                similar = False
                for url_token_pair in cache:
                    # print(frequency, url_token_pair[1], sep='\n')
                    if Similarity(frequency, url_token_pair[1], SIMHASH_THRESH):
                        similar = True
                        print('[SKIPPING] Similarity found between these two urls. Skipping the second url...\n{0}\n{1}'.format(url_token_pair[0], url))
                        break
                # ------------------------ End filter

                # Remember this url in our cache
                cache.append((url, frequency))

                # Actually add to our index
                if not similar and not low_value_page:
                    # Put weights on frequency

                    # Add to index on memory
                    for token in frequency:
                        index[token].append([current_doc_id, frequency[token]])

                    # Logging
                    if current_doc_id % 100 == 0:
                        print('{:.2f} Processed up to doc_id: {}\nName: {}\nIndex Size: {}\nUnique Tokens: {}\n'.format(time.time() - start, current_doc_id, url, sys.getsizeof(index), total_unique_tokens))

                    # Write of index
                    if sys.getsizeof(index) >= write_threshhold:
                        print('>> Writing tmp_{}.index with index of size {}'.format(current_tmp_index, sys.getsizeof(index)))
                        
                        filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index))
                        current_tmp_index += 1

                        index.clear()

                    # Writing of doc_ids
                    if sys.getsizeof(doc_ids) >= write_threshhold:
                        print('>> Writing final.ids with doc ids of size {}'.format(sys.getsizeof(doc_ids)))

                        filer.ids_to_file(doc_ids, 'final.ids')
                        current_tmp_ids += 1
                
                # Prepare for next document
                current_doc_id += 1
                frequency.clear()

        
        #here is where we would put the "HELPER"
        #f.close()      
    except Exception as e:
        print('>> [ERROR] {:.2f} Processed up to doc_id: {}\nName: {}\nIndex Size: {}\n'.format(time.time() - start, current_doc_id, rem_filename, sys.getsizeof(index)))
        print(e + '\n')

        filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index+1))
    
    # Final Operations
    print('>> Writing tmp_{}.index with index of size {}'.format(current_tmp_index, sys.getsizeof(index)))
    filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index))
    
    print('>> Writing final.ids with doc ids of size {}'.format(sys.getsizeof(doc_ids)))
    filer.ids_to_file(doc_ids, 'final.ids')

    print('{:.2f} Processed up to doc_id: {}\nName: {}\nIndex Size: {}\nUnique Tokens: {}\n'.format(time.time() - start, current_doc_id, url, sys.getsizeof(index), total_unique_tokens))

    # Merging of indexes
    print('Merging indexes...\n')
    merge_indexes()

    #queries = {"hey": []}

    # after we have merged we can hypothetically get a list