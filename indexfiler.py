class IndexFiler():
    def __init__(self):
        pass
    
    def from_file(self, filepath: str) -> dict:
    # Converts a file intoa usable index
        index_dict = dict()
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                key, posting = line.split('|')
                postings_parsed = [[int(p[0]), int(p[1])] for p in (pair.split(',') for pair in posting.split())]
                index_dict[key.rstrip()] = postings_parsed
            
        return index_dict
    
    def to_file(self, index:dict, filepath:str):
    # Writes index to file so it can be later parsed with from_file
        with open(filepath, 'w', encoding='utf-8') as file:
            for key, posting in index.items():
                posting_str = ' '.join(','.join(str(p) for p in pair) for pair in posting)
                file.write('{key} | {posting_str}\n'.format(key=key, posting_str=posting_str))


# filer = IndexFiler()

# d = filer.from_file("E:\\School\\Classes\\Year 4\\Spring\\CS121\\HW3\\Assignment3-SearchEngine\\test.txt")
# print(d)

# d = {'one': [[1, 2], [3, 1]], 'two': [[1, 1], [2, 1]], 'three': [[3, 1], [2, 3]]}

# filer.to_file(d, "E:\\School\\Classes\\Year 4\\Spring\\CS121\\HW3\\Assignment3-SearchEngine\\test.txt")
# c = filer.from_file("E:\\School\\Classes\\Year 4\\Spring\\CS121\\HW3\\Assignment3-SearchEngine\\test.txt")
# print(c)