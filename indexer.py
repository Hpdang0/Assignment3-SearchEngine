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
from urllib.parse import urlparse

CORPUS_PATH = '\\DEV'
LOW_VALUE_THRESHOLD = 10
SIMHASH_THRESH = 0.92

_FRAGMENT = r'[#].*'
FRAGMENT = re.compile(_FRAGMENT)

def merge_indexes():
    filer = indexfiler.IndexFiler()
    if os.path.exists('final.index'):
        os.remove('final.index')
    os.rename("tmp_0.index", "final.index")
    file_list = os.scandir('.') # list of files in the directory (their names)
    for file in file_list: 
        if file.name.endswith('.index') and 'tmp_' in file.name:
            print('Merging {} with final.index...'.format(file.name))
            filer.new_combine(file.name)
            #os.remove(file.name)
            

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz"
            + r"|ppsx)$", parsed.path.lower())
    except TypeError:
        print ("TypeError for ", parsed)
        raise

if __name__ == '__main__':
    # Class setup
    tokenizer = tokenizer.Tokenizer()
    filer = indexfiler.IndexFiler()
    cache = cache.Cache(3)
    
    # File Writing setup
    current_tmp_index = 0
    current_tmp_ids = 0
    write_threshhold = 6291472 #6291472
    # write_threshhold = 12582944 # this is how many documents we go before writing to the file and clearing our local index
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
                
                if not is_valid(url):
                    print('[SKIPPING] URL is not valid: {}\n'.format(url))

                # Tokenize Content
                frequency = tokenizer.tokenize_index(content, encoding)
                if len(frequency) == 0:
                    continue

                # print(frequency, '\n')
                # -------------- Filtering done here
                # Determine if indexing is worthwhile
                low_value_page = False
                if sum(val[0] for val in frequency.values()) < LOW_VALUE_THRESHOLD:
                    low_value_page = True
                    try:
                        print('{0:.2f} [SKIPPING] URL found to be of low value: {1}\n{2} with tokens...\n{3}\n'.format(time.time() - start, sum(frequency.values()), url, frequency[0]))
                    except:
                        print('{0:.2f} [SKIPPING] URL found to be of low value: {1}\n{2}\n'.format(time.time() - start, sum(val[0] for val in frequency.values()), url))

                # Compare similarity to last 5 pages we crawled in
                similar = False
                cache1 = None
                if not low_value_page:
                    for curl, cfreq, ccache in cache:
                        cache2 = ccache
                        sim_result, cache1, cache2 = Similarity(frequency, cfreq, SIMHASH_THRESH, cache1=cache1, cache2=ccache)
                        
                        if sim_result:
                            similar = True
                            print('{0:.2f} [SKIPPING] Similarity found between these two urls. Skipping the second url...\n{1}\n{2}\n'.format(time.time() - start, curl, url))
                            break
                # ------------------------ End filter

                # Remember this url in our cache
                cache.append((url, frequency, cache1))

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
                        print('{:.2f} Writing tmp_{}.index with index of size {}\n'.format(time.time() - start, current_tmp_index, sys.getsizeof(index)))
                        
                        filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index))
                        current_tmp_index += 1

                        index.clear()

                    # Writing of doc_ids
                    if sys.getsizeof(doc_ids) >= write_threshhold:
                        print('{:.2f} Writing final.ids with doc ids of size {}\n'.format(time.time() - start, sys.getsizeof(doc_ids)))

                        filer.ids_to_file(doc_ids, 'final.ids')
                        current_tmp_ids += 1
                    
                    current_doc_id += 1
                
                # frequency.clear()

        
        #here is where we would put the "HELPER"
        #f.close()      
    except Exception as e:
        print('{:.2f} [ERROR] Processed up to doc_id: {}\nName: {}\nIndex Size: {}\n'.format(time.time() - start, current_doc_id, rem_filename, sys.getsizeof(index)))
        print(e + '\n')

        filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index+1))
    
    # Final Operations
    print('{:.2f} Writing tmp_{}.index with index of size {}'.format(time.time() - start, current_tmp_index, sys.getsizeof(index)))
    filer.index_to_file(index, 'tmp_{}.index'.format(current_tmp_index))
    
    print('{:.2f} Writing final.ids with doc ids of size {}'.format(time.time() - start, sys.getsizeof(doc_ids)))
    filer.ids_to_file(doc_ids, 'final.ids')

    print('{:.2f} Processed up to doc_id: {}\nName: {}\nIndex Size: {}\nUnique Tokens: {}\n'.format(time.time() - start, current_doc_id, url, sys.getsizeof(index), total_unique_tokens))

    # Merging of indexes
    print('{:.2f} Merging indexes...\n'.format(time.time() - start))
    merge_indexes()

    #queries = {"hey": []}

    # after we have merged we can hypothetically get a list