# BookNLP New (both)

import pandas as pd
import csv

import os
# import own script
from hyphens import *
from calculate_metrics import *
from check_inconsistencies import *

directory = os.fsencode('/mnt/book-nlp/data/tokens/overlap/')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".tokens"): 
        new_filepath = "/mnt/Git/annotation/gs/" + str(filename.replace('.tokens','')) + "_final.tsv"
        booknlp_filepath = '/mnt/book-nlp/data/tokens/overlap/' + filename
        # read booknlp
        current_file= pd.read_csv(booknlp_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=["originalWord","ner"])
        current_file = current_file.rename(columns={"originalWord": "original_word", "ner": "booknlp"})
        # alternatively convert all PERSON to PER
        current_file["booknlp"].replace('PERSON', 'I-PER', inplace = True)
        # replace rest of entities with O
        current_file.loc[~current_file["booknlp"].isin(['I-PER']), "booknlp"] = "O"
        # correct hyphened words from booknlp (note: stanford CoreNLP only splits on "most hyphens")
        current_file = correct_hyphened(current_file)
        current_file = current_file.reset_index(drop=True)
        # remove chapter separation with stars"
        if filename == "AliceInWonderland.tokens":
            current_file = current_file.drop(current_file.index[1911:1931])
            current_file = current_file.reset_index(drop=True)
        # read new annotated dataset
        gs_new = pd.read_csv(new_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1,2])
        # extract only PERSON labels (following CoNLL-2003 guidelines)
        gs_new_conll = gs_new.copy()
        gs_new_conll['gs'] = "O"
        for item in ['B-PERSON', 'I-PERSON']:
            gs_new_conll['gs'][gs_new_conll['ner'].str.contains(item)] = item
            gs_new_conll['gs'][gs_new_conll['m_ner'].str.contains(item)] = item
        gs_new_conll.loc[gs_new_conll["gs"].isin(['B-PERSON']), "gs"] = "B-PER"
        gs_new_conll.loc[gs_new_conll["gs"].isin(['I-PERSON']), "gs"] = "I-PER"
        del gs_new_conll['ner']
        del gs_new_conll['m_ner']
        # extract to a new column both labels person and perx (extension, taken from the LitBank annotation guidelines)
        gs_new['gs'] = "O" 
        for item in ['B-PERSON', 'I-PERSON','B-PERX','I-PERX']:
            gs_new['gs'][gs_new['ner'].str.contains(item)] = item
            gs_new['gs'][gs_new['m_ner'].str.contains(item)] = item
        gs_new.loc[gs_new["gs"].isin(['B-PERSON','B-PERX']), "gs"] = "B-PER"
        gs_new.loc[gs_new["gs"].isin(['I-PERSON','I-PERX']), "gs"] = "I-PER"
        del gs_new['ner']
        del gs_new['m_ner']
        ###########################################
        ##### first evaluation only with PERSON label
        check_for_inconsistencies_new(current_file,gs_new_conll)
        # merge the two dataframes
        merged_booknlp_person = pd.merge(gs_new_conll, current_file, left_index=True, right_index=True)
        del merged_booknlp_person['original_word_y']
        #actually it is a space separated value
        merged_booknlp_person.to_csv("/mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_new_person/" + str(filename.replace('.tokens','.tsv')), sep=' ', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, header=False)
        ###########################################
        ###### second evaluation with PERSON and PERX labels
        check_for_inconsistencies_new(current_file,gs_new)
        # merge the two dataframes
        merged_booknlp_perx = pd.merge(gs_new, current_file, left_index=True, right_index=True)
        del merged_booknlp_perx['original_word_y']
        #actually it is a space separated value
        merged_booknlp_perx.to_csv("/mnt/Git/scripts/conll_evaluation/data_conll_format/booknlp_new_perx/" + str(filename.replace('.tokens','.tsv')), sep=' ', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, header=False)

