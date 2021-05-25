###################################################################################
# IMPORTANT
# This file contains unfinished code nad pseudocode to be implemented. 
# Issue: The formats of the raw texts used in LitBank and Dekker et al.
# are not the same. There are differences such as punctuation, spelling, etc.
# The currect extraction of overlapping was done manually.
###################################################################################

#################################
# extract gold standard
#################################

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

for filename in "/mnt/data/gold_standard/dekker_et_al":
    filepath = path_to_folder + "/" + filename
    dekkeretal = pd.read_csv(filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"]) 
    dekker_start = dekkeretal['original_word'][:5].tolist()
    filepath2 = "/mnt/data/gold_standard/litbank" + books_mapping.get(filename)
    litbank = pd.read_csv(filepath2, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"]) 

    ###### Find start of matching section
    for index, entity in litbank.itertuples(index=True):
        if entity == dekker_start[0]:
            list_i = 1
            i = index + 1
            while list_i < (len(dekker_start)+1):
                if litbank.iloc[i]['booknlp'] == dekker_start[list_i]:
                    list_i += 1
                    i += 1
                else: 
                    #escape while loop
                    list_i = len(dekker_start) + 1
                    continue
            if list_i == 5:
                #if all entries in the list were the same and list_i reached the end
                break
            else: 
                #no match - continue
                continue

    start_position = index
    # drop all entries before start_position in litbank

    ###### Find end of matching section
    try:
        for index, word, ner in dekkeretal.itertuples(index=True):
            if word != litbank["original_word"].loc[index]:
                print("Position ", index, " '", word, "' in current is not the same as '", litbank["original_word"].loc[index], "'in gs")
                break
    #Note: some original texts are longer than the annotated files, we stop the comparisson at that length
    except KeyError:
        print("Reached end of annotated file. Cropped currect_file.")
        print("Last word ", word, " in line ", index)
        dekkeretal = dekkeretal.truncate(after=index-1)
        pass

    # export to file
    dekkeretal.to_csv(actual_filepath, sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)
    litbank.to_csv(actual_filepath2, sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)

#################################
# extract relevant original text
#################################



