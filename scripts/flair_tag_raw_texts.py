# this script partially uses sample code provided in the official Flair repository

from flair.data import Sentence #used for sentence
from flair.models import SequenceTagger
from flair.tokenization import SegtokSentenceSplitter
import os
import csv

'''#todo iterate over files
#passed_variable = sys.argv[1]
passed_variable = 'AliceInWonderland'
passed_variable = 'DavidCopperfield'
path = "/mnt/data/gold_standard/overlap/original_texts/" + str(passed_variable) + ".txt"
#todo read from path'''

directory = os.fsencode('/mnt/data/gold_standard/overlap/original_texts/')

# The model key is taken from 'https://huggingface.co/flair/ner-english-large' and automatically downloads the newest version
tagger = SequenceTagger.load('ner-large')
# initialize sentence splitter
splitter = SegtokSentenceSplitter() 

#sentences = Sentence('So she was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.')
#text = 'So Alice was considering in her own mind (as well as she could, for the hot day made her feel very sleepy and stupid), whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her.'


for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".txt"): 
        with open("/mnt/data/gold_standard/overlap/original_texts/"+filename,'r') as file:
            text = file.read()
        # use splitter to split text into list of sentences
        sentences = splitter.split(text)
        # predict tags for sentences
        tagger.predict(sentences)
        # write tagged tokens to file
        with open("/mnt/flair/" + filename.replace('.txt','.tsv'), 'a') as w_file:
            tsv_writer = csv.writer(w_file, delimiter='\t')
            tsv_writer.writerow(['original_word', 'ner', 'confidence'])
            for sentence in sentences:
                for token in sentence:
                    tag = token.get_tag('ner')
                    #print(f'{str(token).split()[2]} {tag.value} {round(tag.score,2)}')
                    tsv_writer.writerow([str(token).split()[2], tag.value, str(round(tag.score,2))])

'''
for sentence in sentences:
    for token in sentence:
        tag = token.get_tag('ner')
        print(f'{str(token).split()[2]} {tag.value} {round(tag.score,2)}')

with open("/mnt/flair/" + passed_variable + ".tsv", 'a') as w_file:
    w_file.write('original_word ner confidence\n')
    for sentence in sentences:
        for token in sentence:
            tag = token.get_tag('ner')
            #print(f'{str(token).split()[2]} {tag.value} {round(tag.score,2)}')
            w_file.write(str(token).split()[2] + '  ' + tag.value + '   ' + str(round(tag.score,2)) + '\n')
'''

'''
# iterate through sentences and print predicted labels
for sentence in sentences:
    print(sentence.to_tagged_string())
'''