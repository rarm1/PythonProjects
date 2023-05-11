import os
import sys

import openpyxl as xl

global READER_SHEET, MODIFIED_FILENAME

def list_all_files(to_print=True, file_type='.xlsx', exclusions: list = ()):
	a = 1
	files_ = []
	for x in os.listdir():
		if (x.endswith(file_type) or x.endswith(file_type)) and not x.startswith('~'):
			if x not in exclusions:
				if to_print:
					print(a, x)
				files_.append(x)
				a += 1
	return files_


def user_selected_file(file_list, doc_type='file', enable_all=True, default_return=False):
	while True:
		if default_return:
			return file_list[0]
		desired_index = input(
				f"Input the index of the {doc_type} you'd like to read "
				f"{'enter a for all files' if enable_all else ''}:")
		try:
			desired_index = int(desired_index)
			if len(file_list) + 1 > desired_index > 0:
				break
		except ValueError:
			if desired_index == 'a':
				return 'a'
			elif desired_index.lower() == 'exit':
				sys.exit("Quitting")
			print("NaN")
	return file_list[int(desired_index) - 1]


def file_name_generator(filename):
	if filename == 'a':
		return list_all_files(False)
	else:
		return [filename]


def sheet_reader(filename, data_only=True, sheet_name='Rebalancer'):
	document = xl.load_workbook(filename, data_only=data_only)
	if sheet_name == "Active":
		return document.active
	else:
		return document[sheet_name]
