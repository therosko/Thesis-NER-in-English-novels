#!/bin/bash

echo -e "\e[30;48;5;45m INFO: Comparing BookNLP overlap annotation to Litbank gold standard and to Dekker et al. gold standard \e[0m"
for filename in /mnt/book-nlp/data/tokens/overlap/*; do
    bookname=$(basename -- "$filename")
    echo -e "\e[30;48;5;45m INFO: Evaluating ${bookname%.*} \e[0m"
    python3 /mnt/Git/scripts/booknlp_vs_overlap.py ${bookname%.*}
done