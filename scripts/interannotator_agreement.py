from disagree import metrics
import csv
import pandas as pd
import os
'''
df = pd.DataFrame(test_annotations)
labels=[0,1]
mets = metrics.Metrics(df, labels)
cohens = mets.cohens_kappa(ann1="b", ann2="c")
print("Cohen's kappa: {:.2f}".format(cohens))
'''
print('Novel & PERSON label & PERX label \\\ ')
directory = os.fsencode('/mnt/Git/annotation/gs')
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith("_1.tsv"): 
        #print(filename)
        annotator_1 = "/mnt/Git/annotation/gs/" + str(filename)
        annotator_2 = "/mnt/Git/annotation/gs/" + str(filename.replace('_1.tsv','_2.tsv'))
        ######
        # read annotated datasets of annotator_1
        gs_new_1 = pd.read_csv(annotator_1, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1,2])
        # extract only PERSON labels (following CoNLL-2003 guidelines)
        gs_new_conll_1 = gs_new_1.copy()
        gs_new_conll_1['a'] = "O"
        for item in ['B-PERSON', 'I-PERSON']:
            gs_new_conll_1['a'][gs_new_conll_1['ner'].str.contains(item)] = item
            gs_new_conll_1['a'][gs_new_conll_1['m_ner'].str.contains(item)] = item
        gs_new_conll_1.loc[gs_new_conll_1["a"].isin(['B-PERSON']), "a"] = "B-PER"
        gs_new_conll_1.loc[gs_new_conll_1["a"].isin(['I-PERSON']), "a"] = "I-PER"
        del gs_new_conll_1['ner']
        del gs_new_conll_1['m_ner']
        # extract to a new column both labels person and perx (extension, taken from the LitBank annotation guidelines)
        gs_new_1['a'] = "O" 
        for item in ['B-PERSON', 'I-PERSON','B-PERX','I-PERX']:
            gs_new_1['a'][gs_new_1['ner'].str.contains(item)] = item
            gs_new_1['a'][gs_new_1['m_ner'].str.contains(item)] = item
        gs_new_1.loc[gs_new_1["a"].isin(['B-PERSON','B-PERX']), "a"] = "B-PER"
        gs_new_1.loc[gs_new_1["a"].isin(['I-PERSON','I-PERX']), "a"] = "I-PER"
        del gs_new_1['ner']
        del gs_new_1['m_ner']
        ######
        # read annotated datasets of annotator_2
        gs_new_2 = pd.read_csv(annotator_2, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1,2])
        # extract only PERSON labels (following CoNLL-2003 guidelines)
        gs_new_conll_2 = gs_new_2.copy()
        gs_new_conll_2['b'] = "O"
        for item in ['B-PERSON', 'I-PERSON']:
            gs_new_conll_2['b'][gs_new_conll_2['ner'].str.contains(item)] = item
            gs_new_conll_2['b'][gs_new_conll_2['m_ner'].str.contains(item)] = item
        gs_new_conll_2.loc[gs_new_conll_2["b"].isin(['B-PERSON']), "b"] = "B-PER"
        gs_new_conll_2.loc[gs_new_conll_2["b"].isin(['I-PERSON']), "b"] = "I-PER"
        del gs_new_conll_2['ner']
        del gs_new_conll_2['m_ner']
        # extract to a new column both labels person and perx (extension, taken from the LitBank annotation guidelines)
        gs_new_2['b'] = "O" 
        for item in ['B-PERSON', 'I-PERSON','B-PERX','I-PERX']:
            gs_new_2['b'][gs_new_2['ner'].str.contains(item)] = item
            gs_new_2['b'][gs_new_2['m_ner'].str.contains(item)] = item
        gs_new_2.loc[gs_new_2["b"].isin(['B-PERSON','B-PERX']), "b"] = "B-PER"
        gs_new_2.loc[gs_new_2["b"].isin(['I-PERSON','I-PERX']), "b"] = "I-PER"
        del gs_new_2['ner']
        del gs_new_2['m_ner']

        merged_conll = pd.merge(gs_new_conll_1, gs_new_conll_2, left_index=True, right_index=True)
        del merged_conll['original_word_x']
        del merged_conll['original_word_y']
        labels=['O','B-PER','I-PER']
        mets = metrics.Metrics(merged_conll, labels)
        cohens_conll = mets.cohens_kappa(ann1="a", ann2="b")
        #print("Cohen's kappa: {:.2f}".format(cohens))

        merged_ext = pd.merge(gs_new_1, gs_new_2, left_index=True, right_index=True)
        del merged_ext['original_word_x']
        del merged_ext['original_word_y']
        labels=['O','B-PER','I-PER']
        mets = metrics.Metrics(merged_ext, labels)
        cohens_ext = mets.cohens_kappa(ann1="a", ann2="b")
        #print("Cohen's kappa: {:.2f}".format(cohens))

        print("{} & {:.2f} & {:.2f} \\\ ".format(str(filename.replace('_1.tsv','')), cohens_conll, cohens_ext))
        #'{0} in {1}'.format(unicode(self.author,'utf-8'),  unicode(self.publication,'utf-8'))


