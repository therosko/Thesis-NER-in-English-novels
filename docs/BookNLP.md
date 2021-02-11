### [BookNLP](https://github.com/dbamman/book-nlp)

`./runjava novels/BookNLP -doc data/originalTexts/dickens.oliver.pg730.txt -printHTML -p data/output/dickens -tok data/tokens/dickens.oliver.tokens -f`

`./runjava novels/BookNLP -doc data/litbank/original/76_adventures_of_huckleberry_finn.txt -printHTML -p data/output/ -tok data/tokens/76_adventures_of_huckleberry_finn.tokens -f`

Flags:

* -doc : original text to process, *those are plain texts in format `.txt`*
* -tok : file path to save processed tokens to (or read them from, if it already exists) 

BookNLP recognises the following NER tags/types **(PERSON, NUMBER, DATE, DURATION, MISC, TIME, LOCATION, ORDINAL, MONEY, ORGANIZATION, SET, O)**

Column meaning in `.token` files:
1. Paragraph id
2. Sentence id
3. Token id
4. Byte start
5. Byte end
6. Whitespace following the token (useful for pretty-printing the original text)
7. Syntactic head id (-1 for the sentence root)
8. Original token
9. Normalized token (for quotes etc.)
10. Lemma
11. Penn Treebank POS tag
12. NER tag (PERSON, NUMBER, DATE, DURATION, MISC, TIME, LOCATION, ORDINAL, MONEY, ORGANIZATION, SET, O)
13. Stanford basic dependency label
14. Quotation label (begin quote, inside quote, outside quote)
15. Character id (all coreferent tokens share the same character id)
16. Supersense tag (https://wordnet.princeton.edu/documentation/lexnames5wn)