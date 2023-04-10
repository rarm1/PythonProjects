# TODO: OO this. particularly the trade functions. There is no reason for each trade not to be an object that has the
#  properties of the columns. This can then be manipulated into being either an email, or into the regular sheet. The
#  steps that need to happen for a broker trade are to take the consideration. Get the price per unit for the3
#  desired security, estimate units from the consideration, create email based on this estimated consideration. We
#  would also then add the same unit quant from the email as on the uploader, the trade type for this needs to be units.
import sys
from datetime import date
from os.path import exists

import openpyxl as xl
import pandas as pd

from assets import constants

# Variable initialisation
global MODIFIED_FILENAME, WRITER_SHEET, READER_SHEET, READER_DOC, NON_BROKER_FILENAME, BROKER_FILENAME, FUND_MANAGER
TRADES = 0
# These are used so that if the location changes, it can be changed here, without refactoring the entire project.
SCHEME_LIST_LOCATION = 'assets/scheme_list_desig.xlsm'
LIBERUM_ACC_NO_FILE = 'Liberum_Account_Numbers.csv'
LIBERUM_ACCOUNT_NUMBERS_DF = pd.read_csv(LIBERUM_ACC_NO_FILE)

TRADE_ID_FILE = 'trade_identifier.xlsx'
TRADE_ID_SHEET = 'trade_identifier'
TG_ACCOUNT_PATH = 'Thomas Grant account numbers.xlsx'
TG_ACCOUNT_DOC = xl.load_workbook(TG_ACCOUNT_PATH, data_only=True)
TG_ACCOUNT_NUMBERS = TG_ACCOUNT_DOC['Sheet1']
# The scheme loopup is written here. This is for ease of updating.
# Again, if multiple people are using this program, then
# ensuring every instance of this document is updated will be more error-prone.
SCHEME_LOOKUP_DOC = xl.load_workbook(SCHEME_LIST_LOCATION)
SCHEME_SHEET = SCHEME_LOOKUP_DOC['Source']
ISIN_TO_TICKER_PATH = 'ISIN_to_Ticker.xlsx'
ISIN_TO_TICKER_DOC = xl.load_workbook(ISIN_TO_TICKER_PATH, data_only=True)
ISIN_TO_TICKER_SHEET = ISIN_TO_TICKER_DOC['Sheet1']
FOLDER_DATE = date.today().strftime("%Y%m%d")
FUND_MANAGERS = {
	"Dmitry Konev": "DMITRY",
	"Richard Cole": "FMONEY",
	"Wayne Buttery": "OPES",
	"IBOSS Asset Management": "IBOSS",
	"Sentinel Asset Management": "SENTINEL"
}
HEADERS_GENERATOR = ['FMDealingCode', 'TradeIdentifier', 'TradeFileDate', 'SchemeIdentifier', 'SecurityName',
                     'SecurityIdentifier', 'NewSecurity', 'Direction', 'DealType', 'Value',
                     'SettlementCurrency', 'PreviouslyReported', 'Notes',
                     'Scheme from Rebalancer (DELETE AFTER VERIFICATION)',
                     'Scheme from PID lookup sheet (DELETE AFTER VERIFICATION)']
BROKER_HEADERS_GENERATOR = ['Action', 'Security', 'ISIN', 'Ticker', 'Shares',
                            'Approx. Notional Value', 'Currency', 'Allocation',
                            'Liberum Account Number', 'Fund Manager', 'Trade ID', 'New Purchase',
                            'Scheme from Rebalancer (DELETE AFTER VERIFICATION)', "Notes"]


