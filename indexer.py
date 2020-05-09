import os
from collections import defaultdict
import sys

import jsonparse
import tokenizer
import indexfiler
from io import TextIOWrapper

import time

_CORPUS_PATH = '\\DEV'

if __name__ == '__main__':
    filer = indexfiler.IndexFiler()
    f = open("final.index", 'w')
    f.close()

    file_list = os.scandir('.') # list of files in the directory (their names)
    for file_name in file_list:
        if 'tmp_' in file_name.name:
            filer.combine('final.index', file_name.name)

    with open('final.index', 'r', encoding='utf-8') as f:
        for line in f:
            print(line, '\n')

if __name__ == '__main2__':
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
                if current_doc_id % 100 == 0:
                    print('{:.2f} Processed up to doc_id: {}\nName: {}\nIndex Size: {}\n'.format(time.time() - start, current_doc_id, filename, sys.getsizeof(index)))

                # Parse JSON here
                url, content, encoding = jsonparse.parse(path + '\\' + filename)
                doc_ids[current_doc_id] = url

                # Tokenize Content
                tokens = tokenizer.tokenize(content)
                
                # Convert to indexable frequency
                for token in tokens:
                    frequency[token] += 1

                # Add to index on memory
                for token in frequency:
                    index[token].append([current_doc_id, frequency[token]])

                # Write after threshhold documents
                # if current_doc_id >= write_threshhold * current_tmp_index:
                if sys.getsizeof(index) >= write_threshhold:
                    print('>> Writing tmp_{}.index with index of size {}'.format(current_tmp_index, sys.getsizeof(index)))
                    
                    filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index))
                    current_tmp_index += 1

                    index.clear()

                if sys.getsizeof(doc_ids) >= write_threshhold:
                    print('>> Writing tmp_{}.ids with doc ids of size {}'.format(current_tmp_ids, sys.getsizeof(doc_ids)))

                    filer.ids_to_file(doc_ids, 'tmp_{}.ids'.format(current_tmp_ids))
                    current_tmp_ids += 1

        
        #here is where we would put the "HELPER"
        #f.close()      
    except Exception as e:
        print('>> [ERROR] {:.2f} Processed up to doc_id: {}\nName: {}\nIndex Size: {}\n'.format(time.time() - start, current_tmp_index+1, rem_filename, sys.getsizeof(index)))
        print(e)

        filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index+1))
    
    print('>> Writing tmp_{}.index with index of size {}'.format(current_tmp_index, sys.getsizeof(index)))
    filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index))
    
    print('>> Writing tmp_{}.ids with doc ids of size {}'.format(current_tmp_ids, sys.getsizeof(doc_ids)))
    filer.ids_to_file(doc_ids, 'tmp_{}.ids'.format(current_tmp_ids))