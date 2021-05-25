########################################################################################################################
# This script reads in the Dekker et al. gold standard and compairs it to the Flair output files
# The data used here consists of only the 12 overlapping novels with their respecive overlapping
# parts of the text.
#
# Output:
# The script appends a csv with the Precision, Recall, and F1 for the respective book
# and stores the false positives, false negatives, and correct detections
#
# Dekker et al. recognises only the I-PERSON tag.
#
# Flair recognises the following NER tags for the entity type PEOPLE
# S-PER - for a single token entity
# B-PER - for the beginning of a multi-token entity
# I-PER - for a token inside of a multi-token entity
# E-PER - for the end of a multi-token entity (due to differences in parsing, sometimes there are two tokens with E-PER)
########################################################################################################################


import pandas as pd
import os
import csv
# import own script
from hyphens import *
from patch_flair_parsing import * 
from calculate_metrics import *

def check_for_inconsistencies(current_file,gs_d):
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

def evaluate(merged_flair_dekkeretal):
    ############################
    # run evaluation
    ############################
    # hold the lines range of the currently detected named entity
    range_ne = []
    # set booleans to keep of track of false positives/negatives of entities spreading over multiple rows
    false_negative_flair = False
    false_positive_flair = False 
    # lists to hold mistakes in the detection (used for the recognition of challenges)
    list_false_negatives = []
    list_false_positives = []
    list_correct = []
    for index, original_word_x, flair, original_word_y, gs in merged_flair_dekkeretal.itertuples(index=True):
        if gs == 'I-PERSON':
            if false_positive_flair == True:
                list_false_positives.append(range_ne)
                range_ne = []
                false_positive_flair = False
                range_ne.append(index)
                continue
            else:
                range_ne.append(index)
        elif gs == 'O':
            if flair == "S-PER":
                list_false_positives.append([index])
                continue
            elif flair == "B-PER":
                if false_positive_flair == False: #first occurence of wrong
                    if len(range_ne) > 0 and false_negative_flair == False: # there was a correct detection immediatelly before
                        list_correct.append(range_ne)
                        range_ne = []
                    false_positive_flair = True
                    range_ne.append(index)
                    continue
                elif false_positive_flair == True:
                    range_ne.append(index)
                    continue
            elif flair in ["I-PER","E-PER"]:
                #due to differences in parsing, sometimes there are two tokens with E-PER
                range_ne.append(index)
                continue
            elif flair == 'O' and false_positive_flair == True:
                list_false_positives.append(range_ne)
                range_ne = []
                false_positive_flair = False
                continue
            elif len(range_ne) > 0 and false_positive_flair == False: #if it is the end of a gold standard entity
                if merged_flair_dekkeretal.iloc[range_ne[0]]['ner'] == 'B-PER' and merged_flair_dekkeretal.iloc[range_ne[-1]]['ner'] == 'E-PER':
                    for line in range_ne[1:-1]: # check if flair detected it correctly
                        if merged_flair_dekkeretal.iloc[line]['ner'] == 'I-PER':
                            continue
                        else: # if flair didn't detect it
                            false_negative_flair = True
                    if false_negative_flair == True:
                        list_false_negatives.append(range_ne)
                        false_negative_flair = False
                    else:
                        list_correct.append(range_ne)
                    range_ne = []
                    continue
                elif len(range_ne) == 1 and merged_flair_dekkeretal.iloc[range_ne[0]]['ner'] in ["S-PER","B-PER"]:
                    list_correct.append(range_ne)
                    range_ne = []
                else:
                    list_false_negatives.append(range_ne)
                    range_ne = []
                    continue
            elif flair == 'O' and false_negative_flair == True:
                list_false_negatives.append(range_ne)
                false_negative_flair = False
                range_ne = []
            elif flair == 'O' and false_negative_flair == False and false_positive_flair == False:
                continue
            else:
                # add error handling in case of a mistake
                print ("1. Semantical mistake in analysing line ", index)
                print(merged_flair_dekkeretal.iloc[index-3:index+4])
                break
            pass
        else:
            # add error handling in case of a mistake
            print ("Semantical mistake in analysing line ", index)
            break
    print("list_false_negatives",list_false_negatives)
    for i in list_false_negatives:
        print(merged_flair_dekkeretal.iloc[i[0]-1:i[-1]+2])
    print("list_false_positives",list_false_positives)
    for i in list_false_positives:
        print(merged_flair_dekkeretal.iloc[i[0]-1:i[-1]+2])
    print("list_correct",list_correct)
    for i in list_correct:
        print(merged_flair_dekkeretal.iloc[i[0]-1:i[-1]+2])
    return list_correct, list_false_positives, list_false_negatives


directory = os.fsencode('/mnt/flair/')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".tsv"): 
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
        check_for_inconsistencies(current_file,gs_d)
        # merge the two dataframes
        merged_flair_dekkeretal = pd.merge(current_file, gs_d, left_index=True, right_index=True)
        #evaluate
        list_correct, list_false_positives, list_false_negatives = evaluate(merged_flair_dekkeretal)
        ###########################################
        # get evaluation metrics and save to files 
        ###########################################
        path_evaluation = '/mnt/Git/results/overlap/flair_dekkeretal_evaluation.csv'
        path_fp = '/mnt/Git/results/overlap/flair_dekkeretal_false_positive.csv'
        path_fn = '/mnt/Git/results/overlap/flair_dekkeretal_false_negative.csv'
        #get_metrics(merged_flair_dekkeretal, list_correct, list_false_positives, list_false_negatives, path_evaluation, path_fp, path_fn, filename.replace('.tsv',''))
