## Master Thesis: "Choose your dataset wisely! The effects of dataset selection on the evaluated performance of named entity recognition tools"
by Rositsa Ivanova

Abstract: 

In recent years, automated named entity recognition (NER) in the domain of English literature has been explored through the creation of domain-specific tools such as BookNLP. For the performance evaluation of such tools, researchers have created domain-specific annotated benchmarking datasets (i.e. gold standards). However, even within the same domain the datasets can address different purposes such as the construction of conversational networks, and coreference resolution for the extraction of social networks. This has led to the creation of gold standards within the domain of English literature, which follow different annotation guidelines and thus do not have a unique definition of the individual named entity types (e.g. person). In this thesis we take a closer look at existing gold standards in the domain of English literature. To better understand the differences between the datasets, we select two existing annotated datasets, which have the same purpose (i.e. coreference resolution), yet follow different annotation guidelines. Further, we create two additional gold standards, one of which follows annotation guidelines created for the domain of English literature, the other being one of the most frequently used annotation guidelines in NER across domains (i.e. CoNLL-2003). We evaluate the performance of two NER tools, one domain-specific and one general-purpose NER tool, using the four gold standards, and analyse the sources for the differences in the measured performance. Lastly, we discuss challenges and opportunities, which we have recognised throughout the annotation and evaluation process.

---------
## How to replicate the experiment

#### Setup and requirements
The standard setup uses [Docker](https://docs.docker.com/get-docker/). Once installed follow the steps:
1. create a folder (`mkdir v_mnt`), which will be mounted to the container
2. inside of this folder create a directory called Git `mkdir Git`
3. clone this repository inside of the Git directory `git clone <repo_path_here> .` (note: don't forget the dot in the end ;)
4. navigate to the cloned repository `cd Git`. The Dockerfile and requirements.txt are located there.
5. build the docker image `sudo docker build -t ner .`
6. run container with the mounted volume (any of the following works):
* directly from the command line `docker container run -v <path to  folder>/v_mnt:/mnt -it ner /bin/bash`
* (preffered by me) mount a volume to the container when running (`docker container run -v <path to folder>/v_mnt:/mnt -it ner /bin/bash`) and develop over VSCode (if working on a remote server, [connect to remote server over SSH ](https://code.visualstudio.com/docs/remote/ssh) ) (push and pull from the same local folder)

#### Next steps:
The following steps are available in the `get_setup.sh`. Those should be executed within the container. You can run all in one by calling the script itself.
* We use *annotated data* from
    * [Litbank](https://github.com/dbamman/litbank) Last commit: *a371cd678701fc98371355b328a1a6c4b58508a3*
    * [Dekker et al.](https://github.com/Niels-Dekker/Out-with-the-Old-and-in-with-the-Novel) Last commit *ad31ce1fa515dceabb8febbaa7aa235f3de47ebd*
    * Two additional annotated datasets created for this work, which can be found in the folder `annotation`
* Tools:
    * [BookNLP](https://github.com/dbamman/book-nlp) Last commit: *f58fbdbb018ba8bf2d836b764d0426afa0f7bc8c*. This version of BookNLP uses Stanford CoreNLP v.4.1.0 . 
    * [Flair](https://github.com/flairNLP/flair) *version 0.8*

--
### More Info:
* use data from [Litbank](https://github.com/dbamman/litbank)

raw texts: `/mnt/data/litbank/entities/brat/*.txt`

annotated files: `/mnt/data/litbank/entities/*.tsv` *we are using the entity and only the first level of the annotation (column 1, column 2)*

Note: The entity annotation layer of LitBank covers six of the ACE 2005 categories in text: People (PER), Facilities (FAC), Geo-political entities (GPE), Locations (LOC), Vehicles (VEH), Organizations (ORG)

* `get_setup.sh` steps to be executed within the container. Script can also be called as a whole from inside the container. 
