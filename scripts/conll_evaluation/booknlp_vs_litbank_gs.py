# BookNLP LitBank

import pandas as pd
import csv

import os
# import own script
from hyphens import *
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

directory = os.fsencode('/mnt/book-nlp/data/tokens/overlap/')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".tokens"):
        booknlp_filepath = "/mnt/book-nlp/data/tokens/overlap/" + filename
        litbank_filepath = "/mnt/data/gold_standard/overlap/litbank/" + books_mapping.get(str(filename.replace('.tokens',''))) + ".tsv"
        #####################################
        # get output file BookNLP
        current_file = pd.read_csv(booknlp_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=["originalWord","ner"])
        current_file = current_file.rename(columns={"originalWord": "original_word", "ner": "booknlp"})
        # alternatively convert all PERSON to PER
        current_file["booknlp"].replace('PERSON', 'I-PER', inplace = True)
        # replace rest of entities with O
        current_file.loc[~current_file["booknlp"].isin(['I-PER']), "booknlp"] = "O"
        # correct hyphened words from booknlp (note: stanford CoreNLP only splits on "most hyphens")
        current_file = correct_hyphened(current_file)
        # reset the index to avoid all parts of hyphened words having same index
        current_file = current_file.reset_index()
        del current_file['index']
        # remove chapter separation with stars"
        if str(filename) == "AliceInWonderland.tokens":
            current_file = current_file.drop(current_file.index[1911:1931])
            current_file = current_file.reset_index(drop=True)
        #####################################
        # get gold standard - Litbank
        gs_lb = pd.read_csv(litbank_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"])
        gs_lb.loc[~gs_lb["gs"].isin(['I-PER','B-PER']), "gs"] = "O"
        check_for_inconsistencies_litbank(current_file, gs_lb)
        # merge the two dataframes
        merged_df = pd.merge(gs_lb, current_file, left_index=True, right_index=True)
        del merged_df['original_word_y']
        #actually it is a space separated value
        merged_df.to_csv("/mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_litbank/" + str(filename.replace('.tokens','.tsv')), sep=' ', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, header=False)
