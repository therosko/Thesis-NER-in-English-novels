########################################################################################################
## Summary: Gold standard - extract first two columns of each tsv file in a folder and write them to a separate tsv file
## Requires: 
##           - path to the initial tsv files
##           - path to the output directory
########################################################################################################

import os
import csv
# import own script
import modules.hyphens

path_to_annotated_files = "/mnt/data/litbank/entities/tsv"
gs_output_dir = "/mnt/data/gold_standard"

for filename in os.listdir(path_to_annotated_files):
    if filename.endswith(".tsv"): 
        # read file to pandas dataframe; litbank files have 6 detenced columns (based on tabs)
        filepath = path_to_annotated_files + "/" + filename
        # files have different levels and therefore a different number of columns. we only take and name the first two columns
        current_file = pd.read_csv(filepath, sep='\t', quoting=csv.QUOTE_NONE, usecols=[0,1], names=["original_word", "gs"]) 

        # The golden standard treats hyphened compound words such as WAISTCOAT-POCKET as one word instead of three separate. We find and split those for the further analysis
        current_file = correct_hyphened(current_file)

        # write only first two columns (entity and first level of annotation) to a specified folder 
        outpath = gs_output_dir + "/" + filename
        current_file.to_csv(outpath, sep='\t', index=False, encoding='utf-8', quoting=csv.QUOTE_NONE)
        # clean up (not mandatory)
        current_file.drop(current_file.index, inplace=True)