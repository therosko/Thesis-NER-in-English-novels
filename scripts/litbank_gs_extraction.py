########################################################################################################
## Summary: Gold standard - extract first two columns of each tsv file in a folder and write them to a separate tsv file
## Requires: 
##           - path to the initial tsv files
##           - path to the output directory
########################################################################################################

import os
import csv
import pandas as pd
# import own script
from hyphens import *

path_to_annotated_files = "/mnt/data/litbank/entities/tsv"
gs_output_dir = "/mnt/data/gold_standard/litbank"

for filename in os.listdir(path_to_annotated_files):
    print("INFO: Current file: ", filename)
    if filename.endswith(".tsv"): 
        # read file to pandas dataframe; litbank files have 6 detenced columns (based on tabs)
        filepath = path_to_annotated_files + "/" + filename

        # files have different levels and therefore a different number of columns. we only take and name the first two columns
        current_original = pd.read_csv(filepath, sep='\t', header=None, quoting=csv.QUOTE_NONE) 
        # create an empty dataframe
        current_file = pd.DataFrame(columns = ['original_word', 'gs']) 
        # move all "widest range entries" (no matter the layer)
        for index in range(0,len(current_original)):
            if "I-PER" in current_original.iloc[index].values:
                new_line = {'original_word': current_original.iloc[index][0], 'gs': "I-PER"}
                current_file = current_file.append(new_line, ignore_index=True)
                continue
            elif "B-PER" in current_original.iloc[index].values:
                new_line = {'original_word': current_original.iloc[index][0], 'gs': "B-PER"}
                current_file = current_file.append(new_line, ignore_index=True)
                continue
            else:
                new_line = {'original_word': current_original.iloc[index][0], 'gs': "O"}
                current_file = current_file.append(new_line, ignore_index=True)
                continue

        # The golden standard treats hyphened compound words such as WAISTCOAT-POCKET as one word instead of three separate. We find and split those for the further analysis
        current_file = correct_hyphened(current_file)

        # write only first two columns (entity and first level of annotation) to a specified folder 
        outpath = gs_output_dir + "/" + filename
        current_file.to_csv(outpath, sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)
        # clean up (not mandatory)
        current_file.drop(current_file.index, inplace=True)
