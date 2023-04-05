# TODO: Consider adding various functions for granularity through this program. Possibly along the lines of 6, 9,
#  or 15 sheets. (15 is s m l v vc c cg g
from Resources import file_id_reader
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)


class ImportProcessing:
    # TODO: This cleaning feels very rigid. Could I do something like get all the dates and then remove where either
    #  fund name, ISIN, avg cap, vg score etc is empty?
    def __init__(self, filetype: str = ".csv"):
        self.DF = None
        self.Headers = None
        all_files = file_id_reader.list_all_files(True, file_type=filetype)
        filename_user = file_id_reader.user_selected_file(all_files)
        self.Filename = file_id_reader.file_name_generator(filename_user)[0]
