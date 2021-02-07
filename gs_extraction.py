########################################################################################################
## Summary: Gold standard - extract first two columns of each tsv file in a folder and write them to a separate tsv file
## Requires: 
##           - path to the initial tsv files
##           - path to the output directory
########################################################################################################

import os
import csv
# extracting filename from filepath (works with all os file path standards)
#import ntpath
import pandas as pd
import re

path_to_annotated_files = "/mnt/data/litbank/entities/tsv"
gs_output_dir = "/mnt/data/gold_standard"

def untangle_hyphened(word):
    ###################################################################################
    ## Matches a hyphened compount word, Splits it into a list of words (incl. hyphen)
    ## Input: Word with a hyphen [Called by correct_hyphened]
    ## Output: List of words / Single hyphen (in case of no match in the RE)
    ###################################################################################
    if re.match(r"[a-zA-Z]+-[a-zA-Z]+-[a-zA-Z]+-[a-zA-Z]+", word):
        # e.g. out-of-the-way
        fixed_words = []
        hyphen_one = word.find("-")
        #add first word
        fixed_words.append(word[:hyphen_one])
        fixed_words.append("-")
        word_temp = word[(hyphen_one+1):]
        hyphen_two = word_temp.find("-")
        # add second word
        fixed_words.append(word_temp[:hyphen_two])
        fixed_words.append("-")
        word_end = word_temp[(hyphen_two+1):]
        hyphen_three = word_end.find("-")
        # add third word
        fixed_words.append(word_end[:hyphen_three])
        fixed_words.append("-")
        # add last word
        fixed_words.append(word_end[(hyphen_three+1):])
        return fixed_words
    elif re.match(r"[a-zA-Z]+-[a-zA-Z]+-[a-zA-Z]+", word):
        # e.g. of-the-way
        hyphen_one = word.find("-")
        fixed_words = []
        fixed_words.append(word[:hyphen_one])
        fixed_words.append("-")
        word_rest = word[(hyphen_one+1):]
        hyphen_two = word_rest.find("-")
        fixed_words.append(word_rest[:hyphen_two])
        fixed_words.append("-")
        fixed_words.append(word_rest[(hyphen_two+1):])
        return fixed_words
    elif re.match(r"[a-zA-Z]+.*-[a-zA-Z]+", word):
        # e.g. WAISTCOAT-POCKET
        hyphen_position = word.find('-')
        #fixed_words = str(word[:hyphen_position]) + ",-," + str(word[(hyphen_position+1):]) # does not work, as single comma entries are later split into two empty strings
        fixed_words = []
        fixed_words.append(word[:hyphen_position])
        fixed_words.append("-")
        fixed_words.append(word[(hyphen_position+1):])
        return fixed_words
    elif word == "-" or word == "--" or word == "----":
        return word
    else:
        print("Warning: " + str(word) + " contains a hypthen, but is not detected (or treated) as a hyphened compound word")
        return word

def correct_hyphened(gs_df):
    ###################################################################################
    ## Iterate over rows, split hyphened compound words into individual entries
    ## Input: dataframe
    ## Output: dataframe
    ###################################################################################
    # change column type to object in order to be able to run the untagling of hyphened compound words
    gs_df['original_word'] = gs_df['original_word'].astype('object')
    for index, word, ner in gs_df.itertuples(index=True):
        if "-" in word:
            # returns hyphened compound words as list of words (incl. hyphen)
            fixed_word = untangle_hyphened(word)
            gs_df.at[index, "original_word"] = fixed_word
    # split list values in separate rows
    gs_df = gs_df.assign(original_word=gs_df['original_word']).explode('original_word')
    return gs_df


for filename in os.listdir(path_to_annotated_files):
    if filename.endswith(".tsv"): 
        # read file to pandas dataframe; litbank files have 6 detenced columns (based on tabs)
        filepath = path_to_annotated_files + "/" + filename
        # files have different levels and therefore a different number of columns. we only take and name the first two columns
        current_file = pd.read_csv(filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"]) 

        # The golden standard treats hyphened compound words such as WAISTCOAT-POCKET as one word instead of three separate. We find and split those for the further analysis
        current_file = correct_hyphened(current_file)

        # write only first two columns (entity and first level of annotation) to a specified folder 
        outpath = gs_output_dir + "/" + filename
        current_file.to_csv(outpath, sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)
        # clean up (not mandatory)
        current_file.drop(current_file.index, inplace=True)




'''
####### For analysis of one file with pandas this works
import pandas as pd
import csv 

filename = "/mnt/data/litbank/entities/tsv/12677_personality_plus_some_experiences_of_emma_mcchesney_and_her_son_jock_brat.tsv"

current_file = pd.read_csv(filename, sep='\t', quoting=csv.QUOTE_NONE, names=["entity", "gs", "lvl2", "lvl3", "lvl4", "rest"]) 
current_file

current_file[["entity","gs"]].to_csv("/mnt/data/gold_standard/test.tsv", sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)
'''
