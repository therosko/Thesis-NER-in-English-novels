#################################################### BEGINNING OF SETUP ##############################################################
#pip install KafNafParserPy
#pip install networkx

cd root
#sudo apt install git-all
#Cloning specific comits https://coderwall.com/p/xyuoza/git-cloning-specific-commits
git clone -n https://github.com/dbamman/book-nlp.git
cd book-nlp
git checkout 81d7a31
sudo apt install wget
# sudo apt-get install unzip
# get requirements
wget http://nlp.stanford.edu/software/stanford-corenlp-full-2014-01-04.zip
unzip stanford-corenlp-full-2014-01-04.zip
rm stanford-corenlp-full-2014-01-04.zip
# copy to book-nlp/lib/ 
cp stanford-corenlp-full-2014-01-04/stanford-corenlp-3.3.1-models.jar lib/

cd ..
#requiers Java 1.7+ , JVM 1.7+
wget http://ixa2.si.ehu.es/ixa-pipes/models/ixa-pipes-1.1.1.tar.gz
tar -xf ixa-pipes-1.1.1.tar.gz
rm ixa-pipes-1.1.1.tar.gz

wget https://nlp.stanford.edu/software/stanford-ner-2017-06-09.zip
unzip stanford-ner-2017-06-09.zip 
rm stanford-ner-2017-06-09.zip

# Java 1.8+
wget http://cogcomp.seas.upenn.edu/software/illinois-ner-3.0.23.zip
unzip illinois-ner-3.0.23.zip
rm illinois-ner-3.0.23.zip

wget https://www.clips.uantwerpen.be/conll2002/ner/bin/conlleval.txt

wget https://github.com/gephi/gephi/releases/download/v0.9.2/gephi-0.9.2-linux.tar.gz
tar -xf gephi-0.9.2-linux.tar.gz
rm gephi-0.9.2-linux.tar.gz

git clone https://github.com/Niels-Dekker/Out-with-the-Old-and-in-with-the-Novel.git


###################################################### END OF SETUP ###############################################################
##### Following steps are taken and adapted from: Out-with-the-Old-and-in-with-the-Novel/NER_Experiments/StepsExperiments.txt

cd Out-with-the-Old-and-in-with-the-Novel

# This file contains the steps to obtain the results reported on in Tables 3 & 4 
# Make sure to check the file paths for your setup. 

# Make sure you're in the NER folder 
cd NER_Experiments