def single_trade_writer(fund, trade_amount):
	"""
	This accepts a trade and appends it to the rebalancer sheet.
	:param fund: Cell
	:param trade_amount: Int
	:return: Void
	"""
	global TRADES
	row = fund.row
	column = fund.column + 2
	reader_cell = READER_SHEET.cell(row=row, column=column)
	if (fund.offset(0, -6).value + trade_amount) / constants.total_portfolio_value().value < 0.0005:
		reader_cell.offset(0, 3).value = "Sell All"
		trade_amount = -fund.offset(0, -6).value
	else:
		trade_amount = round(trade_amount, -3)
	reader_cell.value = trade_amount
	constants.cash_figure().value -= trade_amount
	TRADES += 1


TODAY = date.today()
REQ_DATE = TODAY.strftime("%d/%m/%Y")


def units_to_trade(trade):
	"""

	:param trade:
	:return:
	"""
	try:
		price_per_unit = abs(trade.offset(0, -6).value) / abs(trade.offset(0, -5).value)
	except ZeroDivisionError:
		return 0
	try:
		return abs(trade.offset(0, 2).value) / abs(price_per_unit)
	except ZeroDivisionError:
		return "Zero Division Error. Either continue or report this error accordingly, please."


def get_trade_data(trade, idx):
	"""

	:param trade:
	:param idx:
	:return:
	"""
	sec_name = trade.offset(0, -7).value
	isin = trade.offset(0, -9).value
	deal_type = _trade_type(trade)
	trade_value = value_of_trade(deal_type, trade)
	trade_id = get_trade_identifier() + idx
	notes = notes_value(trade)
	
	return sec_name, isin, deal_type, trade_value, trade_id, notes


def is_broker_trade(notes):
	"""

	:param notes:
	:return:
	"""
	return "broker" in notes.lower() or "etf" in notes.lower()


def get_liberum_account_number(designation):
	"""

	:param designation:
	:return:
	"""
	liberum_account_number = str()
	for idx, row in LIBERUM_ACCOUNT_NUMBERS_DF.iterrows():
		if designation in row['Designation']:
			liberum_account_number = row['Account_Number']
	return liberum_account_number


def get_broker_trade_details(trade, sec_name, isin, trade_id, notes):
	"""

	:param trade:
	:param sec_name:
	:param isin:
	:param trade_id:
	:param notes:
	:return:
	"""
	total_units_to_trade = units_to_trade(trade)
	total_units = trade.offset(0, -5).value
	try:
		if abs(total_units - total_units_to_trade) < 0.01 * total_units:
			total_units_to_trade = total_units
	except ZeroDivisionError:
		total_units_to_trade = "Zero Division Error. Either continue or report this error accordingly, please."
	except TypeError:
		pass
	action = buy_or_sell(trade)
	approx_notional_value = abs(trade.offset(0, 2).value)
	designation = str(READER_SHEET.cell(4, 2).value)
	fund_name = READER_SHEET.cell(2, 2).value
	liberum_account_number = get_liberum_account_number(designation)
	return [action, sec_name, isin, ticker_lookup(isin), round(total_units_to_trade),
	        approx_notional_value, currency_finder(trade),
	        fund_name + " " + designation, liberum_account_number, FUND_MANAGER,
	        trade_id, new_buy_finder(trade), fund_name, notes]


def get_regular_trade_details(sec_name, isin, trade_id, trade, deal_type, trade_value, notes):
	"""

	:param sec_name:
	:param isin:
	:param trade_id:
	:param trade:
	:param deal_type:
	:param trade_value:
	:param notes:
	:return:
	"""
	return [FUND_MANAGER, trade_id, REQ_DATE, scheme_lookup().value, sec_name,
	        isin, new_buy_finder(trade), buy_or_sell(trade), deal_type, trade_value,
	        currency_finder(trade), "N", notes, READER_SHEET.cell(2, 2).value,
	        scheme_lookup().offset(0, 1).value]


