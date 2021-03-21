##############################################################################################################
# This script reads in the two gold standards Litbank and Dekker et al and compares them to
# the .token files created by booknlp
# The data used here consists of only the 12 overlapping novels with their respecive overlapping
# parts of the text.
#
# Output:
# The script appends a csv with the Precision, Recall, and F1 for the respective book and respective tool
# and stores the false positives, false negatives, and correct detections
#
#
# BookNLP recognises the following NER tags/types 
# (PERSON, NUMBER, DATE, DURATION, MISC, TIME, LOCATION, ORDINAL, MONEY, ORGANIZATION, SET, O)
# Dekker et al.'s collection covers the entity person (i.e. I-PERSON)
# LitBank covers six of the ACE 2005 categories: 
# People (PER), Facilities (FAC), Geo-political entities (GPE), Locations (LOC), Vehicles (VEH), Organizations (ORG)
#
# Therefore we map the BookNLP entities to those of Dekker et al. in the following way:
# O stays O and PERSON turns to PER. We ignore rest for character detection (in particular)
##############################################################################################################

import pandas as pd
import csv
import sys
import re
# import own script
from modules.hyphens import *
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
passed_variable = sys.argv[1]
booknlp_filepath = "/mnt/book-nlp/data/tokens/overlap/" + str(passed_variable) + ".tokens"
dekker_filepath = "/mnt/data/gold_standard/overlap/dekker_et_al/" + str(passed_variable) + ".gs"
litbank_filepath = "/mnt/data/gold_standard/overlap/litbank/" + books_mapping.get(str(passed_variable)) + ".tsv"

#######################################
# get current annotated book - BookNLP
#######################################
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


