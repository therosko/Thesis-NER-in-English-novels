##############################################################
# Fixing missmatches in parsing of doccano output
# The script also does not claim to be a reusable solution,
# instead it merely adapts the doccano output files to correspond 
# to the entity split style of LitBank.
# Input: pandas dataframe, filename
# Output: pandas dataframe
##############################################################

import pandas as pd

def fix_ner_label(df):
    '''
    The exported files contain a label represented by a number (id). 
    We replace those ids with the respective text of the label.
    '''
    for label in ['B-3','B-4','B-5','B-6','B-7','B-8','B-9','B-10','B-11','B-12','B-13','B-14']:
        df = df.replace([label], 'B-PERSON')
    for label in ['I-3','I-4','I-5','I-6','I-7','I-8','I-9','I-10','I-11','I-12','I-13','I-14']:
        df = df.replace([label], 'I-PERSON')
    for label in ['B-18','B-19','B-20','B-21','B-22','B-23','B-24','B-25','B-26','B-27','B-28','B-29']:
        df = df.replace([label], 'B-PERX')
    for label in ['I-18','I-19','I-20','I-21','I-22','I-23','I-24','I-25','I-26','I-27','I-28','I-29']:
        df = df.replace([label], 'I-PERX')
    return df

def fix_titles(df):
    ''' 
    titles such as "Mr." are separated into "Mr" and "." . 
    We correct this by merging them together. #St.
    '''
    list_titles_Mr = df[df['original_word']=='Mr'].index.tolist()
    list_titles_Mrs = df[df['original_word']=='Mrs'].index.tolist()
    list_titles_St = df[df['original_word']=='St'].index.tolist()
    list_titles_Dr = df[df['original_word']=='Dr'].index.tolist()

    list_titles = list_titles_Mr + list_titles_Mrs + list_titles_St + list_titles_Dr #todo
    list_to_drop = []
    for i in list_titles:
        if df['original_word'].iloc[i+1] == '.':
            current_title = df.loc[i,'original_word']
            df.loc[i,'original_word'] = current_title + "."
            list_to_drop.append(i+1)
        else:
            continue
    df = df.drop(df.index[[list_to_drop]])
    return df

def add_layer(df):
    '''
    For the cases where a token is both a (part of) PERSON and PERX entity, 
    we need a separate column, in which we can add the second entity type.
    By default the second layer is O.
    '''
    df['m_ner'] = 'O'
    return df

