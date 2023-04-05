from Resources import file_id_reader

import numpy as np

ALL_FILES = file_id_reader.list_all_files(True, '.csv')
FILENAME_USER = file_id_reader.user_selected_file(ALL_FILES, enable_all=False)
FILENAMES = file_id_reader.file_name_generator(FILENAME_USER)
file = np.recfromcsv(FILENAMES[0], encoding=None)

important_info = []
for line in file:
    fundname = line[4]
    direction = line[7]
    portfolio = line[-2]
    notes = line[-3]
    important_info.append([portfolio, fundname, direction, notes])

dictionary_output = {}

for deal in important_info:
    if deal[0] in dictionary_output.keys():
        dictionary_output[deal[0]].append([deal[1], deal[2], deal[3]])
    else:
        dictionary_output[deal[0]] = [[deal[1], deal[2], deal[3]]]

with open('tell_dealing.txt', 'w') as f:
    for portfolio in dictionary_output.keys():
        print(dictionary_output[portfolio])
        if dictionary_output[portfolio][0][2].lower() == "rebalancing":
            f.write("Non-critical Rebalancing")
        else:
            f.write(dictionary_output[portfolio][0][2])
        len_port = len(dictionary_output[portfolio])
        print(len_port > 1)
        f.write(f"{portfolio} {len_port} trade{'s' if len_port > 1 else ''}\n")
        print(portfolio, len(dictionary_output[portfolio]),"trades")
        for trade in dictionary_output[portfolio]:
            print(f"{trade[0]}: {trade[1]}")
            f.write(f"{trade[0]}: {trade[1]}\n")
        else:
            f.write('\n')
