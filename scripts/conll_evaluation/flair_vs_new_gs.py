import pandas as pd
import csv
import os
# import own script
from hyphens import *
from patch_flair_parsing import *
from check_inconsistencies import *


directory = os.fsencode('/mnt/flair/')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".tsv"): 
        new_filepath = "/mnt/Git/annotation/gs/" + str(filename.replace('.tsv','')) + "_final.tsv"
        flair_filepath = '/mnt/flair/' + filename
        # read flair
        current_file= pd.read_csv(flair_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1])
        current_file = correct_hyphened(current_file)
        # patch inconsistencies between parsing of flair and gold standards (using LitBank)
        current_file = patch_flair(current_file, filename)
        current_file.loc[~current_file["ner"].isin(['S-PER','I-PER','B-PER','E-PER']), "ner"] = "O"
        # the conll script only accepts IOB format
        current_file["ner"].replace('S-PER', 'B-PER', inplace = True)
        current_file["ner"].replace('E-PER', 'I-PER', inplace = True)
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
        merged_flair_new_person = pd.merge(gs_new_conll, current_file, left_index=True, right_index=True)
        del merged_flair_new_person['original_word_y']
        #actually it is a space separated value
        merged_flair_new_person.to_csv("/mnt/Git/scripts/conll_evaluation/data_conll_format/flair_new_person/" + str(filename), sep=' ', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, header=False)
        ###########################################
        ###### second evaluation with PERSON and PERX labels
        check_for_inconsistencies_new(current_file,gs_new)
        # merge the two dataframes
        merged_flair_new_perx = pd.merge(gs_new, current_file, left_index=True, right_index=True)
        del merged_flair_new_perx['original_word_y']
        #actually it is a space separated value
        merged_flair_new_perx.to_csv("/mnt/Git/scripts/conll_evaluation/data_conll_format/flair_new_perx/" + str(filename), sep=' ', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, header=False)

