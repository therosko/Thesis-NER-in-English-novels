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

def check_for_inconsistencies(current_file,gs_lb):
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

def evaluate(merged_flair_litbank):
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
    # double-check that the merge is correct, calculate incorrect and correct by using lists
    for index, original_word_x, flair, original_word_y, gs in merged_flair_litbank.itertuples(index=True):
        if original_word_x != original_word_y:
            print ("Mismatch in row ", index, ": ", original_word_x , " is not the same as ", original_word_y)
            break
        if gs == 'B-PER':
            if flair == "S-PER" and merged_flair_litbank['ner'].iloc[index+1] == "O":
                list_correct.append(index)
                #print (index, original_word_x, flair, original_word_y, gs)
            elif flair == "B-PER" and merged_flair_litbank['ner'].iloc[index+1] == "O":
                list_correct.append(index)
            if len(range_ne) > 0:
                if false_positive_flair == False: #make sure that the mistake is not a false positive, but instead the end of a gold standard entity
                    if merged_flair_litbank.iloc[range_ne[0]]['ner'] == 'B-PER' and merged_flair_litbank.iloc[range_ne[-1]]['ner'] == 'E-PER':
                        for line in range_ne[1:-1]: # check if flair detected it correctly
                            if merged_flair_litbank.iloc[line]['ner'] == 'I-PER':
                                continue
                            else: # if flair didn't detect it
                                false_negative_flair = True
                        if false_negative_flair == True:
                            list_false_negatives.append(range_ne)
                            false_negative_flair = False
                        else:
                            list_correct.append(range_ne)
                        range_ne = []
                        # add the new B-PER to the beginning of an entity
                        range_ne.append(index)
                        continue
                    else:
                        list_false_negatives.append(range_ne)
                        range_ne = []
                        range_ne.append(index)
                        continue
                elif false_positive_flair == True: # if the mistake is a false positive
                    list_false_positives.append(range_ne)
                    range_ne = []
                    false_positive_flair = False
                    range_ne.append(index)
                    continue
            else:
                range_ne.append(index)
                #print (index, original_word_x, flair, original_word_y, gs)
        elif gs == 'I-PER':
            range_ne.append(index)
        elif gs == 'O':
            if flair in ['S-PER','B-PER','I-PER'] :
                if false_positive_flair == False: #first occurence of wrong
                    if len(range_ne) > 0 and false_negative_flair == False: # there was a correct detection immediatelly before
                        list_correct.append(range_ne)
                        range_ne = []
                    # both if statements should be ran!
                    if flair != 'S-PER':
                        false_positive_flair = True
                        range_ne.append(index)
                        continue
                    else: #if S-PER (single token entity)
                        range_ne.append(index)
                        list_false_positives.append(range_ne)
                        range_ne = []
                        continue
                elif false_positive_flair == True:
                    range_ne.append(index)
                    continue
            elif flair == 'E-PER' and false_positive_flair == True:
                range_ne.append(index)
                list_false_positives.append(range_ne)
                range_ne = []
                false_positive_flair = False
                continue
            elif len(range_ne) > 0 and false_positive_flair == False: #if it is the end of a gold standard entity
                if merged_flair_litbank.iloc[range_ne[0]]['ner'] == 'B-PER' and merged_flair_litbank.iloc[range_ne[-1]]['ner'] == 'E-PER':
                    for line in range_ne[1:-1]: # check if flair detected it correctly
                        if merged_flair_litbank.iloc[line]['ner'] == 'I-PER':
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
                else:
                    list_false_negatives.append(range_ne)
                    range_ne = []
                    continue
            elif flair == 'O' and false_positive_flair == True:
                list_false_positives.append(range_ne)
                range_ne = []
                false_positive_flair = False
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
                print(merged_flair_litbank.iloc[index-3:index+4])
                break
        else:
            # add error handling in case of a mistake
            print ("Semantical mistake in analysing line ", index)
            break
    print("list_false_positives",list_false_positives)
    return list_correct, list_false_positives, list_false_negatives


directory = os.fsencode('/mnt/flair/')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".tsv"): 
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
        check_for_inconsistencies(current_file,gs_lb)
        # merge the two dataframes
        merged_flair_litbank = pd.merge(current_file, gs_lb, left_index=True, right_index=True)
        #evaluate
        list_correct, list_false_positives, list_false_negatives = evaluate(merged_flair_litbank)
        ###########################################
        # get evaluation metrics and save to files 
        ###########################################
        path_evaluation = '/mnt/Git/results/overlap/flair_litbank_evaluation.csv'
        path_fp = '/mnt/Git/results/overlap/flair_litbank_false_positive.csv'
        path_fn = '/mnt/Git/results/overlap/flair_litbank_false_negative.csv'
        get_metrics(merged_flair_litbank, list_correct, list_false_positives, list_false_negatives, path_evaluation, path_fp, path_fn, filename.replace('.tsv',''))
