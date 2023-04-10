import pandas as pd


class DataProcessing:
	"""

	"""
	
	# This should be automated, defining it removes the point of the whole process.
	def __init__(self, unprocessed_document: pd.DataFrame):
		self.UnprocessedDocument = unprocessed_document
		self.FundName = 'Group/Investment'
		self.ISIN = 'ISIN'
		self.IASector = 'IA Sector'
		self.StyleBox = 'Equity Style Box (Long)'
		self.AverageCap = 'Average Market Cap (mil) (Long)'
		self.ValueGrowth = 'Value-Growth Score (Long)'
		self.UpCapRatio = 'Up Capture Ratio'
		self.DownCapRatio = 'Down Capture Ratio'
		self.UpDownDifference = 'Up Down Difference'
		self.Headers = [self.FundName, self.ISIN, self.IASector, self.AverageCap, self.ValueGrowth, self.UpCapRatio,
		                self.DownCapRatio, self.UpDownDifference]
		self.Output_DF = pd.DataFrame()
		self.process_df()
	
	def process_df(self):
		"""

		"""
		try:
			self.UnprocessedDocument[self.UpDownDifference] = \
				self.UnprocessedDocument[self.UpCapRatio].astype(float) - \
				self.UnprocessedDocument[self.DownCapRatio].astype(float)
			self.UnprocessedDocument = self.UnprocessedDocument.sort_values(by=self.UpDownDifference, ascending=False)
		except TypeError as te:
			print(f"Error generated, none floatable value has been passed to the process_df Function {te}")
		self.Output_DF = self.UnprocessedDocument[self.Headers]
