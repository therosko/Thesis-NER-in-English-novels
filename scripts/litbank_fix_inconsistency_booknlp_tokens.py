########################################################################################################
# Summary:
# This script is part of evaluate_litbank.sh for the purpose of comparing BookNLP with the LitBank gold standard
# Some LitBank files contain entities, the format of which is not consistent with the splitting of BookNLP
# We fix those here
########################################################################################################

import os
import csv
import pandas as pd
from hyphens import *

# 110_tess_of_the_durbervilles_a_pure_woman_brat.tsv
current_file = pd.read_csv("/mnt/data/gold_standard/litbank/110_tess_of_the_durbervilles_a_pure_woman_brat.tsv", sep='\t', quoting=csv.QUOTE_NONE) 
current_file.loc[1735,'original_word'] = "'"
current_file.loc[1736,'original_word'] = "Tis"
current_file.to_csv("/mnt/data/gold_standard/litbank/110_tess_of_the_durbervilles_a_pure_woman_brat.tsv", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

# 1661_the_adventures_of_sherlock_holmes_brat.tsv
current_file = pd.read_csv("/mnt/data/gold_standard/litbank/1661_the_adventures_of_sherlock_holmes_brat.tsv", sep='\t', quoting=csv.QUOTE_NONE) 
current_file.loc[1897,'original_word'] = "Eg."
current_file = current_file.drop([1898])
current_file = current_file.reset_index()
del current_file['index']
current_file.to_csv("/mnt/data/gold_standard/litbank/1661_the_adventures_of_sherlock_holmes_brat.tsv", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

# 2005_piccadilly_jim_brat.tsv
current_file = pd.read_csv("/mnt/data/gold_standard/litbank/2005_piccadilly_jim_brat.tsv", sep='\t', quoting=csv.QUOTE_NONE) 
current_file.loc[1636,'original_word'] = ". . ."
current_file = current_file.drop([1637])
current_file = current_file.drop([1638])
current_file = current_file.reset_index()
del current_file['index']
current_file.to_csv("/mnt/data/gold_standard/litbank/2005_piccadilly_jim_brat.tsv", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

# 2084_the_way_of_all_flesh_brat.tsv
current_file = pd.read_csv("/mnt/data/gold_standard/litbank/2084_the_way_of_all_flesh_brat.tsv", sep='\t', quoting=csv.QUOTE_NONE) 
# correct hyphened words from booknlp (note: stanford CoreNLP only splits on "most hyphens")
current_file = correct_hyphened(current_file)
# reset the index to avoid all parts of hyphened words having same index
current_file = current_file.reset_index()
del current_file['index']
current_file.to_csv("/mnt/data/gold_standard/litbank/2084_the_way_of_all_flesh_brat.tsv", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

# 472_the_house_behind_the_cedars_brat.tsv
current_file = pd.read_csv("/mnt/data/gold_standard/litbank/472_the_house_behind_the_cedars_brat.tsv", sep='\t', quoting=csv.QUOTE_NONE) 
current_file.loc[366,'original_word'] = "Ca'lina"
current_file = current_file.drop([367])
current_file = current_file.drop([368])
current_file = current_file.reset_index()
del current_file['index']
current_file.to_csv("/mnt/data/gold_standard/litbank/472_the_house_behind_the_cedars_brat.tsv", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

# 521_the_life_and_adventures_of_robinson_crusoe_brat.tsv
current_file = pd.read_csv("/mnt/data/gold_standard/litbank/521_the_life_and_adventures_of_robinson_crusoe_brat.tsv", sep='\t', quoting=csv.QUOTE_NONE) 
current_file.loc[599,'original_word'] = "viz."
current_file = current_file.drop([600])
current_file = current_file.reset_index()
del current_file['index']
current_file.to_csv("/mnt/data/gold_standard/litbank/521_the_life_and_adventures_of_robinson_crusoe_brat.tsv", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

# 60_the_scarlet_pimpernel_brat.tsv
current_file = pd.read_csv("/mnt/data/gold_standard/litbank/60_the_scarlet_pimpernel_brat.tsv", sep='\t', quoting=csv.QUOTE_NONE) 
current_file.loc[1693,'original_word'] = ". . ."
current_file = current_file.drop([1694])
current_file = current_file.drop([1695])
current_file = current_file.reset_index()
del current_file['index']
current_file.to_csv("/mnt/data/gold_standard/litbank/60_the_scarlet_pimpernel_brat.tsv", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

# crop tokens file, due to value error in irrelevant section
# 514_little_women_brat.tsv 
#df = pd.read_csv("/mnt/book-nlp/data/tokens/litbank/514_little_women.tokens", nrows = 2500, sep='\t')
#df.to_csv("/mnt/book-nlp/data/tokens/litbank/514_little_women.tokens", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)
with open("/mnt/book-nlp/data/tokens/litbank/514_little_women.tokens") as f1:
    lines = f1.readlines()

with open("/mnt/book-nlp/data/tokens/litbank/514_little_women.tokens", 'w') as f2:
    f2.writelines(lines[:2500])