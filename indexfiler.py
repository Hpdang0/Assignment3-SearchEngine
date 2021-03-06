import os

class IndexFiler():
    def __init__(self):
        pass
    

    def index_from_file(self, filepath: str) -> dict:
    # Converts a file into a usable index
        index_dict = dict()
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                key, posting = line.split(' | ')
                postings_parsed = [[int(p[0]), float(p[1])] for p in (pair.split(',') for pair in posting.split())]
                index_dict[key.rstrip()] = postings_parsed    
        return index_dict
    
    def index_to_file(self, index:dict, filepath:str):
    # Writes index to file so it can be later parsed with from_file
        with open(filepath, 'w', encoding='utf-8') as file:
            for key, posting in sorted(index.items()):
                docs = []
                for doc in posting:
                    id = str(doc[0])
                    freq = str(doc[1][0])
                    mode = doc[1][1]
                    docs.append(','.join([id, freq, mode]))
                # posting_str = ' '.join(','.join(str(p) for p in pair) for pair in posting)
                file.write('{key} | {posting_str}\n'.format(key=key, posting_str=' '.join(docs)))

    def ids_from_file(self, filepath: str) -> dict:
        # Retrieves the doc_id:url pair and return a dict of it
        ids_dict = dict()
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                pair = line.split()
                ids_dict[int(pair[0])] = pair[1]    
        return ids_dict


    def ids_to_file(self, ids:dict, filepath: str) -> dict:
        # Writes a doc_ids:url pair to a file
        with open(filepath, 'w', encoding='utf-8') as file:
            for id, url in ids.items():
                file.write('{} {}\n'.format(id, url))


    def new_combine(self, staged_filepath):
        final_dict = dict()
        with open('final.index', 'r+', encoding='utf-8') as file_a: #tmp_0, tmp_0 + tmp_1, tmp_0 + tmp_1 + tmp_2
            with open(staged_filepath, 'r', encoding='utf-8') as file_b: #tmp_1, tmp_2, tmp_3
                temp_file = open('temp.index', 'w', encoding='utf-8')
                lineA = file_a.readline()
                lineB = file_b.readline()
                while True:  
                    if lineA == "":
                        #debug purpose
                        #print('process done')
                        temp_file.close()
                        break
                    elif lineB == "":
                        temp_file.write(lineA)
                        lineA = file_a.readline()
                    else:
                        keyA, postingA = lineA.split(' | ')
                        keyB, postingB = lineB.split(' | ')
                        #Checking if A is the earlier term & adding it into index
                        if keyA < keyB:
                            #print debug purpose
                            #print('A', keyA, keyB)
                            temp_file.write(lineA)
                            lineA = file_a.readline()
                        #Checking if B is the earlier term & adding it into index
                        elif keyA > keyB:
                            #print debug purpose
                            #print('B', keyA, keyB)
                            temp_file.write(lineB)
                            lineB = file_b.readline()
                        #Checking if A and B are the same and combining them
                        elif keyA == keyB:
                            postings_parsedA = [[int(p[0]), int(p[1]), str(p[2])] for p in (pair.split(',') for pair in postingA.split())]
                            postings_parsedB = [[int(p[0]), int(p[1]), str(p[2])] for p in (pair.split(',') for pair in postingB.split())]
                            final_dict[keyA.rstrip()] = postings_parsedA + postings_parsedB
                            #printdebug purpose
                            # print("combining term", keyA)
                            posting_str = ' '.join(','.join(str(t) for t in tri) for tri in final_dict[keyA.rstrip()])
                            temp_file.write('{key} | {posting_str}\n'.format(key=keyA, posting_str=posting_str))
                            final_dict.clear()
                            lineA = file_a.readline()
                            lineB = file_b.readline()
        os.remove('final.index')
        os.rename('temp.index', 'final.index')
                
                    


    def bsearch_file(self, path, query):
    # Given a file path and a query, perform a binary search and its posting
        with open(path, 'r') as file:
            lo = 0
            file.seek(0, 2)
            hi = file.tell() - 1
            mid = (lo+hi) >> 1

            return self._bsearch(file, query, lo, hi, mid)


    def _bsearch(self, file, query, lo, hi, mid):
    # Recursive binary search on a line-sorted text file
        if lo >= hi:                    # If true, we know that it's not in the list 
            return None

        if mid > 0:                     # If mid turns out to have truncated to 0, then we need to be sure not to read forward, but go backwards
            file.seek(mid - 1)          # When we seek, we could have seeked in the middle of a line,
            file.readline()             # so read until a new line and instead start at the next line
            mid_line = file.tell()
        else:
            mid_line = 0                # To ensure that we can still read the first line
            file.seek(mid_line)

        line = file.readline()          # Now that we are the start of an actual line, read it
        token = line.split(' | ')[0]    # and parse it to only get the token

        if token == query:              # If it's an exact match, it's what we're looking for
            return line
        
        if query > token:                # If true, b-search upper section
            return self._bsearch(file, query, mid+1, hi, (mid+hi) >> 1)

        if query < token:                # If true, b-search lower section
            return self._bsearch(file, query, lo, mid, (lo+mid) >> 1)


        

# filer = IndexFiler()

# # d = filer.ids_from_file('test.txt')
# d = {1: 'test.com', 2: 'test2.com', 3: 'test3.com'}

# filer.ids_to_file(d, 'test.txt')