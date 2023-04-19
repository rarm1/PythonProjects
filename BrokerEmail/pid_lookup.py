import chardet
import pandas as pd


class PIDLookup:
	"""

	"""
	
	def __init__(self, pid):
		self.pid = pid
		with open('pid_lookup.csv', 'rb') as f:
			result = chardet.detect(f.read())
		self.document = pd.read_csv('pid_lookup.csv', encoding=result['encoding'])
	
	@property
	def designation_lookup(self):
		"""

		:return:
		"""
		allocations = [
			f"{str(self.document.loc[self.document['pID'] == p, 'PortfolioLongName'].values[0])} "
			f"{int(self.document.loc[self.document['pID'] == p, 'Designation'].values[0])}"
			for p in self.pid
		]
		return allocations
