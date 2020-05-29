class IndexFiler():
    def __init__(self):
        pass
    
    def index_from_file(self, filepath: str) -> dict:
    # Converts a file into a usable index
        index_dict = dict()
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                key, posting = line.split('|')
                postings_parsed = [[int(p[0]), int(p[1])] for p in (pair.split(',') for pair in posting.split())]
                index_dict[key.rstrip()] = postings_parsed
            
        return index_dict
    
    def index_to_file(self, index:dict, filepath:str):
    # Writes index to file so it can be later parsed with from_file
        with open(filepath, 'w', encoding='utf-8') as file:
            for key, posting in sorted(index.items(), lambda item: item[0]):
                posting_str = ' '.join(','.join(str(p) for p in pair) for pair in posting)
                file.write('{key} | {posting_str}\n'.format(key=key, posting_str=posting_str))

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

    def combine(self, final_file_name:str, staged_filepath):
        stoppoint = 300
        i = 0
        staged_dict = dict()
        with open(staged_filepath, 'r', encoding='utf-8') as staged_file:
            for line in staged_file:
                key, posting = line.split('|')
                postings_parsed = [[int(p[0]), int(p[1])] for p in (pair.split(',') for pair in posting.split())]
                staged_dict[key.rstrip()] = postings_parsed


        tmp_dict = dict()
        temp_file = open('temp.index', 'w', encoding='utf-8')
        with open(final_file_name, 'r', encoding='utf-8') as final_file:
            for line in final_file:
                key, posting = line.split('|')
                postings_parsed = [[int(p[0]), int(p[1])] for p in (pair.split(',') for pair in posting.split())]
                tmp_dict[key.rstrip()] = postings_parsed
                if key.rstrip() in staged_dict.keys():
                    tmp_dict[key.rstrip()] += staged_dict[key.rstrip()]
                    del staged_dict[key.rstrip()]
                i+=1
                if i >= stoppoint: # we're stopping for a minute
                    stoppoint+=i
                    for key, posting in tmp_dict.items(): #writing to a temp file
                        posting_str = ' '.join(','.join(str(p) for p in pair) for pair in posting)
                        temp_file.write('{key} | {posting_str}\n'.format(key=key, posting_str=posting_str))
                    tmp_dict.clear()
        
        for key, posting in staged_dict.items(): #writing to a temp file
            posting_str = ' '.join(','.join(str(p) for p in pair) for pair in posting)
            temp_file.write('{key} | {posting_str}\n'.format(key=key, posting_str=posting_str))
        tmp_dict.clear()


        with open("temp.index", 'r', encoding='utf-8') as f:
            with open("final.index", "w", encoding='utf-8') as f1:
                for line in f:
                    f1.write(line)
        
        f1.close()
        f.close()
        staged_file.close()


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
            # print(line[:20])
            return line
        
        if query > line:                # If true, b-search upper section
            return self._bsearch(file, query, mid+1, hi, (mid+hi) >> 1)

        if query < line:                # If true, b-search lower section
            return self._bsearch(file, query, lo, mid, (lo+mid) >> 1)


        

# filer = IndexFiler()

# # d = filer.ids_from_file('test.txt')
# d = {1: 'test.com', 2: 'test2.com', 3: 'test3.com'}

# filer.ids_to_file(d, 'test.txt')