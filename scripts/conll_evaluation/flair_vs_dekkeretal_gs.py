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
        dekker_filepath = "/mnt/data/gold_standard/overlap/dekker_et_al/" + str(filename.replace('.tsv','')) + ".gs"
        flair_filepath = '/mnt/flair/' + filename
        # read Flair
        current_file= pd.read_csv(flair_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1])
        current_file = correct_hyphened(current_file)
        # patch inconsistencies between parsing of flair and gold standards (using LitBank)
        current_file = patch_flair(current_file, filename)
        current_file.loc[~current_file["ner"].isin(['S-PER','I-PER','B-PER','E-PER']), "ner"] = "O"
        # the conll script only accepts IOB format
        current_file["ner"].replace('S-PER', 'B-PER', inplace = True)
        current_file["ner"].replace('E-PER', 'I-PER', inplace = True)
        # read Dekker et al. gs
        gs_d = pd.read_csv(dekker_filepath, sep=' ', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"])
        gs_d = correct_hyphened(gs_d)
        gs_d.loc[~gs_d["gs"].isin(['I-PERSON']), "gs"] = "O"
        gs_d["gs"].replace('I-PERSON', 'I-PER', inplace = True)
        check_for_inconsistencies_dekker(current_file,gs_d)
        # merge the two dataframes
        merged_flair_dekkeretal = pd.merge(gs_d, current_file, left_index=True, right_index=True)
        del merged_flair_dekkeretal['original_word_y']
        #actually it is a space separated value
        merged_flair_dekkeretal.to_csv("/mnt/Git/scripts/conll_evaluation/data_conll_format/flair_dekkeretal/" + str(filename), sep=' ', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, header=False)
