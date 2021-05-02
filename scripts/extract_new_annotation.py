import json
import pandas as pd
import os
import csv
import nltk
nltk.download('punkt')
# import own script
from modules.hyphens import *
from modules.fix_doccano_output import *
# import adapted version of doccano_transformer
from doccano_transformer.datasets import NERDataset
from doccano_transformer.utils import read_jsonl


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


directory = os.fsencode('/mnt/Git/annotation/original_data')

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".jsonl"): 
        print(filename)
        dataset = read_jsonl(filepath='/mnt/Git/annotation/original_data/'+filename, dataset=NERDataset, encoding='utf-8')
        df_final = pd.DataFrame(columns=['original_word', 'ner'])
        df_an1 = pd.DataFrame(columns=['original_word', 'ner'])
        df_an2 = pd.DataFrame(columns=['original_word', 'ner'])
        litbank_filepath = "/mnt/data/gold_standard/overlap/litbank/" + books_mapping.get(str(filename.replace('.jsonl',''))) + ".tsv"
        gs_lb = pd.read_csv(litbank_filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"])
        gs_lb.loc[~gs_lb["gs"].isin(['I-PER','B-PER']), "gs"] = "O"
        for row in dataset.to_conll2003(tokenizer=str.split):
            #final agreement (done with admin user, which is automatically created first)
            if row['user'] == 1:
                row_data = row['data'].splitlines()
                for token_tag in row_data:
                    l_token_tag = token_tag.split("  ")
                    tokens = nltk.word_tokenize(l_token_tag[0])
                    tag = l_token_tag[1]
                    for token in tokens:
                        new_line = {'original_word': token, 'ner': tag}
                        df_final = df_final.append(new_line, ignore_index=True)
            #annotator 1
            elif row['user'] == 2:
                row_data = row['data'].splitlines()
                for token_tag in row_data:
                    l_token_tag = token_tag.split("  ")
                    tokens = nltk.word_tokenize(l_token_tag[0])
                    tag = l_token_tag[1]
                    for token in tokens:
                        new_line = {'original_word': token, 'ner': tag}
                        df_an1 = df_an1.append(new_line, ignore_index=True)
            #annotator 2
            else:
                row_data = row['data'].splitlines()
                for token_tag in row_data:
                    l_token_tag = token_tag.split("  ")
                    tokens = nltk.word_tokenize(l_token_tag[0])
                    tag = l_token_tag[1]
                    for token in tokens:
                        new_line = {'original_word': token, 'ner': tag}
                        df_an2 = df_an2.append(new_line, ignore_index=True)
        # add an second layer with default O to all for the manuall input of comments (overlapping entities)
        df_final = correct_hyphened(df_final)
        df_final = fix_all_in_one(df_final, filename)
        df_an1 = correct_hyphened(df_an1)
        df_an1 = fix_all_in_one(df_an1, filename)
        df_an2 = correct_hyphened(df_an2)
        df_an2 = fix_all_in_one(df_an2, filename)
        # TEST FOR ERRORS
        # FINAL
        try:
            for index, word, ner, m_ner in df_final.itertuples(index=True):
                if word != gs_lb["original_word"].loc[index]:
                    print("Position ", index, " '", word, "' in current is not the same as '", gs_lb["original_word"].loc[index], "'in gs")
                    print(df_final.iloc[index-1:index+4])
                    print(gs_lb.iloc[index-1:index+4])
                    break
        #Note: some original texts are longer than the annotated files, we stop the comparisson at that length
        except KeyError:
            print("Reached end of annotated file. Cropped currect_file.")
            print("Last word ", word, " in line ", index)
            df_final = df_final.truncate(after=index-1)
            pass
        # ANNOTATOR 1
        try:
            for index, word, ner, m_ner in df_an1.itertuples(index=True):
                if word != gs_lb["original_word"].loc[index]:
                    print("Position ", index, " '", word, "' in current is not the same as '", gs_lb["original_word"].loc[index], "'in gs")
                    print(df_an1.iloc[index-1:index+4])
                    print(gs_lb.iloc[index-1:index+4])
                    break
        #Note: some original texts are longer than the annotated files, we stop the comparisson at that length
        except KeyError:
            print("Reached end of annotated file. Cropped currect_file.")
            print("Last word ", word, " in line ", index)
            df_an1 = df_an1.truncate(after=index-1)
            pass
        # ANNOTATOR 2
        try:
            for index, word, ner, m_ner in df_an2.itertuples(index=True):
                if word != gs_lb["original_word"].loc[index]:
                    print("Position ", index, " '", word, "' in current is not the same as '", gs_lb["original_word"].loc[index], "'in gs")
                    print(df_an2.iloc[index-1:index+4])
                    print(gs_lb.iloc[index-1:index+4])
                    break
        #Note: some original texts are longer than the annotated files, we stop the comparisson at that length
        except KeyError:
            print("Reached end of annotated file. Cropped currect_file.")
            print("Last word ", word, " in line ", index)
            df_an2 = df_an2.truncate(after=index-1)
            pass
        n+=1
        outpath = "/mnt/Git/annotation/formatted_annotated_data/" + filename.replace('.jsonl','')
        df_final.to_csv(outpath+'_final.tsv', sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)
        df_an1.to_csv(outpath+'_1.tsv', sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)
        df_an2.to_csv(outpath+'_2.tsv', sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)
    else:
        continue


