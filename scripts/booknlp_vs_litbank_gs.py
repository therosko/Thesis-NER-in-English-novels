###########################################################################################
# This script reads in the gold standard (output of gs_extraction.py) and compares it to
# the .token files created by booknlp
#
# Output:
# The script appends a csv with the Precision, Recall, and F1 for the respective book
# and stores the false positives, false negatives, and correct detections for the respective book
#
#
# BookNLP recognises the following NER tags/types 
# (PERSON, NUMBER, DATE, DURATION, MISC, TIME, LOCATION, ORDINAL, MONEY, ORGANIZATION, SET, O)
# LitBank covers six of the ACE 2005 categories: 
# People (PER), Facilities (FAC), Geo-political entities (GPE), Locations (LOC), Vehicles (VEH), Organizations (ORG)
#
# Therefore we map the BookNLP entities to those of LitBank in the following way:
# O stays O and PERSON turns to PER. We ignore rest for character detection (in particular)
###########################################################################################


import pandas as pd
import csv
# import own script
import modules.hyphens

#### book example Alice in wonderland
#booknlp_filepath = "/mnt/book-nlp/data/tokens/alice.tokens"
#gs_filepath = "/mnt/data/gold_standard/11_alices_adventures_in_wonderland_brat.tsv"
#### book example Evelina
#booknlp_filepath = "/mnt/book-nlp/data/tokens/evelina.tokens"
#gs_filepath = "/mnt/data/gold_standard/6053_evelina_or_the_history_of_a_young_ladys_entrance_into_the_world_brat.tsv"
#### book example Sherlock
booknlp_filepath = "/mnt/book-nlp/data/tokens/huckleberry.tokens"
gs_filepath = "/mnt/data/gold_standard/76_adventures_of_huckleberry_finn_brat.tsv"

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

####### compare to gold standard
gs_df = pd.read_csv(gs_filepath, sep='\t', quoting=csv.QUOTE_NONE)
gs_df.loc[~gs_df["gs"].isin(['I-PER','B-PER']), "gs"] = "O"

# compare if the output file and the gold standard are the same
try:
    for index, word, ner in current_file.itertuples(index=True):
        if word != gs_df["original_word"].loc[index]:
            print("Position ", index, " '", word, "' in current is not the same as '", gs_df["original_word"].loc[index], "'in gs")
            break
# some original texts are longer than the annotated files, we stop the comparisson at that length
except KeyError:
    print("Reached end of annotated file. Cropped currect_file.")
    print("Last word ", word)
    current_file = current_file.truncate(after=index-1)
    pass

# merge the two dataframes
merged_df = pd.merge(current_file, gs_df, left_index=True, right_index=True)

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
for index, original_word_x, booknlp, original_word_y, gs in merged_df.itertuples(index=True):
    if original_word_x != original_word_y:
        print ("Mismatch in row ", index, ": ", original_word_x , " is not the same as ", original_word_y)
        break
    if gs == 'B-PER':
        if len(range_ne) > 0:
            if false_positive_booknlp == False: #make sure that the mistake is not a false positive, but instead the end of a gold standard entity
                for line in range_ne: # check if booknlp detected it correctly
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
                continue
            elif false_positive_booknlp == True: # if the mistake is a false positive
                list_false_positives.append(range_ne)
                range_ne = []
                false_positive_booknlp = False
                continue
        else:
            range_ne.append(index)
    elif gs == 'I-PER':
        range_ne.append(index)
    elif gs == 'O':
        if booknlp == 'PER':
            if false_positive_booknlp == False: #first occurence of wrong
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
            # add error handling in case of a mistake
            print ("1. Semantical mistake in analysing line ", index)
            break
    else:
        # add error handling in case of a mistake
        print ("Semantical mistake in analysing line ", index)
        break

# get the total number of named entites in the gold standard (each NE beginns with B-PER)
N_existing = merged_df.gs.str.count("B-PER").sum()

if ( len(list_false_positives) + len(list_false_negatives) + len(list_correct) ) != N_existing:
    raise Error ("Mismatch in total number of entities! Must be a semantic error")
#todo remove check after all books have been tested.

Precision =  len(list_correct) / (len(list_correct) + len(list_false_positives)) #true positives / (true positives + false positives)
Recall = len(list_correct) / (len(list_correct) + len(list_false_negatives)) #true positives / (true positives + false negatives)
F_1 = 1/((1/Precision)+(1/Recall))
#todo store results in a tsv

