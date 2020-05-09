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
            for key, posting in index.items():
                posting_str = ' '.join(','.join(str(p) for p in pair) for pair in posting)
                file.write('{key} | {posting_str}\n'.format(key=key, posting_str=posting_str))

    def ids_from_file(self, filepath: str) -> dict:
        ids_dict = dict()
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                pair = line.split()
                ids_dict[int(pair[0])] = pair[1]
            
        return ids_dict

    def ids_to_file(self, ids:dict, filepath: str) -> dict:
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


        

filer = IndexFiler()

# d = filer.ids_from_file('test.txt')
d = {1: 'test.com', 2: 'test2.com', 3: 'test3.com'}

filer.ids_to_file(d, 'test.txt')