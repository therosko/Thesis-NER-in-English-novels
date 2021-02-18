#!/bin/bash

# run setup script (installs tools and dependencies, gets datasets)
scripts/get_setup.sh


# run tool over Oliver Twist (already available in the repository) if you want to do a test run
#./runjava novels/BookNLP -doc data/originalTexts/dickens.oliver.pg730.txt -printHTML -p data/output/dickens -tok data/tokens/dickens.oliver.tokens -f

#mkdir /mnt/Git/results
# run all litbank books over BookNLP
scripts/evaluate_booknlp.sh

# run all litbank books over Dekker et al.
scripts/evaluate_dekkeretal.sh
