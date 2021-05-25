#!/bin/bash

# Run the following block, only if skipping step evaluate_overlap.sh on purpose (all steps executed there). Remove lines 4 and 41.
: <<'END'
# create overlap directories
mkdir /mnt/data/gold_standard/overlap
mkdir /mnt/data/gold_standard/overlap/litbank
mkdir /mnt/data/gold_standard/overlap/dekker_et_al
mkdir /mnt/data/gold_standard/overlap/original_texts
mkdir /mnt/data/gold_standard/overlap/new_annotation

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

echo -e "\e[30;48;5;45m INFO: Running Flair over overlapping text sections \e[0m"
python3 /mnt/Git/scripts/alt_evaluation/flair_tag_raw_texts.py ${bookname%.*}
END
# create a folder for results
mkdir /mnt/Git/results/overlap_conll

#todo remove those and just catch putput and pipe to correct folder
# create empty csv with header for the evaluation results
echo "book_title, precision_booknlp, recall_booknlp, f1_booknlp" >> /mnt/Git/results/overlap_conll/booknlp_dekkeretal_evaluation.csv
#echo "book_title, index_list, word_list" >> /mnt/Git/results/overlap_conll/booknlp_dekkeretal_false_positive.csv
#echo "book_title, index_list, word_list" >> /mnt/Git/results/overlap_conll/booknlp_dekkeretal_false_negative.csv

echo "book_title, precision_booknlp, recall_booknlp, f1_booknlp" >> /mnt/Git/results/overlap_conll/booknlp_litbank_evaluation.csv
#echo "book_title, index_list, word_list" >> /mnt/Git/results/overlap_conll/booknlp_litbank_false_positive.csv
#echo "book_title, index_list, word_list" >> /mnt/Git/results/overlap_conll/booknlp_litbank_false_negative.csv

# create an empty folders for data
mkdir /mnt/Git/scripts/conll_evaluation/data_conll_format
mkdir /mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_litbank
mkdir /mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_dekkeretal
mkdir /mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_new_person
mkdir /mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_new_perx
mkdir /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_litbank
mkdir /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_dekkeretal
mkdir /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_new_person
mkdir /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_new_perx

# add conll to path in order to add arguments
ln -s /mnt/Git/scripts/conll_evaluation/conlleval.pl /usr/bin/conlleval.pl

# CAUTION: We do not use the flag -r as we are comparing the entities tags of the prefix

echo -e "\e[30;48;5;45m INFO: Evaluating BookNLP using LitBank \e[0m"
python3 /mnt/Git/scripts/conll_evaluation/booknlp_vs_litbank_gs.py
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_litbank/*tsv ; do echo $x ; conlleval.pl -l < $x ; done > /mnt/Git/results/overlap_conll/booknlp_litbank.txt

echo -e "\e[30;48;5;45m INFO: Evaluating BookNLP using Dekker et al. \e[0m"
python3 /mnt/Git/scripts/conll_evaluation/booknlp_vs_dekkeretal_gs.py
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_dekkeretal/*tsv ; do echo $x ; conlleval.pl -l < $x ; done > /mnt/Git/results/overlap_conll/booknlp_dekkeretal.txt

echo -e "\e[30;48;5;45m INFO: Evaluating BookNLP using New gold standard \e[0m"
python3 /mnt/Git/scripts/conll_evaluation/booknlp_vs_new_gs.py
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_new_person/*tsv ; do echo $x ; conlleval.pl -l < $x ; done > /mnt/Git/results/overlap_conll/booknlp_new_person.txt
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_new_perx/*tsv ; do echo $x ; conlleval.pl -l < $x ; done > /mnt/Git/results/overlap_conll/booknlp_new_perx.txt

echo -e "\e[30;48;5;45m INFO: Evaluating Flair using LitBank \e[0m"
python3 /mnt/Git/scripts/conll_evaluation/flair_vs_litbank_gs.py
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_litbank/*tsv ; do echo $x ; conlleval.pl -l < $x ; done > /mnt/Git/results/overlap_conll/flair_litbank.txt
# evaluation with prefixes
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_litbank/*tsv ; do echo $x ; conlleval.pl -r -l < $x ; done > /mnt/Git/results/overlap_conll/flair_litbank_with_prefix.txt

echo -e "\e[30;48;5;45m INFO: Evaluating Flair using Dekker et al. \e[0m"
python3 /mnt/Git/scripts/conll_evaluation/flair_vs_dekkeretal_gs.py
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_dekkeretal/*tsv ; do echo $x ; conlleval.pl -l < $x ; done > /mnt/Git/results/overlap_conll/flair_dekkeretal.txt

echo -e "\e[30;48;5;45m INFO: Evaluating Flair using New gold standard \e[0m"
python3 /mnt/Git/scripts/conll_evaluation/flair_vs_new_gs.py
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_new_person/*tsv ; do echo $x ; conlleval.pl -l < $x ; done > /mnt/Git/results/overlap_conll/flair_new_person.txt
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_new_perx/*tsv ; do echo $x ; conlleval.pl -l < $x ; done > /mnt/Git/results/overlap_conll/flair_new_perx.txt
# evaluation with prefixes
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_new_person/*tsv ; do echo $x ; conlleval.pl -r -l < $x ; done > /mnt/Git/results/overlap_conll/flair_new_person_with_prefix.txt
for x in /mnt/Git/scripts/conll_evaluation/data_conll_format/flair_new_perx/*tsv ; do echo $x ; conlleval.pl -r -l < $x ; done > /mnt/Git/results/overlap_conll/flair_new_perx_with_prefix.txt
