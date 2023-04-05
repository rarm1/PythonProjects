import os
from constants import Constants


class OutputDocument:

    def __init__(self):
        self.AOL_Filename = None
        self.AOL_pdf_filename = None
        self.AOL_Written_File_Path = None

        self.DA_Filename = None
        self.DA_pdf_filename = None
        self.DA_Written_File_Path = None

        self.Location = None
        self.Constants = Constants()

    def create_files(self):
        try:
            # self.Constants.AOL_Template_Doc.save(self.Location + self.AOL_Filename)
            # self.AOL_Written_File_Path = self.Location + self.AOL_Filename
            # output_path = os.path.join(self.Location, self.AOL_Filename)
            # self.Constants.AOL_Template_Doc.save(output_path)
            # self.AOL_Written_File_Path = output_path
            output_path = self.Location / self.AOL_Filename
            self.Constants.AOL_Template_Doc.save(str(output_path))
            self.AOL_Written_File_Path = str(output_path)
        except PermissionError as pe:
            print(pe)
        try:
            # self.Constants.DA_Template_Doc.save(self.Location + self.DA_Filename)
            # self.DA_Written_File_Path = self.Location + self.DA_Filename
            # output_path = os.path.join(self.Location, self.DA_Filename)
            # self.Constants.DA_Template_Doc.save(output_path)
            # self.DA_Written_File_Path = output_path
            output_path = self.Location / self.DA_Filename
            self.Constants.DA_Template_Doc.save(str(output_path))
            self.DA_Written_File_Path = str(output_path)
        except PermissionError as pe:
            print(pe)