#####################################
# get gold standard - Dekker
#####################################
gs_d = pd.read_csv(dekker_filepath, sep=' ', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"])
gs_d = correct_hyphened(gs_d)

gs_d.loc[~gs_d["gs"].isin(['I-PERSON']), "gs"] = "O"


# compare if the output file and the gold standard are the same
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
                break
#Note: some original texts are longer than the annotated files, we stop the comparisson at that length
except KeyError:
    print("Reached end of annotated file. Cropped currect_file.")
    print("Last word ", word, " in line ", index)
    current_file = current_file.truncate(after=index-1)
    pass

# merge BookNLP and Dekker et al.
merged_booknlp_dekkeretal = pd.merge(current_file, gs_d, left_index=True, right_index=True)

########################################################
# run evaluation using gold standard Dekker et al. 
########################################################
# hold the lines range of the currently detected named entity
range_ne = []
# set booleans to keep of track of false positives/negatives of entities spreading over multiple rows
false_negative_booknlp = False
false_positive_booknlp = False 
# lists to hold mistakes in the detection (used for the recognition of challenges)
list_false_negatives = []
list_false_positives = []
list_correct = []

for index, original_word_x, booknlp, original_word_y, gs in merged_booknlp_dekkeretal.itertuples(index=True):
    '''
    if original_word_x != original_word_y:
        print ("Mismatch in row ", index, ": ", original_word_x , " is not the same as ", original_word_y)
        break
    '''
    if original_word_x != original_word_y:
        if (original_word_y == '-LRB-' and original_word_x == '(') or (original_word_y == '-RRB-' and original_word_x == ')') or (original_word_y == '-LSB-' and original_word_x == '[') or (original_word_y == '-RSB-' and original_word_x == ']'):
            pass
        elif (original_word_y in ['`',"``","--","''","'",'--']) and (original_word_x in ["‘","' \" '",'"',"“",'-',"”","'",",","’","—","_"]):
            pass
        elif (re.match(r"[a-zA-Z]*'[a-zA-Z]+", original_word_y)) and (re.match(r"[a-zA-Z]*’[a-zA-Z]+", original_word_x)):
            pass
        elif (re.match(r"[a-zA-Z]*’[a-zA-Z]+", original_word_y)) and (re.match(r"[a-zA-Z]*'[a-zA-Z]+", original_word_x)):
            pass
        elif (original_word_y == "`" and original_word_x == "'t") or (original_word_y == "tis" and original_word_x == "is") or (original_word_y == "honourable" and original_word_x == "honorable") or (original_word_y == "honour" and original_word_x == "honor"):
            pass
        else:
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
                if merged_booknlp_dekkeretal.iloc[line]['booknlp'] == 'PER':
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
            # add error handling in case of a mistake
            print ("1. Semantical mistake in analysing line ", index)
            break
    else:
        # add error handling in case of a mistake
        print ("Semantical mistake in analysing line ", index)
        break

#####################################################################
# get evaluation metrics and save to files (BookNLP & Dekker et al.)
#####################################################################

path_evaluation = '/mnt/Git/results/overlap/booknlp_dekkeretal_evaluation.csv'
path_fp = '/mnt/Git/results/overlap/booknlp_dekkeretal_false_positive.csv'
path_fn = '/mnt/Git/results/overlap/booknlp_dekkeretal_false_negative.csv'

#todo outcomment in the end
get_metrics(merged_booknlp_dekkeretal, list_correct, list_false_positives, list_false_negatives, path_evaluation, path_fp, path_fn, passed_variable)

########################################################################################################################################################################


##################################
# get gold standard - Litbank
##################################
gs_lb = pd.read_csv(litbank_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"])
gs_lb.loc[~gs_lb["gs"].isin(['I-PER','B-PER']), "gs"] = "O"

# compare if the output file and the gold standard are the same
try:
    for index, word, ner in current_file.itertuples(index=True):
        if word != gs_lb["original_word"].loc[index]:
            print("Position ", index, " '", word, "' in current is not the same as '", gs_lb["original_word"].loc[index], "'in gs")
            break
#Note: some original texts are longer than the annotated files, we stop the comparisson at that length
except KeyError:
    print("Reached end of annotated file. Cropped currect_file.")
    print("Last word ", word, " in line ", index)
    current_file = current_file.truncate(after=index-1)
    pass

# merge the two dataframes
merged_booknlp_litbank = pd.merge(current_file, gs_lb, left_index=True, right_index=True)

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

# double-check that the merge is correct, calculate incorrect and correct by using lists
for index, original_word_x, booknlp, original_word_y, gs in merged_booknlp_litbank.itertuples(index=True):
    if original_word_x != original_word_y:
        print ("Mismatch in row ", index, ": ", original_word_x , " is not the same as ", original_word_y)
        break
    if gs == 'B-PER':
        if len(range_ne) > 0:
            if false_positive_booknlp == False: #make sure that the mistake is not a false positive, but instead the end of a gold standard entity
                for line in range_ne: # check if booknlp detected it correctly
                    if merged_booknlp_litbank.iloc[line]['booknlp'] == 'PER':
                        continue
                    else: # if booknlp didn't detect it
                        false_negative_booknlp = True
                if false_negative_booknlp == True:
                    list_false_negatives.append(range_ne)
                    false_negative_booknlp = False
                else:
                    list_correct.append(range_ne)
                range_ne = []
                range_ne.append(index)
                continue
            elif false_positive_booknlp == True: # if the mistake is a false positive
                list_false_positives.append(range_ne)
                range_ne = []
                false_positive_booknlp = False
                range_ne.append(index)
                continue
        else:
            range_ne.append(index)
    elif gs == 'I-PER':
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
                if merged_booknlp_litbank.iloc[line]['booknlp'] == 'PER':
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
            # add error handling in case of a mistake
            print ("1. Semantical mistake in analysing line ", index)
            break
    else:
        # add error handling in case of a mistake
        print ("Semantical mistake in analysing line ", index)
        break

#####################################################################
# get evaluation metrics and save to files (BookNLP & Dekker et al.)
#####################################################################

path_evaluation = '/mnt/Git/results/overlap/booknlp_litbank_evaluation.csv'
path_fp = '/mnt/Git/results/overlap/booknlp_litbank_false_positive.csv'
path_fn = '/mnt/Git/results/overlap/booknlp_litbank_false_negative.csv'

get_metrics(merged_booknlp_litbank, list_correct, list_false_positives, list_false_negatives, path_evaluation, path_fp, path_fn, passed_variable)
