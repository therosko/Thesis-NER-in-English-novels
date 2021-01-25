### initial steps to be ran first (outside docker container)
#cd <to the folder with the image>
# build docker image
#sudo docker build -t ner .
# run container in interactive mode with mounted volume
# the mount enables easy remote use with VSCode over SSH and mounts a clone of the Git repo
docker container run -v /home/ivanova/NER/v_mnt:/mnt -it ner /bin/bash
# run container in interactive mode
#docker container run -it ner /bin/bash
# clone Git repository inside and use directly in the container (without mount)
#git clone <add path here>