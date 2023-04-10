import pandas as pd

from assets import file_id_reader

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
		self.def_df()
		self._clean()
	
	def _cleantop(self):
		row_index = self.DF.loc[self.DF.iloc[:, 0] == 'Group/Investment'].index[0]
		self.DF = self.DF.iloc[row_index:, :].reset_index(drop=True)
		self.DF.columns = self.DF.iloc[0].tolist()
	
	def dropna(self):
		# TODO: Drop if there is no ISIN or Fund name.
		self.DF.dropna(subset=['Group/Investment', 'ISIN'], inplace=True)
		# for header in self.Headers:
		#     self.DF.dropna(subset=header, inplace=True)
		self.DF = self.DF.iloc[1:, :].reset_index(drop=True)
	
	def _clean(self):
		self._cleantop()
		self.dropna()
		print(self.DF)
	
	# self.Headers = [header for header in self.DF.iloc[0] if
	#                 "Return" not in header]
	# self.clean_columns()
	
	def clean_columns(self):
		returns = False
		column_names = []
		return_count = 1
		for idx, col in enumerate(self.DF.columns):
			if "Return" in col and returns:
				column_names.append(f"Return {return_count}")
				return_count += 1
			elif "Return" in col and not returns:
				column_names.append("Return")
				returns = True
			else:
				column_names.append(col)
		self.DF.columns = column_names
	
	def def_df(self):
		if "csv" in self.Filename:
			self.DF = pd.read_csv(self.Filename, index_col=None)
		elif "xlsx" in self.Filename:
			self.DF = pd.read_excel(self.Filename, sheet_name=0, index_col=None)
