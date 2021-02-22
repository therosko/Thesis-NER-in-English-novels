#!/bin/bash

# run setup script (installs tools and dependencies, gets datasets)
scripts/get_setup.sh


# run tool over Oliver Twist (already available in the repository) if you want to do a test run
#./runjava novels/BookNLP -doc data/originalTexts/dickens.oliver.pg730.txt -printHTML -p data/output/dickens -tok data/tokens/dickens.oliver.tokens -f

#mkdir /mnt/Git/results
# run all LitBank books over BookNLP
scripts/evaluate_booknlp.sh

# run all Dekker et al. over BookNLP
scripts/evaluate_dekkeretal.sh

# run all overlapping between Dekker et al. and LitBank over BookNLP
scripts/evaluate_overlap.sh
