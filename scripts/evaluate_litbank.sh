#!/bin/bash

# navigate to book-nlp
cd /mnt/book-nlp

mkdir data/output/litbank
mkdir data/tokens/litbank

#TODO outcomment in the end
: <<'END'
echo -e "\e[30;48;5;45m INFO: Running BookNLP over Litbank \e[0m"
total_count=$(ls /mnt/data/litbank/original/ -1 | wc -l)
current_count=1
#iterate over original book texts and run BookNLP
for filename in /mnt/data/litbank/original/*.txt; do
    bookname=$(basename -- "$filename")
    echo -e "\e[30;48;5;45m INFO: $current_count/ $total_count: ${bookname%.*} \e[0m"
    ./runjava novels/BookNLP -doc /mnt/data/litbank/original/$bookname -p data/output/litbank/${bookname%.*} -tok data/tokens/litbank/${bookname%.*}.tokens -f
    ((current_count++))
done
END

#mkdir /mnt/Git/results/litbank
# create empty csv with header for the evaluation results
echo "book_title, precision_booknlp, recall_booknlp, f1_booknlp" >> /mnt/Git/results/litbank/booknlp_litbank_evaluation.csv
echo "book_title, index_list, word_list" >> /mnt/Git/results/litbank/booknlp_litbank_false_positive.csv
echo "book_title, index_list, word_list" >> /mnt/Git/results/litbank/booknlp_litbank_false_negative.csv

echo -e "\e[30;48;5;45m INFO: Comparing BookNLP Litbank annotation to Litbank gold standard \e[0m"
for filename in /mnt/book-nlp/data/tokens/litbank/*.tokens; do
    bookname=$(basename -- "$filename")
    echo -e "\e[30;48;5;45m INFO: Evaluating ${bookname%.*} \e[0m"
    python3 /mnt/Git/scripts/booknlp_vs_litbank_gs.py ${bookname%.*}
done
