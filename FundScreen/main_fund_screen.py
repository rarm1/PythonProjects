# TODO: Could I do something cool here like, all the funds that've been rejected just end up in the final page on
#  excel called 'rejects' and it does whatever calculations it can do?
import pandas as pd

from import_processing import ImportProcessing


def main():
    import_document = ImportProcessing()
    import_document.print_(import_document.performance_dataframes)
    import_document.print_(import_document.index_dataframes)
    import_document.print_(import_document.na_dataframe)


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.max_rows', None)
    main()