def get_word(list_of_indices):
    word_list = []
    for index in list_of_indices:
        word_list.append(merged_df.iloc[index]['original_word_x'])
    return word_list

# extract incorrect observations
incorrect=pd.DataFrame(columns=['index_list', 'word_list', 'false'])
for entity in list_false_negatives:
    incorrect = incorrect.append({'index_list': entity, 'word_list': get_word(entity), 'false': 'negative'}, ignore_index=True)

for entity in list_false_positives:
    incorrect = incorrect.append({'index_list': entity, 'word_list': get_word(entity), 'false': 'positive'}, ignore_index=True)
#incorrect.to_csv("compare_booknlp_to_gs_Huckleberry.tsv", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

# extract correct observations for testing
correct=pd.DataFrame(columns=['index_list', 'word_list', 'false'])
for entity in list_correct:
    correct = correct.append({'index_list': entity, 'word_list': get_word(entity), 'false': 'negative'}, ignore_index=True)
correct.to_csv("check_correct_detection_Alice.tsv", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

# TODO: run the same for another book!
#todo store results in a tsv
######################################################################################################
# Replicate 1 word = 1 NER
######################################################################################################
'''
current_file = pd.read_csv(booknlp_filepath, sep='\t', quoting=csv.QUOTE_NONE)

# BookNLP recognises the following NER tags/types (PERSON, NUMBER, DATE, DURATION, MISC, TIME, LOCATION, ORDINAL, MONEY, ORGANIZATION, SET, O)
# LitBank covers six of the ACE 2005 categories: People (PER), Facilities (FAC), Geo-political entities (GPE), Locations (LOC), Vehicles (VEH), Organizations (ORG)

# Therefore we map the BookNLP entities to those of LitBank in the following way:
# O stays O and PERSON turns to PER. We ignore rest for character detection (in particular)
# all_taggers_booknlp_to_litbank = {'PERSON':'PER', 'NUMBER':'', 'DATE': '', 'DURATION': '', 'MISC': '', 'TIME': '', 'LOCATION': 'LOC', 'ORDINAL': '', 'MONEY': '', 'ORGANIZATION': 'ORG', 'SET': '' }

current_file = current_file[['originalWord','ner']]
current_file = current_file.rename(columns={"originalWord": "original_word", "ner": "booknlp"})

# alternatively convert all PERSON to PER
current_file["booknlp"].replace('PERSON', 'PER', inplace = True)
# replace rest of entities with O
current_file.loc[~current_file["booknlp"].isin(['PER']), "booknlp"] = "O"
####### compare to gold standard
gs_df = pd.read_csv(gs_filepath, sep='\t', quoting=csv.QUOTE_NONE)
gs_df["gs"].replace('I-PER', 'PER', inplace = True)
gs_df["gs"].replace('B-PER', 'PER', inplace = True)
gs_df.loc[~gs_df["gs"].isin(['PER']), "gs"] = "O"

for index, word, ner in current_file.itertuples(index=True):
    if word != gs_df["original_word"].loc[index]:
        print("'", word, "' in current is not the same as '", gs_df["original_word"].loc[index], "'in gs")
        break

# merge the two dataframes
result = pd.merge(current_file, gs_df, left_index=True, right_index=True)

# set variables for evaluation
N_incorrect = 0
N_correct = 0
list_incorrect = []
# double-check that the merge is correct, calculate N_incorrect and N_correct
for index, original_word_x, booknlp, original_word_y, gs in result.itertuples(index=True):
    if original_word_x != original_word_y:
        print ("Mismatch in row ", index, ": ", original_word_x , " is not the same as ", original_word_y)
    elif (booknlp == 'PER' and gs == 'O') or (booknlp == 'O' and gs == 'PER'):
        N_incorrect += 1
        list_incorrect.append(original_word_x)
    elif booknlp == 'PER' and gs == 'PER':
        N_correct += 1
    elif booknlp == 'O' and gs == 'O':
        continue
    else:
        print("Semantical mistake")
        break

# get the total number of named entites in the gold standard

N_existing = result.gs.str.count("PER").sum()
Precision =  N_correct / (N_correct + N_incorrect)
Recall = N_correct / N_existing

result.loc[result['booknlp'] == 'PER']
result.loc[result['gs'] == 'PER']
'''