'''
merged_conll = pd.merge(gs_new_conll_1, current_file, left_index=True, right_index=True)
del merged_conll['original_word_y']






################################################################################################
annotator_1 = "/mnt/Git/annotation/gs/Dracula_1.tsv"
annotator_2 = "/mnt/Git/annotation/gs/Dracula_2.tsv"
######
# read annotated datasets of annotator_1
gs_new_1 = pd.read_csv(annotator_1, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1,2])
# extract only PERSON labels (following CoNLL-2003 guidelines)
gs_new_conll_1 = gs_new_1.copy()
gs_new_conll_1['a'] = "O"
for item in ['B-PERSON', 'I-PERSON']:
    gs_new_conll_1['a'][gs_new_conll_1['ner'].str.contains(item)] = item
    gs_new_conll_1['a'][gs_new_conll_1['m_ner'].str.contains(item)] = item
gs_new_conll_1.loc[gs_new_conll_1["a"].isin(['B-PERSON']), "a"] = "B-PER"
gs_new_conll_1.loc[gs_new_conll_1["a"].isin(['I-PERSON']), "a"] = "I-PER"
del gs_new_conll_1['ner']
del gs_new_conll_1['m_ner']
# extract to a new column both labels person and perx (extension, taken from the LitBank annotation guidelines)
gs_new_1['a'] = "O" 
for item in ['B-PERSON', 'I-PERSON','B-PERX','I-PERX']:
    gs_new_1['a'][gs_new_1['ner'].str.contains(item)] = item
    gs_new_1['a'][gs_new_1['m_ner'].str.contains(item)] = item
gs_new_1.loc[gs_new_1["a"].isin(['B-PERSON','B-PERX']), "a"] = "B-PER"
gs_new_1.loc[gs_new_1["a"].isin(['I-PERSON','I-PERX']), "a"] = "I-PER"
del gs_new_1['ner']
del gs_new_1['m_ner']
######
# read annotated datasets of annotator_2
gs_new_2 = pd.read_csv(annotator_2, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1,2])
# extract only PERSON labels (following CoNLL-2003 guidelines)
gs_new_conll_2 = gs_new_2.copy()
gs_new_conll_2['b'] = "O"
for item in ['B-PERSON', 'I-PERSON']:
    gs_new_conll_2['b'][gs_new_conll_2['ner'].str.contains(item)] = item
    gs_new_conll_2['b'][gs_new_conll_2['m_ner'].str.contains(item)] = item
gs_new_conll_2.loc[gs_new_conll_2["b"].isin(['B-PERSON']), "b"] = "B-PER"
gs_new_conll_2.loc[gs_new_conll_2["b"].isin(['I-PERSON']), "b"] = "I-PER"
del gs_new_conll_2['ner']
del gs_new_conll_2['m_ner']
# extract to a new column both labels person and perx (extension, taken from the LitBank annotation guidelines)
gs_new_2['b'] = "O" 
for item in ['B-PERSON', 'I-PERSON','B-PERX','I-PERX']:
    gs_new_2['b'][gs_new_2['ner'].str.contains(item)] = item
    gs_new_2['b'][gs_new_2['m_ner'].str.contains(item)] = item
gs_new_2.loc[gs_new_2["b"].isin(['B-PERSON','B-PERX']), "b"] = "B-PER"
gs_new_2.loc[gs_new_2["b"].isin(['I-PERSON','I-PERX']), "b"] = "I-PER"
del gs_new_2['ner']
del gs_new_2['m_ner']


merged_conll = pd.merge(gs_new_conll_1, gs_new_conll_2, left_index=True, right_index=True)
del merged_conll['original_word_x']
del merged_conll['original_word_y']
labels=['O','B-PER','I-PER']
mets = metrics.Metrics(merged_conll, labels)
cohens_conll = mets.cohens_kappa(ann1="a", ann2="b")
#print("Cohen's kappa: {:.2f}".format(cohens))

merged_ext = pd.merge(gs_new_1, gs_new_2, left_index=True, right_index=True)
del merged_ext['original_word_x']
del merged_ext['original_word_y']
labels=['O','B-PER','I-PER']
mets = metrics.Metrics(merged_ext, labels)
cohens_ext = mets.cohens_kappa(ann1="a", ann2="b")
#print("Cohen's kappa: {:.2f}".format(cohens))

print("{} & {} & {:.2f} \\\ ".format(str(filename.replace('_1.tsv','')), cohens_conll, cohens_ext))
#'{0} in {1}'.format(unicode(self.author,'utf-8'),  unicode(self.publication,'utf-8'))
'''