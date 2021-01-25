### make sure that the following steps are ran directly in the container
# if you haven't mounted a volume with the git repository, clone the repo here
#cd /mnt
#mkdir Git
#git clone <repo_path_here> .

################################################
######## Those steps are already covered by the mount. I have already cloned the repo in /usr/data. However the final version on Git will be without it. Therefore the following steps will be importat to follow.
mkdir /mnt/data
# get data from Litbank
echo "Cloning Litbank (raw and annotated dataset collection)"
cd /mnt/data
git clone https://github.com/dbamman/litbank.git #last commit https://github.com/dbamman/litbank/commit/a371cd678701fc98371355b328a1a6c4b58508a3 
################################################
# create output folder
mkdir /mnt/data/gold_standard
echo "Converting 4-level annotated data to 1-level gold standard"
#TODO test updated pandas version in requirements.txt (rebuild)
python3 /mnt/gs_extraction.py

cd /mnt
# BOOK NLP
# clone repository
echo "Cloning BookNLP"
# last commit https://github.com/dbamman/book-nlp/tree/f58fbdbb018ba8bf2d836b764d0426afa0f7bc8c
git clone https://github.com/dbamman/book-nlp.git
#cd book-nlp
#git reset --hard f58fbdbb018ba8bf2d836b764d0426afa0f7bc8c

cd /mnt
# install dependencies 
# Download and unzip http://nlp.stanford.edu/software/stanford-corenlp-4.1.0.zip
echo "Getting dependencies"
wget http://nlp.stanford.edu/software/stanford-corenlp-4.1.0.zip
unzip stanford-corenlp-4.1.0.zip
rm stanford-corenlp-4.1.0.zip
# copy stanford-corenlp-4.1.0/stanford-corenlp-4.1.0-models.jar to the lib/ folder in the current working directory
cp stanford-corenlp-4.1.0/stanford-corenlp-4.1.0-models.jar book-nlp/lib/

# navigate to book-nlp
cd /mnt/book-nlp
echo "Running BookNLP"
# run tool over Oliver Twist (already available in the repository)
./runjava novels/BookNLP -doc data/originalTexts/dickens.oliver.pg730.txt -printHTML -p data/output/dickens -tok data/tokens/dickens.oliver.tokens -f
# run on litbank
./runjava novels/BookNLP -doc /mnt/data/litbank/entities/brat/6053_evelina_or_the_history_of_a_young_ladys_entrance_into_the_world_brat.txt -p data/tokens/ -tok data/tokens/test.tokens -f

echo "Comparing BookNLP to gold standard"
python3 processing_BookNLP.py
