import os
import sys


def list_files_by_type(to_print=True, file_type='.xlsx', to_ignore=()):
	"""
	List all files according to certain criteria.
	:param to_print: Bool, If True, prints all files found.
	:param file_type: str, The filetype that is to be listed.
	:param to_ignore: tuple, Pass an array of files that are not to be listed.
	:return: list, A list of file names.
	"""
	index = 1
	files_ = []
	for filename in os.listdir():
		if filename.endswith(file_type) and not filename.startswith('~') and filename not in to_ignore:
			if to_print:
				print(index, filename)
			files_.append(filename)
			index += 1
	return files_


def select_file_by_user(file_list, doc_type='file', enable_all=True, default_return=False):
	"""
	Allows the user to return an index for the desired file. doctype allows for printing various file_types.
	Returns the filename to.
	:param default_return:
	:param enable_all:
	:param file_list: Array
	:param doc_type: String.
	:return: String.
	"""
	while True:
		if default_return:
			return file_list[0]
		desired_index = input(
				f"Input the index of the {doc_type} you'd like to read {'enter a for all files' if enable_all else ''}:")
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


def generate_file_names(filename):
	"""
	Generates all filenames required
	:param filename: str, The file name or 'a' for all files
	:return: list, A list of filenames
	"""
	if filename == 'a':
		return list_files_by_type(False)
	else:
		return [filename]
