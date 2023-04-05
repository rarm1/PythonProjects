# Take in the returns using the same methods as the Regression writer.
import math

import pandas as pd

from Resources import file_id_reader as fid

global DOCUMENT


# Function allows the document to be changed easier, with lower risk of mistakes
def document_to_read(file_name):
    file = pd.read_excel(file_name, thousands=",")
    return file


# Increased efficiency by only reading once per line from the entire document. This reduces the amount of memory and
# processing power that is being used.
def create_time_series():
    to_return = []
    for companyIndex in list(x.row for x in fid.find_all_funds())[:-1]:
        time_series = 0
        company_all_returns = DOCUMENT.iloc[companyIndex]
        for weeklyReturn in list(x.column for x in fid.returns_column())[:-1]:
            if math.isnan(company_all_returns[weeklyReturn]):
                interest = 0
            else:
                interest = (company_all_returns[weeklyReturn]) / 100
            time_series = ((1 + time_series) * (1 + interest)) - 1
        to_return.append(([company_all_returns[0], time_series * 100]))
    else:
        return to_return


# This writes the returns to an Excel document and handles any errors that may be thrown.
def excel_writer(arr, modified_filename):
    try:
        with pd.ExcelWriter(modified_filename, engine="openpyxl") as writer:
            df = pd.DataFrame(arr, columns=['Fund', 'Returns'])
            df.to_excel(writer, sheet_name="Time Series", index=False)
    # Permission Errors tend to occur when the file is already open. It is rare that permission errors will occur
    # Because the program does not have permissions to write to a certain folder.
    except PermissionError:
        print(f"There has been a problem. Chances are that the file: {modified_filename} is already open. \n"
              f"Please check whether this is the case and rerun the program if so. \n"
              f"Otherwise, please contact richard.armstrong@margetts.com")
    # This catches any other errors.
    except Exception as e:
        print(e, ": error thrown, please contact richard.armstrong@margetts.com for assistance.")


def main():
    global DOCUMENT
    filename = 'Global EM Screening.xlsx'
    DOCUMENT = document_to_read(filename)
    fid.READER_SHEET = fid.sheet_reader(filename, True, 'Active')
    ts_array = create_time_series()
    excel_writer(ts_array, filename[:-5]+" finished.xlsx")


if __name__ == '__main__':
    main()
