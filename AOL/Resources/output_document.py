from AOL.Resources.constants import Constants
import os


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
			output_path = self.Location / self.AOL_Filename
			output_directory = output_path.parent
			os.makedirs(output_directory, exist_ok=True)
			self.Constants.AOL_Template_Doc.save(str(output_path))
			self.AOL_Written_File_Path = str(output_path)
		except PermissionError as pe:
			print(pe)
		try:
			output_path = self.Location / self.DA_Filename
			self.Constants.DA_Template_Doc.save(str(output_path))
			self.DA_Written_File_Path = str(output_path)
		except PermissionError as pe:
			print(pe)

	@staticmethod
	def sanitize_filename(filename):
		return ''.join(c if c.isalnum() else '_' for c in filename)
