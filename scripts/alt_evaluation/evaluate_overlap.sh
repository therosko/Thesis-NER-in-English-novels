#!/bin/bash

# create overlap directories
mkdir /mnt/data/gold_standard/overlap
mkdir /mnt/data/gold_standard/overlap/litbank
mkdir /mnt/data/gold_standard/overlap/dekker_et_al
mkdir /mnt/data/gold_standard/overlap/original_texts
mkdir /mnt/data/gold_standard/overlap/new_annotation


# get overlap #todo currently manually extracted
# python3 overlap_litbank_dekkeretal.py
# copy manually created overlapping files to the data folder
cp /mnt/Git/data_overlap_manual_collection/dekker_et_al/* /mnt/data/gold_standard/overlap/dekker_et_al/
cp /mnt/Git/data_overlap_manual_collection/litbank/* /mnt/data/gold_standard/overlap/litbank/
cp /mnt/Git/data_overlap_manual_collection/original_texts/* /mnt/data/gold_standard/overlap/original_texts/
cp /mnt/Git/annotation/* /mnt/data/gold_standard/overlap/new_annotation/


####################################
#########     BookNLP      #########
####################################
echo -e "\e[30;48;5;45m INFO: Beginning with BookNLP \e[0m"
cd /mnt/book-nlp
mkdir data/output/overlap
mkdir data/tokens/overlap

echo -e "\e[30;48;5;45m INFO: Running BookNLP over overlapping text sections \e[0m"
total_count=$(ls /mnt/data/gold_standard/overlap/original_texts/ -1 | wc -l)
current_count=1
#iterate over original book texts and run BookNLP
for filename in /mnt/data/gold_standard/overlap/original_texts/*.txt; do
    bookname=$(basename -- "$filename")
    echo -e "\e[30;48;5;45m INFO: $current_count/ $total_count: ${bookname%.*} \e[0m"
    ./runjava novels/BookNLP -doc /mnt/data/gold_standard/overlap/original_texts/$bookname -p data/output/overlap/${bookname%.*} -tok data/tokens/overlap/${bookname%.*}.tokens -f
    ((current_count++))
done

mkdir /mnt/Git/results/overlap 
# create empty csv with header for the evaluation results
echo "book_title, precision_booknlp, recall_booknlp, f1_booknlp" >> /mnt/Git/results/overlap/booknlp_dekkeretal_evaluation.csv
echo "book_title, index_list, word_list" >> /mnt/Git/results/overlap/booknlp_dekkeretal_false_positive.csv
echo "book_title, index_list, word_list" >> /mnt/Git/results/overlap/booknlp_dekkeretal_false_negative.csv

echo "book_title, precision_booknlp, recall_booknlp, f1_booknlp" >> /mnt/Git/results/overlap/booknlp_litbank_evaluation.csv
echo "book_title, index_list, word_list" >> /mnt/Git/results/overlap/booknlp_litbank_false_positive.csv
echo "book_title, index_list, word_list" >> /mnt/Git/results/overlap/booknlp_litbank_false_negative.csv

echo -e "\e[30;48;5;45m INFO: Comparing BookNLP overlap annotation to Litbank, Dekker et al. and new gold standard \e[0m"
for filename in /mnt/book-nlp/data/tokens/overlap/*; do
    bookname=$(basename -- "$filename")
    echo -e "\e[30;48;5;45m INFO: Evaluating ${bookname%.*} \e[0m"
    python3 /mnt/Git/scripts/alt_evaluation/booknlp_vs_overlap.py ${bookname%.*}
done

echo -e "\e[30;48;5;45m INFO: Evaluating BookNLP using New gold standard \e[0m"
python3 /mnt/Git/scripts/alt_evaluation/booknlp_vs_new_gs.py

####################################
#########      Flair       #########
####################################


echo -e "\e[30;48;5;45m INFO: Running Flair over overlapping text sections \e[0m"
python3 /mnt/Git/scripts/alt_evaluation/flair_tag_raw_texts.py ${bookname%.*}

echo -e "\e[30;48;5;45m INFO: Evaluating Flair using Dekker et al. \e[0m"
python3 /mnt/Git/scripts/alt_evaluation/flair_vs_dekkeretal_gs.py

echo -e "\e[30;48;5;45m INFO: Evaluating Flair using LitBank \e[0m"
python3 /mnt/Git/scripts/alt_evaluation/flair_vs_litbank_gs.py

echo -e "\e[30;48;5;45m INFO: Evaluating Flair using New gold standard \e[0m"
python3 /mnt/Git/scripts/alt_evaluation/flair_vs_new_gs.py