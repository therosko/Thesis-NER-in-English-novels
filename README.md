## Master Thesis: Named Entity Recognition in Novels

Note to self: run with `docker container run -v /home/ivanova/NER/v_mnt:/mnt -it ner /bin/bash`

## Status Updates
* flattened hyphened words in gold standard (uses old version of Stanford CoreNLP)
* derive differences between booknlp and gold standard, extract false positives and false negatives

--
* use data from [Litbank](https://github.com/dbamman/litbank)

raw texts: `/mnt/data/litbank/entities/brat/*.txt`

annotated files: `/mnt/data/litbank/entities/*.tsv` *we are using the entity and only the first level of the annotation (column 1, column 2)*

Note: The entity annotation layer of LitBank covers six of the ACE 2005 categories in text: People (PER), Facilities (FAC), Geo-political entities (GPE), Locations (LOC), Vehicles (VEH), Organizations (ORG)

* `get_setup.sh` steps to be executed within the container. Script can also be called as a whole from inside the container. 


---------
## How to use

#### Setup and requirements
The standard setup uses [Docker](https://docs.docker.com/get-docker/). Once installed follow the steps:
1. create a folder (e.g. `mkdir v_mnt`), which will be mounted to the container
2. inside of this folder create a directory called Git `mkdir Git`
3. clone this repository inside of the Git directory `git clone <repo_path_here> .` (note: don't forget the dot in the end ;)
4. navigate to the cloned repository `cd Git`. The Dockerfile and requirements.txt are located there.
5. build the docker image `sudo docker build -t ner .`
6. run container with the mounted volume (any of the following works):
* directly from the command line `docker container run -v <path to  folder>/v_mnt:/mnt -it ner /bin/bash`
* (preffered by me) mount a volume to the container when running (`docker container run -v <path to folder>/v_mnt:/mnt -it ner /bin/bash`) and develop over VSCode (if working on a remote server, [connect to remote server over SSH ](https://code.visualstudio.com/docs/remote/ssh) ) (push and pull from the same local folder)

#### Next steps:
The following steps are available in the `get_setup.sh`. Those should be executed within the container. You can run all in one by calling the script itself.
* Data: 
    * We use annotated data from [Litbank](https://github.com/dbamman/litbank) Last commit: *a371cd678701fc98371355b328a1a6c4b58508a3*
* Tools:
    * [BookNLP](https://github.com/dbamman/book-nlp) Last commit: *f58fbdbb018ba8bf2d836b764d0426afa0f7bc8c*. This version of BookNLP uses Stanford CoreNLP v.4.1.0 . 
