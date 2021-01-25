### [BookNLP](https://github.com/dbamman/book-nlp)

`./runjava novels/BookNLP -doc data/originalTexts/dickens.oliver.pg730.txt -printHTML -p data/output/dickens -tok data/tokens/dickens.oliver.tokens -f`

Flags:

* -doc : original text to process, *those are plain texts in format `.txt`*
* -tok : file path to save processed tokens to (or read them from, if it already exists) 

BookNLP recognises the following NER tags/types **(PERSON, NUMBER, DATE, DURATION, MISC, TIME, LOCATION, ORDINAL, MONEY, ORGANIZATION, SET, O)**
