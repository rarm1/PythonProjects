# TODO: Take unit trades and adjust the value depending on the cost of units.
import logging
import os
import pathlib
import shutil
import sys
from stat import S_IREAD

import pandas as pd

from Resources import constants
from Resources import file_id_reader
from Resources import trade_writer

logging.basicConfig(filename='Resources/Trade_reader.log', format='%(asctime)s - %(message)s',
					level=logging.INFO)
HEADERS_GENERATOR = ['FMDealingCode', 'TradeIdentifier', 'TradeFileDate', 'SchemeIdentifier', 'SecurityName',
                     'SecurityIdentifier', 'NewSecurity', 'Direction', 'DealType', 'Value',
                     'SettlementCurrency', 'PreviouslyReported', 'Notes',
                     'Scheme from Rebalancer (DELETE AFTER VERIFICATION)',
                     'Scheme from PID lookup sheet (DELETE AFTER VERIFICATION)']





class TradeReader:
	def __init__(self):
		self.trade_df = None
		self.list_of_trades = []
		self.path = self.set_path()
		trade_writer.fundmanager_selection()


	@staticmethod
	def set_path():
		directory = f'Rebalancing {trade_writer.FOLDER_DATE}_TRAIL_DONOTPLACE'
		parent_directory = "X:/Fund Management/Dealing and Rebalancing"
		path = os.path.join(parent_directory, directory)
		if not os.path.exists(path):
			os.mkdir(path)
		return path
	
	@staticmethod
	def find_trades():
		all_found_trades = [x for x in constants.all_funds() if x.offset(0, 2).value not in [None, ""]]
		return all_found_trades
	
	def process(self):
		all_files = file_id_reader.list_all_files()
		if not all_files:
			sys.exit("Please ensure that there are files ending in .xlsx within the project folder.")
		
		filename_user = file_id_reader.user_selected_file(all_files)
		filenames = file_id_reader.file_name_generator(filename_user)
		counters = self.process_files(filenames)
		
		self.trades(counters)

		print(f"Written a total of {counters['total_trades']} trade{'s' if counters['total_trades'] > 1 else ''}")
		sys.exit(
				"I hope you enjoyed this program! Please direct any queries or issues to richard.armstrong@margetts.com")
	
	def process_files(self, filenames):
		tradeless = []
		counters = {"total_trades": 0, "funds_without_trades": 0}
		
		for i, filename in enumerate(filenames):
			if len(filenames) > 1:
				print(f'\r{i + 1} rebalancers read.', end='')
			
			reader_sheet = file_id_reader.sheet_reader(filename)
			self.set_reader_sheets(filename, reader_sheet)
			all_trades = self.find_trades()
			counters["total_trades"] += len(all_trades)

			counters = self.process_trades(counters, all_trades)

			if (i + 1) == len(filenames):
				self.print_summary(filenames, tradeless, counters)

			self.copy_file_to_path(filename)

		return counters
	
	@staticmethod
	def set_reader_sheets(filename, reader_sheet):
		trade_writer.READER_DOC = filename
		trade_writer.READER_SHEET = reader_sheet
		constants.READER_SHEET = reader_sheet

	def process_trades(self, counters, all_trades):
		if counters["total_trades"]:
			trades = trade_writer.automated_trading_array_generator(all_trades)
			if not len(trades) == 0:
				self.list_of_trades.extend(trades)
		return counters

	@staticmethod
	def print_summary(filenames, tradeless, counters):
		print(f"\nFinished reading {len(filenames)} file{'s' if len(filenames) > 1 else ''}."
		      f"\nThere were {len(tradeless)} portfolios without trades.")
		print(f"Written a total of {counters['total_trades']} trade{'s' if counters['total_trades'] > 1 else ''}")
	
	def copy_file_to_path(self, filename, read_only: bool=False):
		file_path = (pathlib.Path(filename).resolve())
		try:
			if read_only:
				os.chmod(file_path, S_IREAD)
			shutil.copy2(file_path, self.path)
		except (shutil.SameFileError, PermissionError, Exception) as e:
			logging.error("Error occured" + str(e))
			print(f"{e}: Error occured while copying file.")
	
	def trades(self, counters):
		try:
			if counters['total_trades'] != 0:
				# todo: here I want to check the broker trades. And amend the values with df manipulation.
				self.trade_df = pd.DataFrame(self.list_of_trades, columns=HEADERS_GENERATOR)
				self.id_broker_trades()

				trade_filename = trade_writer.main_writer(self.trade_df, HEADERS_GENERATOR)
				self.copy_file_to_path(trade_filename, read_only=True)
		except AttributeError as e:
			logging.error("Error occured" + str(e))

	def id_broker_trades(self):
		# In here is where I can get all the tickers from the isins which I can save and then init an instance of the
		# price finder class. Then I can get the prices and modify the gross consideration of the trade to be the
		# quantity of units of the trade.
		pass

if __name__ == "__main__":
	trade_processor = TradeReader()
	trade_processor.process()
