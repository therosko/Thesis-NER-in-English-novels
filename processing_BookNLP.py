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
gs_df["gs"].replace('I-PER', 'PER', inplace = True)
gs_df["gs"].replace('B-PER', 'PER', inplace = True)
gs_df.loc[~gs_df["gs"].isin(['PER']), "gs"] = "O"


# merge two dataframes
# TODO remove temporary change of column name to gs bellow
current_file = current_file.rename(columns={"originalWord": "original_word", "booknlp": "gs"})
diff = pd.concat([current_file,gs_df]).drop_duplicates(keep=False)
diff.head(38)
diff.tail(30)

result = pd.merge(current_file, gs_df, on="index")



'''
# Moved to gs_extraction.py
# The golden standard treats hyphened compound words such as WAISTCOAT-POCKETas one word instead of three separate. We find and split those for the further analysis
# change column type to object in order to be able to run the untagling of hyphened compound words
gs_df['original_word'] = gs_df['original_word'].astype('object')

def untangle_hyphened(word):
    if re.match(r"[a-zA-Z]*-[a-zA-Z]*", word):
        hyphen_position = word.find('-')
        #fixed_words = str(word[:hyphen_position]) + ",-," + str(word[(hyphen_position+1):]) # does not work, as single comma entries are later split into two empty strings
        fixed_words = []
        fixed_words.append(word[:hyphen_position])
        fixed_words.append("-")
        fixed_words.append(word[(hyphen_position+1):])
        return fixed_words
    else:
        print("Warning: " + str(word) + " contains a hypthen, but is not detected (or treated) as a hyphened compound word")

for index, word, ner in gs_df.itertuples(index=True):
    if "-" in word:
        # returns hyphened compound words as list of words (incl. hyphen)
        fixed_word = untangle_hyphened(word)
        gs_df.at[index, "original_word"] = fixed_word

# split list values in separate rows
gs_df = gs_df.assign(original_word=gs_df['original_word']).explode('original_word')
'''

'''
# When lists are already in the column
df = pd.DataFrame({'var1': [['a','b','c'], 'd'], 'var2': [1, 2]})
df.assign(var1=df['var1']).explode('var1')
'''