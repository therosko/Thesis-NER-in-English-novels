import pandas as pd
import csv
# to match hyphened compound words
import re

booknlp_filepath = "/mnt/book-nlp/data/tokens/alice.tokens"
gs_filepath = "/mnt/data/gold_standard/11_alices_adventures_in_wonderland_brat.tsv"
#gs_filepath = "/mnt/data/gold_standard/6053_evelina_or_the_history_of_a_young_ladys_entrance_into_the_world_brat.tsv"


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
gs_df.loc[~gs_df["gs"].isin(['I-PER','B-PER']), "gs"] = "O"


# merge two dataframes
# TODO remove temporary change of column name to gs bellow
#current_file = current_file.rename(columns={"originalWord": "original_word", "booknlp": "gs"})
#diff = pd.concat([current_file,gs_df]).drop_duplicates(keep=False)
#diff.head(38)
#diff.tail(30)

for index, word, ner in current_file.itertuples(index=True):
    if word != gs_df["original_word"].loc[index]:
        print("'", word, "' in current is not the same as '", gs_df["original_word"].loc[index], "'in gs")
        break

# merge the two dataframes
merged_df = pd.merge(current_file, gs_df, left_index=True, right_index=True)

# set variables for evaluation
N_incorrect = 0
N_correct = 0
list_incorrect = []
# hold the lines range of the currently detected named entity
range_ne = []
missed_booknlp = 0
wrong_booknlp = 0
# double-check that the merge is correct, calculate N_incorrect and N_correct
for index, original_word_x, booknlp, original_word_y, gs in merged_df.itertuples(index=True):
    if original_word_x != original_word_y:
        print ("Mismatch in row ", index, ": ", original_word_x , " is not the same as ", original_word_y)
    if gs == 'B-PER':
        if len(range_ne) > 0:
            for line in range_ne:
                if merged_df.iloc[line]['booknlp'] == 'PER':
                    continue
                else: # if booknlp didn't detect it
                    missed_booknlp = 1
            if missed_booknlp == 1:
                N_incorrect +=1
                missed_booknlp = 0
            else:
                N_correct +=1
            range_ne = []
        else:
            range_ne.append(index)
    elif gs == 'I-PER':
        range_ne.append(index)
    elif gs == 'O':
        if len(range_ne) > 0:
            for line in range_ne:
                if merged_df.iloc[line]['booknlp'] == 'PER':
                    continue
                else: # if booknlp didn't detect it
                    missed_booknlp = 1
            if missed_booknlp == 1:
                N_incorrect +=1
                missed_booknlp = 0
            else:
                N_correct +=1
            range_ne = []
        else:
            if booknlp == 'PER':
                if wrong_booknlp == 0: #first occurence of wrong
                    wrong_booknlp = 1
                    range_ne.append(index)
                else: #wrong_booknlp == 1
                    range_ne.append(index)
            else: # booknlp == 'O'
                if wrong_booknlp == 0:
                    continue
                else: #wrong_booknlp == 1
                    N_incorrect +=1
                    range_ne = []
                    wrong_booknlp = 0
    else:
        print ("Happy little accident in line ", index)
        break

# get the total number of named entites in the gold standard (each NE beginns with B-PER)
N_existing = merged_df.gs.str.count("B-PER").sum()

Precision =  N_correct / (N_correct + N_incorrect)
Recall = N_correct / N_existing
F_1 = 1/((1/Precision)+(1/Recall))


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
