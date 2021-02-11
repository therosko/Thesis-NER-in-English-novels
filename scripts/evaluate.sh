#!/bin/bash

# navigate to book-nlp
cd /mnt/book-nlp
echo "Running BookNLP"
# run tool over Oliver Twist (already available in the repository)
./runjava novels/BookNLP -doc data/originalTexts/dickens.oliver.pg730.txt -printHTML -p data/output/dickens -tok data/tokens/dickens.oliver.tokens -f
# run on litbank
# evelina works
./runjava novels/BookNLP -doc /mnt/data/litbank/entities/brat/6053_evelina_or_the_history_of_a_young_ladys_entrance_into_the_world_brat.txt -p data/output/evelina -tok data/tokens/evelina.tokens -f
# huckleberry works
./runjava novels/BookNLP -doc /mnt/data/litbank/original/76_adventures_of_huckleberry_finn.txt -p data/output/huckleberry -tok data/tokens/huckleberry.tokens -f

./runjava novels/BookNLP -doc /mnt/data/litbank/original/18581_adrift_in_new_york_tom_and_florence_braving_the_world.txt -printHTML -p data/output/ -tok data/tokens/76_adventures_of_huckleberry_finn.tokens -f
./runjava novels/BookNLP -doc /mnt/data/litbank/original/1661_the_adventures_of_sherlock_holmes_brat.txt -printHTML -p data/output/sherlock -tok data/tokens/sherlock.tokens -f
./runjava novels/BookNLP -doc /mnt/data/litbank/entities/brat/11_alices_adventures_in_wonderland_brat.txt -p data/output/alice2 -tok data/tokens/alice2.tokens -f

echo "Comparing BookNLP to gold standard"
python3 /mnt/Git/scripts/booknlp_vs_litbank_gs.py