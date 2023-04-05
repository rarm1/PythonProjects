import os
import sys


# This lists all xlsx files which can be read by the rebalancer.
def list_all_files(to_print=True, file_type='.xlsx', to_ignore=()):
    """
    List all files according to certain criteria.
    :param to_ignore: Pass an array of files that are not to be listed
    :params:
    :param to_print: Boolean
    | Is this function to print out all files found. Can be used when the same list would be printed twice.
    | This helps avoid clutter in the console.
    :param file_type: String
    | The filetype that is to be listed. This can be passed an empty string to return all files in directory.
    :return: Array
    """
    a = 1
    files_ = []
    for x in os.listdir():
        if (x.endswith(file_type) or x.endswith(file_type)) and not x.startswith('~') and x not in to_ignore:
            if to_print:
                print(a, x)
            files_.append(x)
            a += 1
    return files_


def user_selected_file(file_list, doc_type='file', enable_all=True, default_return=False):
    """
    Allows the user to return an index for the desired file. doctype allows for printing various file_types.
    Returns the filename to.
    :param default_return:
    :param enable_all:
    :param file_list: Array
    :param doc_type:
    :return:
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


def file_name_generator(filename):
    """
    Generates all filenames required
    :param filename: String
    :return: Funct / String
    """
    if filename == 'a':
        return list_all_files(False)
    else:
        return [filename]
