#!/bin/bash

# navigate to book-nlp
cd /mnt/book-nlp

mkdir data/output/dekkeretal
mkdir data/tokens/dekkeretal

echo -e "\e[30;48;5;45m INFO: Running BookNLP over Dekker et al. \e[0m"
total_count=$(ls /mnt/data/dekker_et_al/dekker_et_al_original/part1/ -1 | wc -l)
current_count=1
#iterate over original book texts and run BookNLP
for filename in /mnt/data/dekker_et_al/dekker_et_al_original/part1/*.txt; do
    bookname=$(basename -- "$filename")
    echo -e "\e[30;48;5;45m INFO: $current_count/ $total_count: ${bookname%.*} \e[0m"
    ./runjava novels/BookNLP -doc /mnt/data/dekker_et_al/dekker_et_al_original/part1/$bookname -p data/output/dekkeretal/${bookname%.*} -tok data/tokens/dekkeretal/${bookname%.*}.tokens -f
    ((current_count++))
done