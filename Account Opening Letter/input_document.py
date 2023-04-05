import openpyxl as xl

from constants import Constants


class InputDocument:
    def __init__(self):
        constants = Constants()
        fund_list_doc = xl.load_workbook(constants.fund_list_filename, read_only=True, data_only=True)
        self.Reader_Sheet = fund_list_doc.worksheets[0]