def trade_array_generator(idx, trade):
	"""

	:param idx:
	:param trade:
	:return:
	"""
	sec_name, isin, deal_type, trade_value, trade_id, notes = get_trade_data(trade, idx)
	
	# if is_broker_trade(notes):
	#     return True, get_broker_trade_details(trade, sec_name, isin, trade_id, notes),
	#     get_regular_trade_details(sec_name, isin, trade_id, trade, deal_type, trade_value, notes)
	# else:
	return False, get_regular_trade_details(sec_name, isin, trade_id, trade, deal_type, trade_value, notes)


# This requests the name of the fund manager from the user and uses this to write to the csv.
def fundmanager_selection():
	"""

	"""
	global FUND_MANAGER
	# The use of enumerate here allows for easier visualisation of the array for the user.
	# without using this function the list would start at '0' which is much less natural for most potential users. #
	for idx, x in enumerate(FUND_MANAGERS, start=1):
		print(f"{idx}: {x}")
	while True:
		desired_index = input("Please input the number of the fund manager to select: ")
		try:
			desired_index = int(desired_index)
			if len(FUND_MANAGERS) + 1 > desired_index > 0:
				break
		except ValueError:
			print("NaN")
	print("\n")
	FUND_MANAGER = list(FUND_MANAGERS.values())[desired_index - 1]


# This finds the scheme loopup reference document. This document, again, is located in a central place, such that it can
# be updated. Provided the layout, and name of the file is the same, then it can be changed without modifying any code.
def scheme_lookup():
	"""

	:return:
	"""
	rebalancer_scheme = READER_SHEET.cell(4, 2)
	for x in range(1, SCHEME_SHEET.max_row + 1):
		lookup_designation = (SCHEME_SHEET.cell(x, 3))
		if str(lookup_designation.value) in str(rebalancer_scheme.value) or str(rebalancer_scheme.value) in str(
				lookup_designation.value):
			return SCHEME_SHEET.cell(row=x, column=1)
	return f"Scheme PID {rebalancer_scheme.value} not listed in {SCHEME_LIST_LOCATION}"


def ticker_lookup(isin):
	"""

	:param isin:
	:return:
	"""
	for i in range(1, ISIN_TO_TICKER_SHEET.max_row + 1):
		isin_in_lookup = ISIN_TO_TICKER_SHEET.cell(i, 1)
		if isin_in_lookup.value is not None:
			if isin.lower() in isin_in_lookup.value.lower():
				return ISIN_TO_TICKER_SHEET.cell(i, 2).value
	else:
		return "ISIN TO BE ADDED"


def new_buy_finder(trade):
	"""
	Determines whether the fund is already held or whether it is a new fund in the portfolio
	:param trade: Cell containing trade
	:return: Y or N based on new holding or not.
	"""
	if trade.offset(0, -2).value == 0:
		return "Y"
	else:
		return "N"


# Define buy or sell. Is the trade greater or larger than 0.
def buy_or_sell(trade):
	"""
	Takes a trade and returns whether it is a buy or a sell.
	:param trade: Cell containing trade
	:return: Direction of trade.
	"""
	if trade.offset(0, 2).value > 0:
		return "BUY"
	else:
		return "SELL"


# This is the trade identifier that is generated in the constants file.
# The reason that this file is centralised is that it reduces duplicate trade errors.
def get_trade_identifier():
	"""

	:return:
	"""
	trade_counter_doc = xl.load_workbook(TRADE_ID_FILE)
	trade_sheet = trade_counter_doc[TRADE_ID_SHEET]
	return trade_sheet.cell(1, 1).value


# This returns the value of the trade. The reason this function exists instead of reading a set value is that if
# all the fund is being sold, then this function must return the amount of units held in the fund.
def value_of_trade(deal_type, trade):
	"""
	Ensure that the correct trade value is returned. This changes based on whether a trade is currency or units.
	:param deal_type: Units or cash
	:param trade: Cell containing trade
	:return: Returns the quantity to be traded.
	"""
	if "sellall" in deal_type.lower():
		return 0  # Sell all is irrelevant for the trade value.
	elif "cash" in deal_type.lower():
		return abs(trade.offset(0, 2).value)  # Return the trade quantity
	elif "unit" in deal_type.lower():
		# This is where we need to have the live price of the ETF's,
		# so we can calculate the value of the trade in units.
		pass


