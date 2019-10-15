#!/bin/bash

test -e ssshtest || wget -q https://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest
. ssshtest

run test_pycodestyle pycodestyle *.py
assert_exit_code 0

run test_good_case python data_import.py --folder_name=smallData --output_file=out --sort_key=cgm_small.csv
assert_exit_code 0
rm out_5.csv
rm out_15.csv

run test_bad_input python data_import.py --folder_name=Bad --output_file=out --sort_key=cgm_small.csv
assert_in_stderr 'Directory not found'

run test_bad_input python data_import.py --folder_name=smallData --output_file=out --sort_key=Bad.csv
assert_in_stderr 'Please double check your sort key'