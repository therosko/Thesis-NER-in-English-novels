

####################################################################################################################################################
# Flair Dekker

import pandas as pd
import os
import csv
# import own script
from hyphens import *
from patch_flair_parsing import * 
from calculate_metrics import *

def check_for_inconsistencies_dekker(current_file,gs_d):
    try:
        for index, word, ner in current_file.itertuples(index=True):
            if word != gs_d["original_word"].loc[index]:
                if (word == '(' and gs_d["original_word"].loc[index] == '-LRB-') or (word == ')' and gs_d["original_word"].loc[index] == '-RRB-') or (word == '[' and gs_d["original_word"].loc[index] == '-LSB-') or (word == ']' and gs_d["original_word"].loc[index] == '-RSB-'):
                    pass
                elif (word in ["‘","-","' \" '",'"',"“",'-',"”","'",",","’"]) and (gs_d["original_word"].loc[index] in ['`',"``","--","''","'",'--']):
                    pass
                elif (word == "—") and (gs_d["original_word"].loc[index] == '--'):
                    #print("Warning ", index, " '", word, "' in current is not the same as '", gs_d["original_word"].loc[index], "'in gs")
                    pass
                elif (word == "'t" and gs_d["original_word"].loc[index] == "`") or (word == "is" and gs_d["original_word"].loc[index] == "tis") or (word == "honorable" and gs_d["original_word"].loc[index] == "honourable") or (word == "honor" and gs_d["original_word"].loc[index] == "honour"):
                    pass
                elif (re.match(r"[a-zA-Z]*’[a-zA-Z]+", word)) and (re.match(r"[a-zA-Z]*'[a-zA-Z]+", gs_d["original_word"].loc[index])):
                    pass
                elif (re.match(r"[a-zA-Z]*'[a-zA-Z]+", word)) and (re.match(r"[a-zA-Z]*’[a-zA-Z]+", gs_d["original_word"].loc[index])):
                    pass
                else:
                    print("Position ", index, " '", word, "' in current is not the same as '", gs_d["original_word"].loc[index], "'in gs")
                    print(current_file.iloc[index-1:index+4])
                    print(gs_d.iloc[index-1:index+4])
                    break
    #Note: some original texts are longer than the annotated files, we stop the comparisson at that length
    except KeyError:
        print("Reached end of annotated file. Cropped currect_file.")
        print("Last word ", word, " in line ", index)
        current_file = current_file.truncate(after=index-1)
        pass

filename = "Dracula.tsv"
dekker_filepath = "/mnt/data/gold_standard/overlap/dekker_et_al/" + str(filename.replace('.tsv','')) + ".gs"
flair_filepath = '/mnt/flair/' + filename
print(filename)
# read Flair
current_file= pd.read_csv(flair_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1])
current_file = correct_hyphened(current_file)
# patch inconsistencies between parsing of flair and gold standards (using LitBank)
current_file = patch_flair(current_file, filename)
current_file.loc[~current_file["ner"].isin(['S-PER','I-PER','B-PER','E-PER']), "ner"] = "O"
# read Dekker et al. gs
gs_d = pd.read_csv(dekker_filepath, sep=' ', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"])
gs_d = correct_hyphened(gs_d)
gs_d.loc[~gs_d["gs"].isin(['I-PERSON']), "gs"] = "O"
check_for_inconsistencies_dekker(current_file,gs_d)
# merge the two dataframes
merged_flair_dekkeretal = pd.merge(gs_d, current_file, left_index=True, right_index=True)
del merged_flair_dekkeretal['original_word_y']

merged_flair_dekkeretal.to_csv(passed_variable+'_conll_2.tsv', sep=' ', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, header=False)


####################################################################################################################################################
# Flair LitBank


import pandas as pd
import os
import csv
# import own script
from modules.hyphens import *
from modules.patch_flair_parsing import * 
from modules.calculate_metrics import *

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

def check_for_inconsistencies_litbank(current_file,gs_lb):
    try:
        for index, word, ner in current_file.itertuples(index=True):
            if word != gs_lb["original_word"].loc[index]:
                print("Position ", index, " '", word, "' in current is not the same as '", gs_lb["original_word"].loc[index], "'in gs")
                print(current_file.iloc[index-1:index+4])
                print(gs_lb.iloc[index-1:index+4])
                break
    #Note: some original texts are longer than the annotated files, we stop the comparisson at that length
    except KeyError:
        print("Reached end of annotated file. Cropped currect_file.")
        print("Last word ", word, " in line ", index)
        current_file = current_file.truncate(after=index-1)
        pass

filename = "TheCallOfTheWild.tsv"
litbank_filepath = "/mnt/data/gold_standard/overlap/litbank/" + books_mapping.get(str(filename.replace('.tsv',''))) + ".tsv"
flair_filepath = '/mnt/flair/' + filename
print(filename)
# read flair
current_file= pd.read_csv(flair_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1])
current_file = correct_hyphened(current_file)
# patch inconsistencies between parsing of flair and gold standards (using LitBank)
current_file = patch_flair(current_file, filename)
current_file.loc[~current_file["ner"].isin(['S-PER','I-PER','B-PER','E-PER']), "ner"] = "O"
# read litbank gs
gs_lb = pd.read_csv(litbank_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"])
gs_lb.loc[~gs_lb["gs"].isin(['I-PER','B-PER']), "gs"] = "O"
check_for_inconsistencies_litbank(current_file,gs_lb)
# merge the two dataframes
merged_flair_litbank = pd.merge(gs_lb, current_file, left_index=True, right_index=True)
del merged_flair_litbank['original_word_y']

merged_flair_litbank.to_csv(str(filename.replace('.tsv',''))+'_conll_3.tsv', sep=' ', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE, header=False)
