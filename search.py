

class Search():
    def __init__(self, index_path: str, ids_path: str):
        self.index_path = index_path
        self.ids_path = ids_path

    def search(self, tokens: [str]) -> [str]:
        # type r: list of urls
        result_list = []
        index_dict = dict()
        with open("final.index", 'r', encoding='utf-8') as file:
            for line in file:
                key, posting = line.split('|')
                postings_parsed = [[int(p[0]), int(p[1])] for p in (pair.split(',') for pair in posting.split())]
                index_dict[key.rstrip()] = postings_parsed
            for token in tokens:
                list = []
                list.append(token)
                for x in index_dict[token]:
                    list.append(x[0])                
                result_list.append(list)
        return result_list