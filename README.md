## Master Thesis: Named Entity Recognition in Novels


## Status Updates
* use data from [Litbank](https://github.com/dbamman/litbank)

raw texts: `/mnt/data/litbank/entities/brat/*.txt`

annotated files: `/mnt/data/litbank/entities/*.tsv` *we are using the entity and only the first level of the annotation (column 1, column 2)*

Note: The entity annotation layer of LitBank covers six of the ACE 2005 categories in text: People (PER), Facilities (FAC), Geo-political entities (GPE), Locations (LOC), Vehicles (VEH), Organizations (ORG)


* `get_setup.sh` steps to be executed within the container. Script can also be called as a whole from inside the container. 
* `init_steps.sh` holds the steps that need to be taken in order to get the required setup. Requirements: [Docker installed](https://docs.docker.com/get-docker/)
* Setup Docker container that fulfills all (current) requirements (Dockerfile, requirements.txt)

The setup can be optimally used in two ways (both describen in `init_steps.sh`): 
* (preffered by me) mount a volume to the container when running (`docker container run -v <path to your folder>:/mnt -it ner /bin/bash`) and develop over VSCode (if working on a remote server, [connect to remote server over SSH ](https://code.visualstudio.com/docs/remote/ssh) ), push and pull from the same local folder
* work directly inside the container and clone this repository in the `/mnt/Git` folder (not permanent, must be repeated every time you run the container)

