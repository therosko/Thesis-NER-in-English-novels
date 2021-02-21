##############################################################
# Patch encoding issues to BookNLP output.
# NB: Script is tailored for books annotated by Dekker et al.
# The script also does not claim to fix the encoding issues, 
# instead it merely adapts the gold standard to correspond to 
# the entity split style of BooknLP.
# Input: pandas dataframe
# Output: pandas dataframe
##############################################################
import pandas as pd

def patch_encoding(gs_df):
    # Magician
    gs_df = gs_df[gs_df.original_word != "||"]
    #Tinker Tailor Soldier Spy
    #caution: the Ã is not followed by space, but by something else (couldn't find out what). It has been directly copied from the .gs file
    gs_df["original_word"].replace({'Ã ': 'Ã'}, inplace=True)

    #split words, when necessary (e.g. didnt -> did, nt) also due to encoding issues
    gs_df['original_word'] = gs_df['original_word'].astype('object')
    for index, word, ner in gs_df.itertuples(index=True):
        if word == "didnt":
            fixed_word = ['did','nt']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "aint":
            fixed_word = ['ai','nt']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "dont":
            fixed_word = ['do','nt']
            gs_df.at[index, "original_word"] = fixed_word
        #Alice in Wonderland
        elif word == "Maâ€™am":
            fixed_word = ['Maâ','€','™', 'am']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "``'":
            fixed_word = ["``","'"]
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "```":
            fixed_word = ["``","`"]
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "'''":
            fixed_word = ["'","''"]
            gs_df.at[index, "original_word"] = fixed_word
        #David Copperfield
        elif word == "oâ€™clock":
            fixed_word = ['oâ','€','™', 'clock']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "maâ€™am":
            fixed_word = ['maâ','€','™', 'am']
            gs_df.at[index, "original_word"] = fixed_word
        #Dracula
        elif word == "calÃ¨che":
            fixed_word = ['calÃ','¨','che']
            gs_df.at[index, "original_word"] = fixed_word
        #Gardens Of The Moon
        elif word == "1158-1194":
            fixed_word = ['1158','-','1194']
            gs_df.at[index, "original_word"] = fixed_word
        #Magician
        elif word == "â€¢":
            fixed_word = ['â','€','¢']
            gs_df.at[index, "original_word"] = fixed_word
        #Oliver Twist
        elif word == "B.":
            fixed_word = ['B','.']
            gs_df.at[index, "original_word"] = fixed_word
        #The Color of Magic #todo why is this not detected by hyphen module?!
        elif word == "of-underground-spirits":
            fixed_word = ['of','-','underground','-','spirits']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "underground-spirits":
            fixed_word = ['underground','-','spirits']
            gs_df.at[index, "original_word"] = fixed_word
        #The Count of Monte Cristo
        elif word == "ChÃ¢teau":
            fixed_word = ['ChÃ','¢','teau']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "dâ€™If":
            fixed_word = ['dâ','€','™', 'If']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "PomÃ¨gue":
            fixed_word = ['PomÃ','¨','gue']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "RÃ©serve":
            fixed_word = ['RÃ','©','serve']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "DantÃ¨s":
            fixed_word = ['DantÃ','¨','s']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "manÅ“uvre":
            fixed_word = ['manÅ','“','uvre']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "MercÃ©dÃ¨s":
            fixed_word = ['MercÃ','©','dÃ','¨','s']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "CanebiÃ¨re":
            fixed_word = ['CanebiÃ','¨','re']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "dâ€™OrlÃ©ans":
            fixed_word = ['dâ','€','™','OrlÃ','©','ans']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "PhocÃ©ens":
            fixed_word = ['PhocÃ','©','ens']
            gs_df.at[index, "original_word"] = fixed_word
        #The Lies Of Locke Lamora
        elif word == "Locke/Fehrwight":
            fixed_word = ['Locke','/','Fehrwight']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "he/they":
            fixed_word = ['he','/','they']
            gs_df.at[index, "original_word"] = fixed_word
        #The Name of the Wind
        elif word == "â€™n":
            fixed_word = ['â','€','™','n']
            gs_df.at[index, "original_word"] = fixed_word
        #The Painted Man
        elif word == "â€™em":
            fixed_word = ['â','€','™','em']
            gs_df.at[index, "original_word"] = fixed_word
        #The Three Musketeers 
        elif word == "dâ€™Artagnan":
            fixed_word = ['dâ','€','™','Artagnan']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "Dâ€™Artagnan":
            fixed_word = ['Dâ','€','™','Artagnan']
            gs_df.at[index, "original_word"] = fixed_word
        #Tinker Tailor Soldier Spy
        elif word == "dictÃ©e":
            fixed_word = ['dictÃ','©','e']
            gs_df.at[index, "original_word"] = fixed_word
        elif word == "TouchÃ©":
            fixed_word = ['TouchÃ','©']
            gs_df.at[index, "original_word"] = fixed_word
        #Ulysses
        elif word == "i.":
            fixed_word = ['i','.']
            gs_df.at[index, "original_word"] = fixed_word

    # split list values in separate rows
    gs_df = gs_df.assign(original_word=gs_df['original_word']).explode('original_word')
    gs_df = gs_df.reset_index(drop=True)
    return gs_df