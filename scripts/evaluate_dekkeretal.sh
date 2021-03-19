#!/bin/bash

# navigate to book-nlp
cd /mnt/book-nlp

mkdir data/output/dekkeretal
mkdir data/tokens/dekkeretal

echo -e "\e[30;48;5;45m INFO: Running BookNLP over Dekker et al. \e[0m"
total_count=$(ls /mnt/data/dekker_et_al/dekker_et_al_original/ -1 | wc -l)
current_count=1
#iterate over original book texts and run BookNLP
for filename in /mnt/data/dekker_et_al/dekker_et_al_original/*.txt; do
    bookname=$(basename -- "$filename")
    echo -e "\e[30;48;5;45m INFO: $current_count/ $total_count: ${bookname%.*} \e[0m"
    ./runjava novels/BookNLP -doc /mnt/data/dekker_et_al/dekker_et_al_original/$bookname -p data/output/dekkeretal/${bookname%.*} -tok data/tokens/dekkeretal/${bookname%.*}.tokens -f
    ((current_count++))
done

mkdir /mnt/Git/results/dekkeretal #todo outcomment in the end
# create empty csv with header for the evaluation results
echo "book_title, precision_booknlp, recall_booknlp, f1_booknlp" >> /mnt/Git/results/dekkeretal/booknlp_dekkeretal_evaluation.csv
echo "book_title, index_list, word_list" >> /mnt/Git/results/dekkeretal/booknlp_dekkeretal_false_positive.csv
echo "book_title, index_list, word_list" >> /mnt/Git/results/dekkeretal/booknlp_dekkeretal_false_negative.csv

echo -e "\e[30;48;5;45m INFO: Comparing BookNLP Litbank annotation to Litbank gold standard \e[0m"
for filename in /mnt/book-nlp/data/tokens/dekkeretal/*; do
    bookname=$(basename -- "$filename")
    echo -e "\e[30;48;5;45m INFO: Evaluating ${bookname%.*} \e[0m"
    python3 /mnt/Git/scripts/booknlp_vs_dekkeretal_gs.py ${bookname%.*}
done
