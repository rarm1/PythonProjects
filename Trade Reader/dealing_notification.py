# TODO: Add logging into this because it has thrown errors in the console several times, which is no good for anyone.
import sys

import file_id_reader
import logging
import numpy as np

logging.basicConfig(filename='Resources/Trade_reader.log', level=logging.INFO)
file_checker = file_id_reader.list_all_files(False, '.csv')
if len(file_checker) == 1:
    file = np.recfromcsv(file_checker[0], encoding=None)
else:
    print("Please select the 'unchecked' file.")
    ALL_FILES = file_id_reader.list_all_files(True, '.csv')
    FILENAME_USER = file_id_reader.user_selected_file(ALL_FILES, enable_all=False)
    FILENAMES = file_id_reader.file_name_generator(FILENAME_USER)
    file = np.recfromcsv(FILENAMES[0], encoding=None)
    print(file)

important_info = []
try:
    for line in file:
        fundname = line[4]
        direction = line[7]
        portfolio = line[-2]
        important_info.append([portfolio, fundname, direction])
except Exception as e:
    logging.error("Error occured" + str(e))
    sys.exit("There has been an error, apologies, the program will now close.")

dictionary_output = {}
try:
    for deal in important_info:
        if deal[0] in dictionary_output.keys():
            dictionary_output[deal[0]].append([deal[1], deal[2]])
        else:
            dictionary_output[deal[0]] = [[deal[1], deal[2]]]
except Exception as e:
    logging.error("Error occured" + str(e))

with open('Tell Dealing.txt', 'w') as f:
    for portfolio in dictionary_output.keys():
        len_port = len(dictionary_output[portfolio])
        f.write(f"{portfolio} {len_port} trade{'s' if len_port > 1 else ''}\n")
        for trade in dictionary_output[portfolio]:
            f.write(f"{trade[0]}: {trade[1]}\n")
        else:
            f.write('\n')
