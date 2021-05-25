import pandas as pd
import csv
import os
# import own script
from hyphens import *
from patch_flair_parsing import *
from check_inconsistencies import *

books_mapping = {'AliceInWonderland': '11_alices_adventures_in_wonderland', 
                'DavidCopperfield': '766_david_copperfield', 
                'Dracula': '345_dracula', 
                'Emma': '158_emma',
                'Frankenstein': '84_frankenstein_or_the_modern_prometheus',
                'HuckleberryFinn': '76_adventures_of_huckleberry_finn',
                'MobyDick': '2489_moby_dick',
                'OliverTwist': '730_oliver_twist',
                'PrideAndPrejudice': '1342_pride_and_prejudice',
                'TheCallOfTheWild': '215_the_call_of_the_wild',
                'Ulysses': '4300_ulysses',
                'VanityFair': '599_vanity_fair'}

directory = os.fsencode('/mnt/flair/')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".tsv"): 
        litbank_filepath = "/mnt/data/gold_standard/overlap/litbank/" + books_mapping.get(str(filename.replace('.tsv',''))) + ".tsv"
        flair_filepath = '/mnt/flair/' + filename
        print(filename)
        # read flair
        current_file= pd.read_csv(flair_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1])
        current_file = correct_hyphened(current_file)
        # patch inconsistencies between parsing of flair and gold standards (using LitBank)
        current_file = patch_flair(current_file, filename)
        current_file.loc[~current_file["ner"].isin(['S-PER','I-PER','B-PER','E-PER']), "ner"] = "O"
        # the conll script only accepts IOB format
        current_file["ner"].replace('S-PER', 'B-PER', inplace = True)
        current_file["ner"].replace('E-PER', 'I-PER', inplace = True)
        # read litbank gs
        gs_lb = pd.read_csv(litbank_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"])
        gs_lb.loc[~gs_lb["gs"].isin(['I-PER','B-PER']), "gs"] = "O"
        check_for_inconsistencies_litbank(current_file,gs_lb)
        # merge the two dataframes
        merged_flair_litbank = pd.merge(gs_lb, current_file, left_index=True, right_index=True)
        del merged_flair_litbank['original_word_y']
        #actually it is a space separated value
        merged_flair_litbank.to_csv("/mnt/Git/scripts/conll_evaluation/data_conll_format/flair_litbank/" + str(filename), sep=' ', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, header=False)
