The annotation was done using [Doccano](https://github.com/doccano/doccano).

The raw texts used for the annotation can be found in `data_overlap_manual_collection/original_texts`.

We let two people annotate all 12 novels and agree on a common version. We ensured that there was no communication between the two annotators during the initial annotation process. 

The files downloaded from Doccano after the final annotation can be found in the folder `doccano_files`. 

The gold standard TSV files can be found in the folder `new_gold_standard`. They follow the simply structure of one entity and entity type per row.

-----------

The folder `original_data` holds the files that we downloaded directly from Doccano. Note:
- all annotations are automatically merged into one file per book
- when PERSON and PERX entities overlap, one of them is added as a comment. The annotators did not always type the repetitive overlapping entities from the comments. However when the comments are manually added as a second layer to the files, all occurrences of the overlapping entities are added