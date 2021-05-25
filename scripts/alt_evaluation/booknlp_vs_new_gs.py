########################################################################################################################
# This script reads in the new gold standard and compairs it to the BookNLP output files
# The data used here consists of only the 12 overlapping novels with their respecive overlapping
# parts of the text.
#
# Output:
# The script appends a csv with the Precision, Recall, and F1 for the respective book
# and stores the false positives, false negatives, and correct detections
#
# The new gold standard, extracted from Doccano, recognises the following NER tags for the entity type PEOPLE
# B-PERSON - for the beginning of an entity according to CoNLL-2003
# I-PERSON - for a token inside of an entity according to CoNLL-2003
# B-PERX - for the beginning of an entity according to extended annotation guidelines
# I-PERX - for a token inside of an entity according to extended annotation guidelines
#
# BookNLP recognises the NER tag PER for the entity type PEOPLE
########################################################################################################################


import pandas as pd
import os
import csv
# import own script
from hyphens import *
from calculate_metrics import *

def check_for_inconsistencies(current_file,gs_new):
    try:
        for index, word, ner in current_file.itertuples(index=True):
            if word != gs_new["original_word"].loc[index]:
                print("Position ", index, " '", word, "' in current is not the same as '", gs_new["original_word"].loc[index], "'in gs")
                print(current_file.iloc[index-1:index+4])
                print(gs_new.iloc[index-1:index+4])
                break
    #Note: some original texts are longer than the annotated files, we stop the comparisson at that length
    except KeyError:
        print("Reached end of annotated file. Cropped currect_file.")
        print("Last word ", word, " in line ", index)
        current_file = current_file.truncate(after=index-1)
        pass

def evaluate(merged_booknlp_new):
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
    for index, original_word_x, booknlp, original_word_y, gs in merged_booknlp_new.itertuples(index=True):
        if original_word_x != original_word_y:
            print ("Mismatch in row ", index, ": ", original_word_x , " is not the same as ", original_word_y)
            break
        if gs == 'B-PER':
            if len(range_ne) > 0:
                if false_positive_booknlp == False: #make sure that the mistake is not a false positive, but instead the end of a gold standard entity
                    for line in range_ne: # check if booknlp detected it correctly
                        if merged_booknlp_new.iloc[line]['booknlp'] == 'PER':
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
                    if merged_booknlp_new.iloc[line]['booknlp'] == 'PER':
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
    '''print("list_false_positives",list_false_positives)
    print("list_correct",list_correct)
    print("list_false_negatives",list_false_negatives)
    for i in list_false_negatives:
        print(merged_booknlp_new.iloc[i[0]-1:i[-1]+2])'''
    return list_correct, list_false_positives, list_false_negatives
    


directory = os.fsencode('/mnt/book-nlp/data/tokens/overlap/')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".tokens"): 
        new_filepath = "/mnt/Git/annotation/gs/" + str(filename.replace('.tokens','')) + "_final.tsv"
        booknlp_filepath = '/mnt/book-nlp/data/tokens/overlap/' + filename
        print(filename)
        # read booknlp
        current_file= pd.read_csv(booknlp_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=["originalWord","ner"])
        current_file = current_file.rename(columns={"originalWord": "original_word", "ner": "booknlp"})
        # alternatively convert all PERSON to PER
        current_file["booknlp"].replace('PERSON', 'PER', inplace = True)
        # replace rest of entities with O
        current_file.loc[~current_file["booknlp"].isin(['PER']), "booknlp"] = "O"
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
        check_for_inconsistencies(current_file,gs_new_conll)
        # merge the two dataframes
        merged_booknlp_new = pd.merge(current_file, gs_new_conll, left_index=True, right_index=True)
        #print(merged_booknlp_new.head(2))
        #evaluate
        list_correct, list_false_positives, list_false_negatives = evaluate(merged_booknlp_new)
        # get evaluation metrics and save to files 
        path_evaluation = '/mnt/Git/results/overlap/booknlp_new_conll_evaluation.csv'
        path_fp = '/mnt/Git/results/overlap/booknlp_new_conll_false_positive.csv'
        path_fn = '/mnt/Git/results/overlap/booknlp_new_conll_false_negative.csv'
        get_metrics(merged_booknlp_new, list_correct, list_false_positives, list_false_negatives, path_evaluation, path_fp, path_fn, filename.replace('.tokens',''))
        ###########################################
        ###### second evaluation with PERSON and PERX labels
        check_for_inconsistencies(current_file,gs_new)
        # merge the two dataframes
        merged_booknlp_new = pd.merge(current_file, gs_new, left_index=True, right_index=True)
        print(merged_booknlp_new.head(2))
        #evaluate
        list_correct, list_false_positives, list_false_negatives = evaluate(merged_booknlp_new)
        # get evaluation metrics and save to files 
        path_evaluation = '/mnt/Git/results/overlap/booknlp_new_all_evaluation.csv'
        path_fp = '/mnt/Git/results/overlap/booknlp_new_all_false_positive.csv'
        path_fn = '/mnt/Git/results/overlap/booknlp_new_all_false_negative.csv'
        get_metrics(merged_booknlp_new, list_correct, list_false_positives, list_false_negatives, path_evaluation, path_fp, path_fn, filename.replace('.tokens',''))