# Create the files from which to extract the Gold Standard annotations 
for x in New/*csv ; do tail -n +2 $x | cut -f2- | sort -n | cut -f3,6- > ${x%csv}tsv; done 
for x in Old/*csv ; do tail -n +2 $x | cut -f2- | sort -n | cut -f3,6- > ${x%csv}tsv; done 


# Create the text files to do the automatic annotations on
#for x in New/*.tsv ; do cut -f1 $x |  gsed 's/|//g' > ${x%.tsv}.txt ; done 
for x in New/*.tsv ; do cut -f1 $x |  sed 's/|//g' > ${x%.tsv}.txt ; done 
#for x in Old/*.tsv ; do cut -f1 $x |  gsed 's/|//g' > ${x%.tsv}.txt ; done 
for x in Old/*.tsv ; do cut -f1 $x |  sed 's/|//g' > ${x%.tsv}.txt ; done 



####### IXA-Pipe-NERC 

# Go to the IXA Pipes NERC dir 
cd ../../ixa-pipes-1.1.1

# Run the tagger  
for x in ../Out-with-the-Old-and-in-with-the-Novel/NER_Experiments/New/*.txt ; do cat $x | java -jar ixa-pipe-tok-1.8.5-exec.jar tok -l en --notok | java -jar ixa-pipe-pos-1.5.1-exec.jar tag -m morph-models-1.5.0/en/en-pos-perceptron-autodict01-conll09.bin -lm morph-models-1.5.0/en/en-lemma-perceptron-conll09.bin | java -jar ixa-pipe-nerc-1.6.1-exec.jar tag -m nerc-models-1.6.1/en/combined/en-newsreader-clusters-3-class-muc7-conll03-ontonotes-4.0.bin > ${x%.txt}.naf ; done 
# WARNING: No lemmatizer dictionary available for language en in src/main/resources! # is this normal?
for x in ../Out-with-the-Old-and-in-with-the-Novel/NER_Experiments/Old/*.txt ; do cat $x | java -jar ixa-pipe-tok-1.8.5-exec.jar tok -l en --notok | java -jar ixa-pipe-pos-1.5.1-exec.jar tag -m morph-models-1.5.0/en/en-pos-perceptron-autodict01-conll09.bin -lm morph-models-1.5.0/en/en-lemma-perceptron-conll09.bin | java -jar ixa-pipe-nerc-1.6.1-exec.jar tag -m nerc-models-1.6.1/en/combined/en-newsreader-clusters-3-class-muc7-conll03-ontonotes-4.0.bin > ${x%.txt}.naf ; done 

# Go back to the experiments folder
cd ../Out-with-the-Old-and-in-with-the-Novel/NER_experiments

# NAF2Conll
for x in New/*naf ; do python naf2conllEntities.py $x > ${x%naf}ixa-conll ; done 
for x in Old/*naf ; do python naf2conllEntities.py $x > ${x%naf}ixa-conll ; done 


# MatchGS2Conll
for x in Old/*tsv ; do python matchGStoConll.py $x ${x%tsv}ixa-conll > ${x%tsv}ixa-conllout ; done 
for x in New/*tsv ; do python matchGStoConll.py $x ${x%tsv}ixa-conll > ${x%tsv}ixa-conllout ; done 


# Run evaluation script 
for x in Old/*ixa-conllout ; do echo $x ; perl conlleval.pl < $x ; done 
for x in New/*ixa-conllout ; do echo $x ; perl conlleval.pl < $x ; done 

 
# Extract the GS files for the other evaluations 
#for x in New/*ixa-conllout ; do cut -f1,2 -d" " $x  > ${x%ixa-conllout}gs ; done 
for x in New/*ixa-conllout ; do cut -f1,2 -d " " $x  > ${x%ixa-conllout}gs ; done 
#for x in Old/*ixa-conllout ; do cut -f1,2 -d" " $x > ${x%ixa-conllout}gs ; done 
for x in Old/*ixa-conllout ; do cut -f1,2 -d " " $x > ${x%ixa-conllout}gs ; done 



#######  Stanford experiments

# Go to the Stanford NER directory (or set up your classpath so you can call it from anywhere)
cd ../../stanford-ner-2017-06-09 

# Run Stanford NER 
for x in ../Out-with-the-Old-and-in-with-the-Novel/NER_experiments/New/*gs ; do java -mx700m -cp "stanford-ner.jar:lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -testFile $x | gtr "\t" " " | gsed 's/ PERSON/ I-PERSON/g' > ${x%gs}stanfordout ; done 

for x in ../Out-with-the-Old-and-in-with-the-Novel/NER_experiments/Old/*gs ; do java -mx700m -cp "stanford-ner.jar:lib/*" edu.stanford.nlp.ie.crf.CRFClassifier -loadClassifier classifiers/english.all.3class.distsim.crf.ser.gz -testFile $x | gtr "\t" " " | gsed 's/ PERSON/ I-PERSON/g' > ${x%gs}stanfordout ; done 

# Go back to the experiments folder 
cd ../Out-with-the-Old-and-in-with-the-Novel/NER_experiments

# Evaluate 
for x in New/*stanfordout ; do echo $x ; perl conlleval.pl < $x ; done
for x in Old/*stanfordout ; do echo $x ; perl conlleval.pl < $x ; done



##### Illinois NER tagger 


# copy input files to a directory where the Illinois NE tagger can find them 
# first create a directory
mkdir ../../illinois-ner/input_new
mkdir ../../illinois-ner/input_old

# then copy 
for x in New/*.txt ; do cp $x ../../illinois-ner/input_new ; done 
for x in Old/*.txt ; do cp $x ../../illinois-ner/input_old ; done 
 
# also create output dirs
mkdir ../../illinois-ner/output_new
mkdir ../../illinois-ner/output_old

# Go to the Illinois NE tagger directory (or set up your classpath so you can call it from anywhere)
cd ../../illinois-ner 

java -Xmx4g -classpath "dist/*:lib/*:models/*" -Xmx8g edu.illinois.cs.cogcomp.ner.NerTagger -annotate input_new output_new config/ner.properties

java -Xmx4g -classpath "dist/*:lib/*:models/*" -Xmx8g edu.illinois.cs.cogcomp.ner.NerTagger -annotate input_old output_old config/ner.properties

# Go back to the experiments folder 
cd /to/NER_experiments

# Gather the results and put them into a file with the Gold Standard 
for x in ../../illinois-ner/output_old/*txt ; do python illinois2conll.py $x > ${x%txt}illoutput ; done
for x in ../../illinois-ner/output_new/*txt ; do python illinois2conll.py $x > ${x%txt}illoutput ; done 
 
cp ../../illinois-ner/output_old/*illoutput Old/
cp ../../illinois-ner/output_new/*illoutput New/

# Paste with GS 
#for x in New/*gs ; do python gs2illinoisTestFormat.py $x ${x%gs}illoutput | cut -f1,2,4 -d" " > ${x%.gs}*.illconllout ; done
for x in New/*gs ; do python gs2illinoisTestFormat.py $x ${x%gs}illoutput | cut -f1,2,4 -d " " > ${x%.gs}*.illconllout ; done
#for x in Old/*gs ; do python gs2illinoisTestFormat.py $x ${x%gs}illoutput | cut -f1,2,4 -d" " > ${x%.gs}*.illconllout ; done
for x in Old/*gs ; do python gs2illinoisTestFormat.py $x ${x%gs}illoutput | cut -f1,2,4 -d " " > ${x%.gs}*.illconllout ; done

# Compute scores  
for x in New/*illconllout ; do echo $x ; perl conlleval.pl < $x ; done
for x in Old/*illconllout ; do echo $x ; perl conlleval.pl < $x ; done


#note: you never left NEW_experiments
###### BookNLP 
for x in New/*gs ; do python booknlp2gs.py $x path/to/BookNLPOutput/${x%.gs}*.tokens > ${x%gs}booknlpoutput ; done 

for x in Old/*gs ; do python booknlp2gs.py $x path/to/BookNLPOutput/${x%.gs}*.tokens > ${x%gs}booknlpoutput ; done 

for x in New/*booknlpoutput ; do echo $x ; perl conlleval.pl < $x ; done
for x in Old/*booknlpoutput ; do echo $x ; perl conlleval.pl < $x ; done

###### BookNLP co-ref
for each novel in collection run below command (replace {variable} by desired input and output):

./runjava novels/BookNLP -doc data/originalTexts/{novel_to_evaluate.txt} -printHTML -p data/output/{novel_logger} -tok data/tokens/{novel_to_evaluate.tokens} -f
