from collections import defaultdict
import indexfiler
import math

class Search():
    def __init__(self, index_path: str, ids_path: str):
        self.index_path = index_path
        self.ids_path = ids_path

    def ranking(self, queries, intersecting_docs, index_dict, max_docID):
        # we can change this ranking func later
        weights = defaultdict(int)

        # idf is essentially the raw number of occurrences at this point
        
        for q in queries:
            for x in index_dict[q]: # for each pair (25239, 1) docID and number of times that token appears in the doc
                if x[0] in intersecting_docs: # x[1] is the term freq for that document
                    weights[x[0]] += self.tf(x[1]) * self.idf(len(index_dict[q]), max_docID) # weight[this doc ID] += by the term freq (in this doc) * idf
        
        return sorted(weights.keys(), key = lambda x: weights[x], reverse = True) # largest to smallest

    def tf(self, raw_count):
        return math.log(1 + raw_count, 10)

    def idf(self, doc_count, max_docID):
        return math.log( (max_docID / (doc_count)) , 10)

    def search(self, tokens: [str]) -> [str]:
        # type r: list of urls
        #result_list = []
        filer = indexfiler.IndexFiler()
        index_dict = dict()
        # with open("final.index", 'r', encoding='utf-8') as file:
        #     for line in file:
        #         key, posting = line.split('|')
        #         postings_parsed = [[int(p[0]), int(p[1])] for p in (pair.split(',') for pair in posting.split())]
        #         index_dict[key.rstrip()] = postings_parsed
        lines = []

        for token in tokens:
            lines.append(filer.bsearch_file('final.index', token))

        for line in lines:
            key, posting = line.split(' | ')
            postings_parsed = [[int(p[0]), int(p[1])] for p in (pair.split(',') for pair in posting.split())]
            index_dict[key.rstrip()] = postings_parsed
        
        sorted_tokens = sorted(tokens, key = lambda token: len(index_dict[token])) # sorted by amount of associated docIDs
        #intersection_docs = set()
        new_list = set()
        intersection_docs = set([tup[0] for tup in index_dict[sorted_tokens.pop(0)]])
                                                            # ^ take out the first token

        max_docID = max(intersection_docs) # this is the N in the idf equation

        # idf = defaultdict(int) # inverse document frequency (to be passed to the ranking helper function)

        # for token in sorted_tokens:
        #     for x in index_dict[token]:
        #         idf[token] += x[1]       # this is essentially the raw frequency

        for token in sorted_tokens: # going from least associated docIDs to most
            for x in index_dict[token]: # for each pair associated with the token
                if x[0] in intersection_docs: # if the doc id is in the intersection_docs, we should add it
                    new_list.add(x[0])
            intersection_docs.intersection(new_list) # first_list should get smaller and smaller

        # basically, ^ the intersection_docs should get smaller because we intersect it with things that are already in
        # it but not necessarily everything in it

        results_scored = self.ranking(tokens, intersection_docs, index_dict, max_docID) # should get a list of sorted queries

        results_scored = results_scored[:5]
        doc_ids = dict()
        with open("tmp_0.ids", 'r', encoding='utf-8') as file:
            for line in file:
                lis = line.split(' ', 1)
                doc_ids[int(lis[0])] = lis[1]
        
        final_answer = []
        for num in results_scored:
            final_answer.append(doc_ids[num])
        return final_answer
