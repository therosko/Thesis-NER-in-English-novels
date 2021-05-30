#!/bin/bash

# run setup script (installs tools and dependencies, gets datasets)
scripts/get_setup.sh


# run tool over Oliver Twist (already available in the repository) if you want to do a test run
#./runjava novels/BookNLP -doc data/originalTexts/dickens.oliver.pg730.txt -printHTML -p data/output/dickens -tok data/tokens/dickens.oliver.tokens -f

#mkdir /mnt/Git/results
# run all LitBank books over BookNLP
scripts/initial_evaluation/evaluate_booknlp.sh

# run all Dekker et al. over BookNLP
scripts/initial_evaluation/evaluate_dekkeretal.sh

# with own script evaluate the overlaping sections of LitBank, Dekker et al., and new gold standard using BookNLP and Flair
scripts/alt_evaluation/evaluate_overlap.sh

# with CoNLL script evaluate the overlaping sections of LitBank, Dekker et al., and new gold standard using BookNLP and Flair
scripts/conll_evaluation/evaluate_overlap_conll.sh

# calculate interannotator agreement
mkdir /mnt/Git/results/interannotator_agreement
python3 /mnt/Git/scripts/interannotator_agreement.py > /mnt/Git/results/interannotator_agreement/results.txt