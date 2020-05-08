import os
from collections import defaultdict
import sys

import jsonparse
import tokenizer
import indexfiler

import time

_CORPUS_PATH = '\\DEV'

if __name__ == '__main__':
    # Class setup
    tokenizer = tokenizer.Tokenizer()
    filer = indexfiler.IndexFiler()
    
    # File Writing setup
    current_tmp_index = 0
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
                    
                    filer.to_file(index, 'tmp_{}.index'.format(current_tmp_index))
                    current_tmp_index += 1

                    index.clear()
    except Exception as e:
        print('>> [ERROR] {:.2f} Processed up to doc_id: {}\nName: {}\nIndex Size: {}\n'.format(time.time() - start, current_tmp_index+1, rem_filename, sys.getsizeof(index)))
        print(e)

        filer.to_file(index, 'tmp_{}.index'.format(current_tmp_index+1))
    
    print('>> Writing tmp_{}.index with index of size {}'.format(current_tmp_index, sys.getsizeof(index)))
    filer.to_file(index, 'tmp_{}.index'.format(current_tmp_index))