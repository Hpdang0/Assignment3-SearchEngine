# Assignment3-SearchEngine
Due to the huge size of the corpus given to us, it will be git.ignored. Be sure you download it from canvas and extract it. The DEV folder should be at the root of the project folder.

## Logic Workflow
Parse JSON for Content, Document_ID, URL ---> Store Document_ID:URL ---> Tokenize Content ---> Store into Index ---> Write Indexes to File ---> Combine Indexes to one Index

## Tasklist
- [ ] JSON parsing, Content Extraction, Document ID

Similar to previous assignment, data is condensed into some data structure, this time being JSON. Each entry has 3 fields, a URL, a content, and an encoding. Correctly extract the content to later be tokenized and then store some `Document_ID:URL` for book keeping.
This function should return the contents, and optionally the URL and Document ID depending on how writing to the Document ID mapping is implemented.

- [ ] Tokenizing and Word Processing

Given the extracted content from above, tokenize and process the contents. This can include normalizing, stemming, and removing stop words. 
This should return some list[(Token, Frequency)] that can be iterated and later to be indexed.

- [ ] Index Creation

Given a list of Tokens and some Document ID, add the Document ID to their Tokens. This should be implemented by some HashMap. I'm not too sure, but I think Python's dictionary is already implemented by HashMap. Double check on this.

Note that after some threshold **T**, we must write the Index somehow to a file. This is because in a realistic approach, we cannot store the entire index in memory. After reading up to **T** pages, we should write to a file. At the very end of indexing, we will merge all files written from this part into one big Index file. How this is done depends on how it is written on the first part.

## Notes
It has come to my attention that task 1 is quite underloaded. Whoever's doing task 1 will also be helping out with Word Processing, as that involves stop words, stemming, and other work.