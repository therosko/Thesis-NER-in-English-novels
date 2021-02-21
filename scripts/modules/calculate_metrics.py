################################################################################################################################
# calculate metrics for evaluation of tool vs. gold standard
# Input: merged_df, list_correct, list_false_positives, list_false_negatives, path_evaluation, path_fp, path_fn
# Output: appended rows to evaluation, false positives, and false negatives files
################################################################################################################################

def get_metrics(merged_df, list_correct, list_false_positives, list_false_negatives, path_evaluation, path_fp, path_fn, passed_variable):
    # handling zero division error taken from: https://github.com/dice-group/gerbil/wiki/Precision,-Recall-and-F1-measure
    if len(list_correct) == 0 and len(list_false_positives) == 0 and len(list_false_negatives) == 0:
        F_1 = 1
        Precision = 1
        Recall = 0
    elif len(list_correct) == 0 and (len(list_false_positives) > 0 or len(list_false_negatives) > 0):
        F_1 = 0
        Precision = 0
        Recall = 0
    else:
        Precision =  len(list_correct) / (len(list_correct) + len(list_false_positives)) #true positives / (true positives + false positives)
        Recall = len(list_correct) / (len(list_correct) + len(list_false_negatives)) #true positives / (true positives + false negatives)
        F_1 = 1/((1/Precision)+(1/Recall))

    #write reults to file (file with header is created by evaluate_dekkeretal.sh)
    results = str(passed_variable) + "," + str(round(Precision, 4)) + "," + str(round(Recall, 4)) + "," + str(round(F_1, 4)) + "\n"
    with open(path_evaluation,'a') as f:
        f.write(results)

    def get_word(list_of_indices):
        word_list = []
        for index in list_of_indices:
            word_list.append(merged_df.iloc[index]['original_word_x'])
        return word_list

    #writin false positives and false negatives to csv
    with open(path_fp,'a') as f:
        for entity in list_false_positives:
            incorrect = str(passed_variable) + "," + str(entity) + "," + str(get_word(entity)) + "\n"
            f.write(incorrect)

    with open(path_fn,'a') as f:
        for entity in list_false_negatives:
            incorrect = str(passed_variable) + "," + str(entity) + "," + str(get_word(entity)) + "\n"
            f.write(incorrect)