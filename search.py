from collections import defaultdict
import indexfiler
import math

QWEIGHT_H02 = 4                                 #1
QWEIGHT_H36 = 3                                 #2
QWEIGHT_BOLD = 1                                #3
QWEIGHT_HYPERLINK = 1                           #4
QWEIGHT_ITALICIZED = .6                         #5
QWEIGHT_LIST = .9                               #6
QWEIGHT_TITLE = 10                              #7

class Search():
    def __init__(self, index_path: str, ids_path: str, max_docID: int):
        self.index_path = index_path
        self.ids_path = ids_path
        self.max_docID = max_docID

    def ranking(self, queries, intersecting_docs, index_dict):
        # we can change this ranking func later
        weights = defaultdict(int)

        # idf is essentially the raw number of occurrences at this point
        mode_map = {
            '1':QWEIGHT_H02,
            '2':QWEIGHT_H36,
            '3':QWEIGHT_BOLD,
            '4':QWEIGHT_HYPERLINK,
            '5':QWEIGHT_ITALICIZED,
            '6':QWEIGHT_LIST,
            '7':QWEIGHT_TITLE
        }
        
        for q in queries:
            for x in index_dict[q]: # for each pair (25239, 1) docID and number of times that token appears in the doc
                if x[0] in intersecting_docs: # x[1] is the term freq for that document
                    weights[x[0]] += self.tf(x[1], x[2], mode_map) * self.idf(len(index_dict[q]), self.max_docID) # weight[this doc ID] += by the term freq (in this doc) * idf
                    print(x)
        print('weights', sorted(weights.items(), key = lambda x: x[1], reverse = True))
        return sorted(weights.keys(), key = lambda x: weights[x], reverse = True) # largest to smallest

    def tf(self, freq, mode, mode_map):
        weight = 0
        for m in mode:
            freq -= 1
            weight += mode_map[m]
        weight += freq
        return math.log(1 + weight, 10)

    def idf(self, doc_count, max_docID):
        return math.log( (max_docID / (doc_count)) , 10)

    def search(self, tokens: [str]) -> [str]:
        # type r: list of urls
        #result_list = []
        if len(tokens) == 0:
            return None

        filer = indexfiler.IndexFiler()
        index_dict = dict()
        # with open("final.index", 'r', encoding='utf-8') as file:
        #     for line in file:
        #         key, posting = line.split('|')
        #         postings_parsed = [[int(p[0]), int(p[1])] for p in (pair.split(',') for pair in posting.split())]
        #         index_dict[key.rstrip()] = postings_parsed
        lines = []

        for token in tokens:
            line = filer.bsearch_file('final.index', token)
            if line is not None:
                lines.append(line)
            
        if len(lines) == 0:
            return None

        for line in lines:
            key, posting = line.split('|')
            postings_parsed = [[int(p[0]), int(p[1]), str(p[2])] for p in (pair.split(',') for pair in posting.split())]
            index_dict[key.rstrip()] = postings_parsed
        
        sorted_tokens = sorted(tokens, key = lambda token: len(index_dict[token])) # sorted by amount of associated docIDs
        #intersection_docs = set()
        new_list = set()
        intersection_docs = set([tup[0] for tup in index_dict[sorted_tokens.pop(0)]])
                                                            # ^ take out the first token

        for token in sorted_tokens: # going from least associated docIDs to most
            for x in index_dict[token]: # for each pair associated with the token
                if x[0] in intersection_docs: # if the doc id is in the intersection_docs, we should add it
                    new_list.add(x[0])
            intersection_docs.intersection(new_list) # first_list should get smaller and smaller

        # basically, ^ the intersection_docs should get smaller because we intersect it with things that are already in
        # it but not necessarily everything in it

        results_scored = self.ranking(tokens, intersection_docs, index_dict) # should get a list of sorted queries
        # print(results_scored)

        results_scored = results_scored[:5]
        doc_ids = dict()
        with open("final.ids", 'r', encoding='utf-8') as file:
            for line in file:
                id, url = line.split()
                doc_ids[int(id)] = url
        
        final_answer = []
        for num in results_scored:
            final_answer.append(doc_ids[num])
        return final_answer
