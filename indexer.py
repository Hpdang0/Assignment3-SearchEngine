import os
from collections import defaultdict
import sys

import jsonparse
import tokenizer
import indexfiler
from io import TextIOWrapper

import time

_CORPUS_PATH = '\\DEV'

def merge_indexes():
    filer = indexfiler.IndexFiler()
    f = open("final.index", 'w')
    f.close()

    file_list = os.scandir('.') # list of files in the directory (their names)
    for file in file_list:
        if file.name.endswith('.index') and 'tmp_' in file.name:
            print('Merging {} with final.index...'.format(file.name))
            filer.combine('final.index', file.name)

if __name__ == '__main__':
    # Class setup
    tokenizer = tokenizer.Tokenizer()
    filer = indexfiler.IndexFiler()
    
    # File Writing setup
    current_tmp_index = 0
    current_tmp_ids = 0
    write_threshhold = 12582944 # this is how many documents we go before writing to the file and clearing our local index

    # Helper variables
    index = defaultdict(list)
    doc_ids = defaultdict(int)
    frequency = defaultdict(int)
    rem_filename = None
    unique_tokens = set()
    total_unique_tokens = 0
    
    current_doc_id = 0
    try:
        start = time.time()
        for path, folder, filenames in os.walk(os.getcwd() + _CORPUS_PATH):
            for filename in filenames:
                rem_filename = filename
                frequency.clear()
                if filename.endswith('.gitignore'):
                    continue
                
                current_doc_id += 1
                

                # Parse JSON here
                url, content, encoding = jsonparse.parse(path + '\\' + filename)
                doc_ids[current_doc_id] = url

                # Tokenize Content
                tokens = tokenizer.tokenize(content, encoding)
                for token in tokens:
                    unique_tokens.add(token)
                total_unique_tokens = len(unique_tokens)
                
                # Convert to indexable frequency
                for token in tokens:
                    frequency[token] += 1

                # Add to index on memory
                for token in frequency:
                    index[token].append([current_doc_id, frequency[token]])

                # Logging
                if current_doc_id % 100 == 0:
                    print('{:.2f} Processed up to doc_id: {}\nName: {}\nIndex Size: {}\nUnique Tokens: {}\n'.format(time.time() - start, current_doc_id, filename, sys.getsizeof(index), total_unique_tokens))

                # Write of index
                if sys.getsizeof(index) >= write_threshhold:
                    print('>> Writing tmp_{}.index with index of size {}'.format(current_tmp_index, sys.getsizeof(index)))
                    
                    filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index))
                    current_tmp_index += 1

                    index.clear()

                # Writing of doc_ids
                if sys.getsizeof(doc_ids) >= write_threshhold:
                    print('>> Writing tmp_{}.ids with doc ids of size {}'.format(current_tmp_ids, sys.getsizeof(doc_ids)))

                    filer.ids_to_file(doc_ids, 'tmp_{}.ids'.format(current_tmp_ids))
                    current_tmp_ids += 1

        
        #here is where we would put the "HELPER"
        #f.close()      
    except Exception as e:
        print('>> [ERROR] {:.2f} Processed up to doc_id: {}\nName: {}\nIndex Size: {}\n'.format(time.time() - start, current_doc_id, rem_filename, sys.getsizeof(index)))
        # print(e + '\n')
        raise(e)

        filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index+1))
    
    # Final Operations
    print('>> Writing tmp_{}.index with index of size {}'.format(current_tmp_index, sys.getsizeof(index)))
    filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index))
    
    print('>> Writing tmp_{}.ids with doc ids of size {}'.format(current_tmp_ids, sys.getsizeof(doc_ids)))
    filer.ids_to_file(doc_ids, 'tmp_{}.ids'.format(current_tmp_ids))

    print('{:.2f} Processed up to doc_id: {}\nName: {}\nIndex Size: {}\nUnique Tokens: {}\n'.format(time.time() - start, current_doc_id, filename, sys.getsizeof(index), total_unique_tokens))

    # Merging of indexes
    print('Merging indexes...\n')
    merge_indexes()