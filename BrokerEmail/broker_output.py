import pandas as pd

from isin_to_ticker import ISINToTicker
from pid_lookup import PIDLookup
from price_finder import Prices

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)


class BrokerOutput:
	"""Generates a broker output DataFrame from a given dealing_sheet."""
	
	def __init__(self, dealing_sheet):
		self.Tickers_Dict = None
		self.share_quantities = None
		self.price_per_share = None
		self.document = dealing_sheet.document
		self.Filetype = dealing_sheet.filetype
		
		column_mapping = {
			"xlsx": {"Security": "SecurityNameLong", "ISIN": "ISIN", "Shares": "Units", "Allocation": "PortfolioName",
			         "TradeID": "TradesTempID"},
			"csv": {"Security": "SecurityName", "ISIN": "SecurityIdentifier", "Shares": "Value",
			        "Allocation": "SchemeIdentifier", "TradeID": "TradeIdentifier"}
		}
		
		self.column_map = column_mapping[self.Filetype]
		headers = ['Action', 'Security', 'ISIN', 'Ticker', 'Shares', 'Approx. Notional Value',
		           'Currency', 'Allocation', 'Margetts Trade Reference']
		
		self.instructionoutput = pd.DataFrame(columns=headers)
		self.tickers = []
		self.define_attributes()
	
	def define_attributes(self):
		"""

		"""
		self.set_action()
		self.set_security()
		self.set_isin()
		self.set_ticker()
		self.set_shares()
		self.set_currency()
		self.set_allocation()
		self.set_trade_id()
		self.set_price_per_share()
		self.apply_prices()
	
	# self.apply_urls()
	
	def set_security(self):
		"""

		"""
		self.instructionoutput['Security'] = self.document[self.column_map["Security"]]
	
	def set_action(self):
		"""

		"""
		self.instructionoutput['Action'] = self.document['Direction']
	
	def set_isin(self):
		"""

		"""
		self.instructionoutput['ISIN'] = self.document[self.column_map["ISIN"]]
	
	def set_ticker(self):
		"""

		"""
		isin_to_ticker = ISINToTicker(isin=self.instructionoutput['ISIN'])
		self.instructionoutput['Ticker'] = isin_to_ticker.tickers
		self.tickers = self.instructionoutput['Ticker']
	
	def set_shares(self):
		"""

		"""
		self.instructionoutput['Shares'] = self.document[self.column_map["Shares"]]
		self.share_quantities = self.instructionoutput['Shares']
	
	def set_price_per_share(self):
		"""

		"""
		prices = Prices(self.tickers)
		self.Tickers_Dict = prices.Prices
	
	def set_currency(self):
		"""

		"""
		currency_template = ['GBP' for _ in range(len(self.instructionoutput['Approx. Notional Value']))]
		self.instructionoutput['Currency'] = currency_template
	
	def set_allocation(self):
		"""

		"""
		pid_lookup = PIDLookup(self.document['SchemeID'])
		self.instructionoutput['Allocation'] = pid_lookup.designation_lookup
	
	# self.output['Allocation'] = self.document[self.column_map["Allocation"]]
	
	def set_trade_id(self):
		"""

		"""
		self.instructionoutput['Margetts Trade Reference'] = self.document[self.column_map["TradeID"]]
	
	def apply_prices(self):
		"""

		"""
		for index, row in self.instructionoutput.iterrows():
			ticker = row['Ticker']
			shares = row['Shares']
			direction = row['Action']
			directional_price = float(self.Tickers_Dict[ticker][direction][:-1])
			if self.Tickers_Dict[ticker]['Currency'] == 'GBX':
				directional_price /= 100  # Convert pence to GBP
			notional_value = shares * directional_price
			formatted_notional_value = f"£{notional_value:,.2f}"
			# self.instructionoutput.at[index, 'Price per Share'] = directional_price
			self.instructionoutput.at[index, 'Approx. Notional Value'] = formatted_notional_value
			self.Tickers_Dict[ticker]['Directional Price'] = directional_price

# def apply_urls(self):
#     isin_to_ticker = ISINToTicker(isin=self.instructionoutput['ISIN'], tickers=self.tickers)
#     urls = isin_to_ticker.urls
#     urls = [_[1] for _ in urls]
#     self.instructionoutput['URLs'] = urls
