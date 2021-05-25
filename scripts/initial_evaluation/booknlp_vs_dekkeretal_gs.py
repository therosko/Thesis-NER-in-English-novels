##########################################################################################################
# This script reads in the gold standard (output of dekkeretal_gs_extraction.py) and compares it to
# the .token files created by booknlp
#
# Output:
# The script appends a csv with the Precision, Recall, and F1 for the respective book
# and stores the false positives, false negatives, and correct detections for the respective book
#
#
# BookNLP recognises the following NER tags/types 
# (PERSON, NUMBER, DATE, DURATION, MISC, TIME, LOCATION, ORDINAL, MONEY, ORGANIZATION, SET, O)
# Dekker et al.'s collection covers the entity person (i.e. I-PERSON)
#
# Therefore we map the BookNLP entities to those of Dekker et al. in the following way:
# O stays O and PERSON turns to PER. We ignore rest for character detection (in particular)
##########################################################################################################

import pandas as pd
import csv
import sys
# import own script
from hyphens import *
from calculate_metrics import *

passed_variable = sys.argv[1]
booknlp_filepath = "/mnt/book-nlp/data/tokens/dekkeretal/" + str(passed_variable) + ".tokens"
gs_filepath = "/mnt/data/gold_standard/dekker_et_al/" + str(passed_variable) + ".gs"

############################
# get current annotated book
############################
current_file = pd.read_csv(booknlp_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=["originalWord","ner"])
current_file = current_file.rename(columns={"originalWord": "original_word", "ner": "booknlp"})
# alternatively convert all PERSON to PER
current_file["booknlp"].replace('PERSON', 'PER', inplace = True)
# replace rest of entities with O
current_file.loc[~current_file["booknlp"].isin(['PER']), "booknlp"] = "O"
# correct hyphened words from booknlp (note: stanford CoreNLP only splits on "most hyphens")
current_file = correct_hyphened(current_file)
# reset the index to avoid all parts of hyphened words having same index
current_file = current_file.reset_index()
del current_file['index']


############################
# get gold standard
############################
gs_df = pd.read_csv(gs_filepath, sep=' ', quoting=csv.QUOTE_NONE, usecols=["original_word", "gs"])
gs_df = correct_hyphened(gs_df)

gs_df.loc[~gs_df["gs"].isin(['I-PERSON']), "gs"] = "O"

#Note that both files contain LRB, RRB, LSB, RSB

# compare if the output file and the gold standard are the same
try:
    for index, word, ner in current_file.itertuples(index=True):
        if word != gs_df["original_word"].loc[index]:
            print("Position ", index, " '", word, "' in current is not the same as '", gs_df["original_word"].loc[index], "'in gs")
            break
#Note: some original texts are longer than the annotated files, we stop the comparisson at that length
except KeyError:
    print("Reached end of annotated file. Cropped currect_file.")
    print("Last word ", word, " in line ", index)
    current_file = current_file.truncate(after=index-1)
    pass

# merge the two dataframes
merged_df = pd.merge(current_file, gs_df, left_index=True, right_index=True)


############################
# run evaluation
############################
# hold the lines range of the currently detected named entity
range_ne = []
# set booleans to keep of track of false positives/negatives of entities spreading over multiple rows
false_negative_booknlp = False
false_positive_booknlp = False 
# lists to hold mistakes in the detection (used for the recognition of challenges)
list_false_negatives = []
list_false_positives = []
list_correct = []

for index, original_word_x, booknlp, original_word_y, gs in merged_df.itertuples(index=True):
    if original_word_x != original_word_y:
        print ("Mismatch in row ", index, ": ", original_word_x , " is not the same as ", original_word_y)
        break
    if gs == 'I-PERSON':
        if false_positive_booknlp == True:
            list_false_positives.append(range_ne)
            range_ne = []
            false_positive_booknlp = False
            range_ne.append(index)
            continue
        else:
            range_ne.append(index)
    elif gs == 'O':
        if booknlp == 'PER':
            if false_positive_booknlp == False: #first occurence of wrong
                if len(range_ne) > 0 and false_negative_booknlp == False: # there was a correct detection immediatelly before
                    list_correct.append(range_ne)
                    range_ne = []
                false_positive_booknlp = True
                range_ne.append(index)
                continue
            elif false_positive_booknlp == True:
                range_ne.append(index)
                continue
        elif booknlp == 'O' and false_positive_booknlp == True:
            list_false_positives.append(range_ne)
            range_ne = []
            false_positive_booknlp = False
            continue
        elif len(range_ne) > 0 and false_positive_booknlp == False: #if it is the end of a gold standard entity
            for line in range_ne:
                if merged_df.iloc[line]['booknlp'] == 'PER':
                    continue
                else: # if booknlp didn't detect it
                    false_negative_booknlp = True
            if false_negative_booknlp == True:
                list_false_negatives.append(range_ne)
                false_negative_booknlp = False
            else:
                list_correct.append(range_ne)
            range_ne = []
        elif booknlp == 'O' and false_negative_booknlp == True:
            list_false_negatives.append(range_ne)
            false_negative_booknlp = False
            range_ne = []
        elif booknlp == 'O' and false_negative_booknlp == False and false_positive_booknlp == False:
            continue
        else:
            # add error detection in case of a mistake
            print ("Semantical mistake in analysing line ", index)
            break
    else:
        # add error detection in case of a mistake
        print ("Semantical mistake in analysing line ", index)
        break

###########################################
# get evaluation metrics and save to files
###########################################

path_evaluation = '/mnt/Git/results/dekkeretal/booknlp_dekkeretal_evaluation.csv'
path_fp = '/mnt/Git/results/dekkeretal/booknlp_dekkeretal_false_positive.csv'
path_fn = '/mnt/Git/results/dekkeretal/booknlp_dekkeretal_false_negative.csv'

get_metrics(merged_df, list_correct, list_false_positives, list_false_negatives, path_evaluation, path_fp, path_fn, passed_variable)
