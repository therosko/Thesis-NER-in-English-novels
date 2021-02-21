import re
import pandas as pd

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
    elif word in ['-LRB-', '-RRB-', '-LSB-', '-RSB-','-','--','----']:
        return word
    else:
        print("Warning: " + str(word) + " contains a hypthen, but is not detected (or treated) as a hyphened compound word")
        return word

def correct_hyphened(df):
    ###################################################################################
    ## Iterate over rows, split hyphened compound words into individual entries
    ## Input: pandas dataframe
    ## Output: pandas dataframe
    ###################################################################################
    # change column type to object in order to be able to run the untagling of hyphened compound words
    df['original_word'] = df['original_word'].astype('object')
    for index, word, ner in df.itertuples(index=True):
        if "-" in word:
            # returns hyphened compound words as list of words (incl. hyphen)
            fixed_word = untangle_hyphened(word)
            df.at[index, "original_word"] = fixed_word
    # split list values in separate rows
    df = df.assign(original_word=df['original_word']).explode('original_word')
    df = df.reset_index(drop=True)
    for index, word, ner in df.itertuples(index=True):
        #only for gs files; if used for others, adapt
        if word == "-" and ner == "B-PER":
            df.at[index, "gs"] = "I-PER"
            df.at[index+1, "gs"] = "I-PER"
    return df