def _trade_type(trade):
	"""
	Generate whether this is a sell all trade or not.
	:param trade: Cell containing trade.
	:return: Returns units or cash.
	"""
	holding_value = trade.offset(0, -6).value
	trade_value = trade.offset(0, 2).value
	if trade_value < 0:
		if notes_value(trade) == "Sell All":
			if holding_value == abs(trade_value):
				return 'SellAll'
			else:
				print(READER_DOC)
				print(f"There has been an error with trade at coordinates: {trade}")
				input("Press any key to continue, the program will exit after this and allow for secondary checks.")
				sys.exit("THERE HAS BEEN A PROBLEM WITH SELL ALL'S NOT BEING NOTED IN NOTES AND/OR VALUATION"
				         "PLEASE RESOLVE THIS ISSUE BEFORE CONTINUING.")
		elif "broker" in notes_value(trade).lower() or "etf" in notes_value(trade).lower():
			return "Unit"
	return "Cash"


def sell_all_reader(trade):
	"""
	Determines whether it is a sell all or a normal rebalancing trade.
	:param trade: Cell containing trade
	:return: Returns either sell all or rebalancing
	"""
	if abs(round(trade.offset(0, 3).value, 2)) == 0.0:
		if notes_value(trade) == "Sell All":
			return 'Sell All'
		else:
			print(READER_DOC)
			print(f"There has been an error with trade at coordinates: {trade}"
			      f"This generally means that the trade value does not match the holding value.")
			input("Press any key to continue, the program will exit after this and allow for secondary checks.")
			sys.exit("THERE HAS BEEN A PROBLEM WITH SELL ALL'S NOT BEING NOTED IN NOTES AND/OR VALUATION"
			         "PLEASE RESOLVE THIS ISSUE BEFORE CONTINUING.")
	else:
		return "Rebalancing"


def currency_finder(trade):
	"""
	The finds the currency that a trade is given in. If there is no currency found, assume GBP.
	:param trade: Cell containing trade.
	:return: Returns currency.
	"""
	if trade.offset(0, -4).value is not None:
		return trade.offset(0, -4).value
	else:
		return "GBP"


def notes_value(trade):
	"""
	Under development:
	Takes trade value, returns notes from context based locations.
	:param trade: Cell containing trade
	:return: Returns contents for notes column.
	"""
	notes = trade.offset(0, 5).value
	if notes is not None:
		# This is another quick sanity check. If The column contains 'sell' indicating that this is a sell all
		# But the trade is a buy, then it will alert the user to this, and give the user the
		if "broker" in notes.lower() or "etf" in notes.lower():
			return "Broker Trade"
		if notes.lower() == "cis":
			return "Rebalancing"
		if "sell all" in notes.lower():
			return "Sell All"
		if 'sell' in notes.lower() and buy_or_sell(trade) == "BUY":
			print(
					f"Are you sure the notes are correct? It looks like this trade is a buy. {trade.offset(0, -7).value}\n"
					f"This is in {READER_DOC}.")
			if input("Do you want to continue? Y/N: ").lower() == "y":
				return notes
			else:
				sys.exit("Closing the program, come back soon!")
		else:
			return notes
	
	if sell_all_reader(trade).lower() == "sell all":
		return "Sell All"
	if FUND_MANAGER == "IBOSS":
		return "IBOSS instructed trade"
	elif FUND_MANAGER == 'CLARION':
		return 'Clarion instructed trade'
	else:
		return 'Rebalancing'


