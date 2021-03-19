#!/bin/bash

# compare the "old" repository for litbank to the most recent one

mkdir /mnt/data/old_litbank
cd /mnt/data/old_litbank
# "old" repository
git clone https://github.com/dbamman/NAACL2019-literary-entities.git .

total_count=$(ls /mnt/data/litbank/entities/tsv/*.tsv -1 | wc -l)
current_count=1
for filename in /mnt/data/litbank/entities/tsv/*.tsv; do
    bookname=$(basename -- "$filename")
    echo -e "\e[30;48;5;45m INFO: $current_count/ $total_count: ${bookname%.*} \e[0m"
    diff /mnt/data/litbank/entities/tsv/$bookname /mnt/data/old_litbank/litbank/entities/tsv/$bookname
    ((current_count++))
done