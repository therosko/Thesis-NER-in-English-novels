#!/bin/bash

# run setup script (installs tools and dependencies, gets datasets)
scripts/get_setup.sh





####################todo 
#https://stackoverflow.com/questions/14155669/call-python-script-from-bash-with-argument
#To execute a python script in a bash script you need to call the same command that you would within a terminal. For instance
python3 python_script.py var1 var2

#To access these variables within python you will need
import sys
print sys.argv[0] # prints python_script.py
print sys.argv[1] # prints var1
print sys.argv[2] # prints var2