# This generates the list of lists to be written to the csv document.
def automated_trading_array_generator(trade_array):
	""" Takes an array of all trade locations. Returns an array that contains all trading information. """
	non_broker_trades, broker_trades = [], []
	trade_id = 1
	constants.READER_SHEET = READER_SHEET
	for idx, a in enumerate(trade_array, start=1):
		trade_id = get_trade_identifier() + idx
		broker_trade, trial_return = trade_array_generator(idx, a)
		if broker_trade:
			broker_trades.append(trial_return[0])
			non_broker_trades.append(trial_return[1])
		else:
			non_broker_trades.append(trial_return)
	
	else:
		if len(trade_array) != 0:
			write_trade_value(trade_id)
		return non_broker_trades, broker_trades


# This updates the trade number after ever rebalancer that has been read. This adds a stable point in which to rewrite.
# And doesn't give the user a chance to write trades, and then escape the program without updating the trade quantity.
def write_trade_value(trade):
	"""

	:param trade:
	"""
	trade_counter_doc = xl.load_workbook(TRADE_ID_FILE)
	trade_sheet = trade_counter_doc[TRADE_ID_SHEET]
	trade_sheet.cell(1, 1).value = trade
	trade_counter_doc.save(TRADE_ID_FILE)


def main_writer(trades):
	"""
	Takes in an array of trades, writes these trades to a .csv file.
	:param trades: Array of all trades.
	:return: No return statement.
	"""
	global NON_BROKER_FILENAME, HEADERS_GENERATOR
	# Do not create empty files.
	if len(trades) == 0:
		return
	elif not len(trades) == 0:
		# This creates a dateaframe from the list of lists generated.
		df = pd.DataFrame(trades)
		req_date: str = date.today().strftime("%d-%m-%Y")
		# Use the variables defined above to generate a csv document using functions
		# that're built into the pandas repository
		if FUND_MANAGER == "CLARION":
			NON_BROKER_FILENAME = 'Unchecked_' + "Clarion_" + req_date + '.csv'
		else:
			NON_BROKER_FILENAME = 'Unchecked_' + FUND_MANAGER + '_' + req_date + '.csv'
		# If this file exists, then there should not be any additional headers, and it should append, rather than
		# overwrite.
		if exists(NON_BROKER_FILENAME):
			headers = False
			mode = 'a'
		# If the file doesn't exist then use the header array and use the 'writer' file.
		else:
			headers = HEADERS_GENERATOR
			mode = 'w'
		try:
			df.to_csv(NON_BROKER_FILENAME, index=False, mode=mode, header=headers)
		except PermissionError:
			df.to_csv(NON_BROKER_FILENAME, index=False, mode=mode, header=headers)
		return NON_BROKER_FILENAME


def broker_trade_writer(trades):
	"""
	Takes in an array of trades, writes these trades to a .csv file.
	:param trades: Array of all trades.
	:return: No return statement.
	"""
	global BROKER_FILENAME
	# Do not create empty files.
	if len(trades) == 0:
		return
	elif not len(trades) == 0:
		# This creates a dateaframe from the list of lists generated.
		df = pd.DataFrame(trades)
		req_date: str = date.today().strftime("%d-%m-%Y")
		# Use the variables defined above to generate a csv document using
		# functions that're built into the pandas repository
		if FUND_MANAGER == "CLARION":
			BROKER_FILENAME = "Unchecked_Dmitry_" + req_date + '_broker_trades.csv'
		else:
			BROKER_FILENAME = 'Unchecked_' + FUND_MANAGER + '_' + req_date + '_broker_trades.csv'
		
		# If this file exists, then there should not be any additional headers, and it should append, rather than
		# overwrite.
		if exists(BROKER_FILENAME):
			headers = False
			mode = 'a'
		# If the file doesn't exist then use the header array and use the 'writer' file.
		else:
			headers = BROKER_HEADERS_GENERATOR
			mode = 'w'
		df.to_csv(BROKER_FILENAME, index=False, mode=mode, header=headers)
		return BROKER_FILENAME