def fix_parsing(df, filename):
    '''
    The parsing sometimes has lead to different tokens, which we fix in this step.
    '''
    list_to_drop = []
    if filename == "AliceInWonderland.jsonl":
        for i in df[df['original_word']=="’"].index.tolist():
            if df['original_word'].iloc[i+1] == 'll':
                df.loc[i,'original_word'] = "’ll"
                list_to_drop.append(i+1)
            elif df['original_word'].iloc[i+1] == 've':
                df.loc[i,'original_word'] = "’ve"
                list_to_drop.append(i+1)
            elif df['original_word'].iloc[i+1] == 's':
                df.loc[i,'original_word'] = "’s"
                list_to_drop.append(i+1)
            elif df['original_word'].iloc[i-1] == 'Ma' and df['original_word'].iloc[i+1] == 'am':
                df.loc[i,'original_word'] = "Ma’am"
                list_to_drop.append(i-1)
                list_to_drop.append(i+1)
            elif df['original_word'].iloc[i+1] == 're':
                df.loc[i,'original_word'] = "’re"
                list_to_drop.append(i+1)
            elif df['original_word'].iloc[i+1] == 'm':
                df.loc[i,'original_word'] = "’m"
                list_to_drop.append(i+1)
            else:
                continue
        for i in df[df['original_word']=="wouldn"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["would","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="couldn"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["could","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="didn"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["did","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="thing."].index.tolist():
            df.loc[i,'original_word'] = "thing"
            df.loc[i+1,'original_word'] = "."
    elif filename == "Emma.jsonl":
        for i in df[df['original_word']=="_them_"].index.tolist():
            fixed_words = ["_","them","_"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="consciousness."].index.tolist():
            fixed_words = ["consciousness","."]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="large."].index.tolist():
            fixed_words = ["large","."]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="_We_"].index.tolist():
            fixed_words = ["_","We","_"]
            df.loc[i,'original_word'] = fixed_words
    elif filename == "Frankenstein.jsonl":
        list_issues = df[df['original_word']=="R"].index.tolist()
        for i in list_issues:
            if df['original_word'].iloc[i+1] == '.':
                df.loc[i,'original_word'] = "R."
                list_to_drop.append(i+1)
            else:
                continue
    elif filename == "DavidCopperfield.jsonl":
        for i in df[df['original_word']=="o"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 'clock':
                df.loc[i,'original_word'] = "o’clock"
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="don"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["do","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="Don"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["Do","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="’"].index.tolist():
            if df['original_word'].iloc[i+1] == 's':
                df.loc[i,'original_word'] = "’s"
                list_to_drop.append(i+1)
            else:
                continue
        for i in df[df['original_word']=="couldn"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["could","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
    elif filename == "PrideAndPrejudice.jsonl":
        for i in df[df['original_word'].str.match('_[a-zA-Z]+_')==True].index.tolist():
            fixed_words = ["_",df.loc[i,'original_word'][1:-1],"_"]
            df.loc[i,'original_word'] = fixed_words
    elif filename == "Ulysses.jsonl":
        for i in df[df['original_word'].str.match('—[a-zA-Z]+')==True].index.tolist():
            fixed_words = ["—",df.loc[i,'original_word'][1:]]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="’"].index.tolist():
            if df['original_word'].iloc[i+1] == 's':
                df.loc[i,'original_word'] = "’s"
                list_to_drop.append(i+1)
            else:
                continue
        for i in df[df['original_word']=="hasn"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["has","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="isn"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["is","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="can"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["ca","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="don"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["do","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="Isn"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["Is","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="’"].index.tolist():
            if df['original_word'].iloc[i+1] == 're':
                df.loc[i,'original_word'] = "’re"
                list_to_drop.append(i+1)
            elif df['original_word'].iloc[i+1] == 'm':
                df.loc[i,'original_word'] = "’m"
                list_to_drop.append(i+1)
            elif df['original_word'].iloc[i+1] == 'll':
                df.loc[i,'original_word'] = "’ll"
                list_to_drop.append(i+1)
            else:
                continue
        for i in df[df['original_word']=="won"].index.tolist():
            if df['original_word'].iloc[i+1] == '’' and df['original_word'].iloc[i+2] == 't':
                fixed_words = ["wo","n’t"]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
                list_to_drop.append(i+2)
            else:
                continue
        for i in df[df['original_word']=="...."].index.tolist():
            if df['original_word'].iloc[i+1] == 'He':
                df.loc[i,'original_word'] = "..."
            else:
                continue
        for i in df[df['original_word']=="g"].index.tolist():
            if df['original_word'].iloc[i+1] == '.':
                df.loc[i,'original_word'] = "g."
                list_to_drop.append(i+1)
            else:
                continue
        for i in df[df['original_word']=="p"].index.tolist():
            if df['original_word'].iloc[i+1] == '.':
                df.loc[i,'original_word'] = "p."
                list_to_drop.append(i+1)
            else:
                continue
        for i in df[df['original_word']=="i"].index.tolist():
            if df['original_word'].iloc[i+1] == '.':
                df.loc[i,'original_word'] = "i."
                list_to_drop.append(i+1)
            else:
                continue
    elif filename == "HuckleberryFinn.jsonl":
        for i in df[df['original_word']=="sumf'n"].index.tolist():
            if df['original_word'].iloc[i+1] == '.':
                fixed_words = ["sumf","'","n."]
                df.loc[i,'original_word'] = fixed_words
                list_to_drop.append(i+1)
            else:
                continue
    elif filename == "Dracula.jsonl":
        for i in df[df['original_word']=="_3"].index.tolist():
            fixed_words = ["_","3"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="Bistritz._"].index.tolist():
            fixed_words = ["Bistritz",".","_"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="P"].index.tolist():
            if df['original_word'].iloc[i+1] == '.':
                df.loc[i,'original_word'] = "P."
                list_to_drop.append(i+1)
            else:
                continue
        for i in df[df['original_word']=="_Mem._"].index.tolist():
            fixed_words = ["_","Mem",".","_"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="``"].index.tolist():
            df.loc[i,'original_word'] = '"'
        for i in df[df['original_word']=="''"].index.tolist():
            df.loc[i,'original_word'] = '"'
        for i in df[df['original_word']=="Friend."].index.tolist():
            fixed_words = ["Friend","."]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="_4"].index.tolist():
            fixed_words = ["_","4"]
            df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word']=="May._"].index.tolist():
            fixed_words = ["May",".","_"]
            df.loc[i,'original_word'] = fixed_words
    elif filename == "VanityFair.jsonl":
        for i in df[df['original_word']=="``"].index.tolist():
            df.loc[i,'original_word'] = '"'
        for i in df[df['original_word']=="''"].index.tolist():
            df.loc[i,'original_word'] = '"'
    elif filename == "OliverTwist.jsonl":
        for i in df[df['original_word'].str.match("'[a-zA-Z]+")==True].index.tolist():
            if df['original_word'].iloc[i] in ["'s","'em","'ll","'S"]:
                continue
            else:
                fixed_words = ["'",df.loc[i,'original_word'][1:]]
                df.loc[i,'original_word'] = fixed_words
        for i in df[df['original_word'].str.match('_[a-zA-Z]+_')==True].index.tolist():
            fixed_words = ["_",df.loc[i,'original_word'][1:-1],"_"]
            df.loc[i,'original_word'] = fixed_words
    elif filename == "TheCallOfTheWild.jsonl":
        for i in df[df['original_word']=="'m"].index.tolist():
            if df['original_word'].iloc[i-1] == "'":
                list_to_drop.append(i-1)
        for i in df[df['original_word']=="'Frisco"].index.tolist():
            fixed_words = ["'","Frisco"]
            df.loc[i,'original_word'] = fixed_words
    df = df.drop(df.index[[list_to_drop]])
    df = df.assign(original_word=df['original_word']).explode('original_word')
    df = df.reset_index(drop=True)
    return df

def fix_inconsistencies(df, filename):
    '''
    Fixes the inconsistencies between LitBank and Dekker et al., 
    which originate from the use of the raw texts from LitBank.
    (E.g. occurrence of the tokens "glasses" "!", which does not exist in Dekker et al.)
    '''
    if filename == "MobyDick.jsonl":
        df = df.drop(df.index[[381,382,539]])
        df = df.reset_index(drop=True)
    elif filename == "Frankenstein.jsonl":
        df.loc[2302,'original_word'] = '"'
        df.loc[2308,'original_word'] = '"'
    return df


def fix_all_in_one(df, filename):
    '''
    Run all steps by calling one function
    '''
    df = fix_ner_label(df)
    df = fix_parsing(df, filename)
    df = fix_titles(df)
    df = add_layer(df)
    df = df.reset_index(drop=True)
    df = fix_inconsistencies(df, filename)
    return df

