##############################################################
# Fixing missmatches in parsing of Flair output
# The script also does not claim to be usable for any given text, 
# instead it merely adapts the Flair output files to correspond 
# to the entity split style of LitBank.
# Input: pandas dataframe, filename
# Output: pandas dataframe
##############################################################

import pandas as pd

def patch_flair(df, filename):
    '''
    The parsing sometimes has lead to different tokens, which we fix in this step.
    '''
    list_to_drop = []

    for i in df[df['original_word'].str.endswith('.’')==True].index.tolist():
        fixed_words = [df.loc[i,'original_word'][:-2],".","’"]
        df.loc[i,'original_word'] = fixed_words
    for i in df[df['original_word'].str.endswith('.')==True].index.tolist():
        if df.loc[i,'original_word'] not in ['.',"Mr.", "Mrs.", "St.", "Dr.","P.","M.","R.","P.S.",'...',"g.","p.","i."]:
            fixed_words = [df.loc[i,'original_word'][:-1],"."]
            df.loc[i,'original_word'] = fixed_words
        elif df.loc[i-1,'original_word'] == '...' and df.loc[i+1,'original_word'] == "He":
            list_to_drop.append(i)
        else:
            pass
    for i in df[df['original_word'].str.endswith('’')==True].index.tolist():
        if df.loc[i,'original_word'] != '’':
            fixed_words = [df.loc[i,'original_word'][:-1],"’"]
            df.loc[i,'original_word'] = fixed_words
        else:
            pass
    for i in df[df['original_word'].str.endswith('--')==True].index.tolist():
        if df.loc[i,'original_word'][:-2] in ["?","’",":","_","!",";",","] and df.loc[i,'original_word'] != "--":
            fixed_words = [df.loc[i,'original_word'][:-2],"--"]
            df.loc[i,'original_word'] = fixed_words
    for i in df[df['original_word'].str.endswith("'")==True].index.tolist():
        if df.loc[i,'original_word'] != "'":
            fixed_words = [df.loc[i,'original_word'][:-1],"'"]
            df.loc[i,'original_word'] = fixed_words
        else:
            pass
    for i in df[df['original_word']==';”'].index.tolist():
        fixed_words = [';','”']
        df.loc[i,'original_word'] = fixed_words
    for i in df[df['original_word']=="cannot"].index.tolist():
        fixed_words = ["can","not"]
        df.loc[i,'original_word'] = fixed_words
    for i in df[df['original_word']=="'"].index.tolist():
            if df['original_word'].iloc[i+1] in ["m"]:
                df.loc[i,'original_word'] = "'"+ df.loc[i+1,'original_word']
                list_to_drop.append(i+1)

    #ALICE IN WONDERLAND
    if filename == "AliceInWonderland.tsv":
        for i in df[df['original_word']=="‘--"].index.tolist():
            fixed_words = ["‘","--"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="[‘"].index.tolist():
            fixed_words = ["[","‘"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']==",)"].index.tolist():
            fixed_words = [",",")"]
            df.loc[i,'original_word'] = fixed_words

    # FRANKENSTEIN
    elif filename == "Frankenstein.tsv":
        for i in df[df['original_word']=='""""'].index.tolist():
            if df['original_word'].iloc[i+1] in ['What']:
                df.loc[i,'original_word'] = '"'
            else:
                continue
        for i in df[df['original_word']=='"!"""'].index.tolist():
            fixed_words = ["!",'"']
            df.loc[i,'original_word'] = fixed_words

    #PRIDE AND PREJUDICE
    elif filename == "PrideAndPrejudice.tsv":
        for i in df[df['original_word']==',”'].index.tolist():
            fixed_words = [',','”']
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=='“_'].index.tolist():
            fixed_words = ['“','_']
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=='_.”'].index.tolist():
            fixed_words = ['_','.','”']
            df.loc[i,'original_word'] = fixed_words

    #HUCKLEBERRY FINN
    elif filename == "HuckleberryFinn.tsv":
        for i in df[df['original_word']=="cannot"].index.tolist():
            fixed_words = ["can","not"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="sumf'n"].index.tolist():
            if df['original_word'].iloc[i+1] == '.':
                fixed_words = ["sumf","'","n."]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
            else:
                continue
        for i in df[df['original_word']=="more'n"].index.tolist():
            fixed_words = ["more","'n"]
            df.loc[i,'original_word'] = fixed_words

    #DRACULA
    elif filename == "Dracula.tsv":
        for i in df[df['original_word']=="_)"].index.tolist():
            fixed_words = ["_",")"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="(_"].index.tolist():
            fixed_words = ["(","_"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="_--"].index.tolist():
            fixed_words = ["_","--"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']==":--"].index.tolist():
            fixed_words = [":","--"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="P"].index.tolist():
            if df['original_word'].iloc[i+1] == '.':
                df.loc[i,'original_word'] = "P."
                list_to_drop.append(i+1)
            else:
                continue
        for i in df[df['original_word']=='""""'].index.tolist():
            if df['original_word'].iloc[i+1] in ['paprika','mamaliga','impletata']:
                df.loc[i,'original_word'] = '"'
            else:
                continue
        for i in df[df['original_word']=='""""'].index.tolist():
            df.loc[i,'original_word'] = '"'
        for i in df[df['original_word']=='","""'].index.tolist():
            if df['original_word'].iloc[i+1] in ['and','I']:
                fixed_words = [",",'"']
                df.loc[i,'original_word'] = fixed_words
            else:
                continue

    #VANITY FAIR
    elif filename == "VanityFair.tsv":
        for i in df[df['original_word']=='""""'].index.tolist():
            df.loc[i,'original_word'] = '"'
        for i in df[df['original_word']=='","""'].index.tolist():
            fixed_words = [",",'"']
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=='"?"""'].index.tolist():
            fixed_words = ["?",'"']
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=='"!"""'].index.tolist():
            fixed_words = ["!",'"']
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="'"].index.tolist():
            if df['original_word'].iloc[i+1] == "tis":
                df.loc[i,'original_word'] = "'t"
                df.loc[i+1,'original_word'] = "is"

    #OLIVER TWIST
    elif filename == "OliverTwist.tsv":
        for i in df[df['original_word']=="'"].index.tolist():
            if df['original_word'].iloc[i+1] in ["s","em","ll","S"]:
                df.loc[i,'original_word'] = "'"+ df.loc[i+1,'original_word']
                list_to_drop.append(i+1)
        for i in df[df['original_word']=="TWIST'S"].index.tolist():
            fixed_words = ["TWIST","'S"]
            df.loc[i,'original_word'] = fixed_words

    #THE CALL OF THE WILD
    elif filename == "TheCallOfTheWild.tsv":
        for i in df[df['original_word']==',”'].index.tolist():
            fixed_words = [',','”']
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="'"].index.tolist():
            if df['original_word'].iloc[i+1] in ["'m"]:
                list_to_drop.append(i)
        for i in df[df['original_word'].str.endswith('--”')==True].index.tolist():
            fixed_words = ['--','”']
            df.loc[i,'original_word'] = fixed_words
        
    df = df.drop(df.index[[list_to_drop]])
    df = df.assign(original_word=df['original_word']).explode('original_word')
    df = df.reset_index(drop=True)
    if filename == "MobyDick.tsv":
        df = df.drop(df.index[[381,382,539]])
        df = df.reset_index(drop=True)
    return df