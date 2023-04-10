import chardet
import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)


class ISINToTicker:
	"""
	A class that converts ISIN codes to tickers.
	"""
	
	_document = None
	
	def __init__(self, **kwargs):
		self.kwargs = kwargs
	
	@property
	def tickers(self):
		"""
		Returns the tickers corresponding to the given ISIN codes.
		"""
		return self._find_ticker()
	
	@property
	def urls(self):
		"""
		Returns the urls corresponding to the given tickers.
		"""
		return self._find_url()
	
	@property
	def thirty_rolling_avg(self):
		"""

		:return:
		"""
		return self._find_30d()
	
	@classmethod
	def _read_csv(cls):
		"""
		Reads the ISIN_to_Ticker.csv file and returns a pandas DataFrame.
		"""
		if cls._document is None:
			with open('../ISIN_to_Ticker.csv', 'rb') as f:
				result = chardet.detect(f.read())
			cls._document = pd.read_csv("../ISIN_to_Ticker.csv", encoding=result['encoding'])  #
		return cls._document
	
	def _find_ticker(self):
		"""
		Finds and returns the tickers corresponding to the given ISIN codes.
		"""
		document = self._read_csv()
		tickers = [document.loc[document['ISIN'] == isin, 'Ticker'].values[0] for isin in self.kwargs['isin']]
		return tickers
	
	def _find_url(self):
		document = self._read_csv()
		urls = [[ticker,
		         document.loc[document['Ticker'] == ticker, 'URL'].values[0],
		         document.loc[document['Ticker'] == ticker, 'Currency'].values[0]]
		        for ticker in self.kwargs['tickers']]
		return urls
	
	def _find_30d(self):
		document = self._read_csv()
		thirty_day_rolling = [document.loc[document['Ticker'] == ticker, '30d Avg'].values[0]
		                      for ticker in self.kwargs['tickers']]
		return thirty_day_rolling
