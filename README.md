# time-series-basics
Time Series basics - importing, cleaning, printing to csv

Note date files are synthetic data. 

# Usage

For general usage:

python data_import.py --folder_name=${FOLDER_NAME} --output_file=${OUTPUT_FILE_NAME} --sort_key=${SORT_KEY}

FOLDER_NAME: The source path for csv files\
OUTPUT_FILE_NAME: The output file name\
SORT_KEY: The primary file you want to check\

An example of usage:

python data_import.py --folder_name=smallData --output_file=out --sort_key=cgm_small.csv

# Unit test and Functional test

The unit test is included in Functional test .travis.yml\
The .travis.yml also tries different failure cases\

# Benchmarking:

Linear Search:7.160130977630615 seconds\
Binear Search:1.138037919998169 seconds\
Binear Search shows better performance then Linear Search.
