import os
import sys


def list_all_files(print__):
    a = 1
    files_ = []
    for x in os.listdir():
        if x.endswith(".py") and x not in __file__:
            if print__:
                print(a, x)
            files_.append(x)
            a += 1
    return files_


def user_selected_file(file_list):
    while True:
        desired_index = input("Input the number next to the function you would like to run: ")
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
    print("\n\n")
    return file_list[int(desired_index) - 1]


function = user_selected_file(list_all_files(True))
exec(open(function).read())
