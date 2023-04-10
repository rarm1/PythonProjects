import pandas as pd

import file_id_reader


class DealingSheet:
	
	def __init__(self):
		print("Welcome to PAM Broker Uploader")
		self.trades = {}
		self.filetype = None
		self.df = self._read_document()
		if self.filetype == "xlsx":
			self.document = self._tidy_trades(self.df)
		elif self.filetype == "csv":
			self.document = self.df
	
	def _read_document(self):
		"""
		Reads the document from the file and returns a pandas DataFrame.
		"""
		all_files = file_id_reader.list_files_by_type(False, to_ignore=['ISIN_to_Ticker.csv', 'pid_lookup.csv'])
		
		if len(all_files) == 1:
			filename = all_files[0]
			print(f"This has identified and will read: {filename}")
		else:
			for idx, filename in enumerate(all_files):
				print(idx + 1, filename)
			filename_user = file_id_reader.select_file_by_user(all_files, enable_all=False)
			filename = file_id_reader.generate_file_names(filename_user)[0]
		
		try:
			self.filetype = "xlsx"
			return pd.read_excel(filename, sheet_name=0)
		except UnicodeDecodeError:
			self.filetype = "csv"
			try:
				return pd.read_csv(filename)
			except UnicodeDecodeError as e:
				print(f"This has errored with {e}")
				raise
	
	@staticmethod
	def _tidy_trades(df):
		df = df[(df['AssetType'] == 'Closed-Ended Funds') | (df['AssetType'] == 'REITs')]
		return df
