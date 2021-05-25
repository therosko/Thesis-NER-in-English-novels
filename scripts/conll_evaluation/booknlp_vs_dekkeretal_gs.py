# BookNLP Dekker

import pandas as pd
import csv

import os
# import own script
from hyphens import *
from check_inconsistencies import *

directory = os.fsencode('/mnt/book-nlp/data/tokens/overlap/')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".tokens"):
        booknlp_filepath = "/mnt/book-nlp/data/tokens/overlap/" + filename
        dekker_filepath = "/mnt/data/gold_standard/overlap/dekker_et_al/" + str(filename.replace('.tokens','.gs'))
        #####################################
        # get output file BookNLP
        current_file = pd.read_csv(booknlp_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=["originalWord","ner"])
        current_file = current_file.rename(columns={"originalWord": "original_word", "ner": "booknlp"})
        # alternatively convert all PERSON to PER
        current_file["booknlp"].replace('PERSON', 'I-PERSON', inplace = True)
        # replace rest of entities with O
        current_file.loc[~current_file["booknlp"].isin(['I-PERSON']), "booknlp"] = "O"
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
        # get gold standard - Dekker
        gs_d = pd.read_csv(dekker_filepath, sep=' ', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"])
        gs_d = correct_hyphened(gs_d)
        gs_d.loc[~gs_d["gs"].isin(['I-PERSON']), "gs"] = "O"
        check_for_inconsistencies_dekker(current_file,gs_d)
        # merge the two dataframes
        merged_df = pd.merge(gs_d, current_file, left_index=True, right_index=True)
        del merged_df['original_word_y']
        #actually it is a space separated value
        merged_df.to_csv("/mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_dekkeretal/" + str(filename.replace('.tokens','.tsv')), sep=' ', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, header=False)