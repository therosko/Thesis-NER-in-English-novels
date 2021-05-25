# compare if the output file and the gold standard are the same
import pandas as pd
import re

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

def check_for_inconsistencies_litbank(current_file,gs_lb):
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

def check_for_inconsistencies_new(current_file,gs_new):
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
