from AOL.Resources.constants import Constants


class FundDetails:
	def __init__(self, row):
		self.consts = Constants()
		self.Reader_Sheet = Constants().Reader_Sheet
		self.BNYAddress = None
		self.Fund_Name = None
		self.ISIN = None
		self.Designation_List = None
		self.variable_definition(row)
		self.bny_address_finder()
		self.ADDR = self.BNYAddress
	
	def bny_address_finder(self):
		try:
			if "gb" in self.ISIN[0:2].lower():
				self.BNYAddress = "The Bank of New York Nominees Ltd, 1 Piccadilly Gardens, Manchester, M1 1RN"
			else:
				self.BNYAddress = "The Bank of New York Custodial Nominees (Ireland) Ltd, 70 Sir Rogerson’s Quay, " \
				                  "Dublin 2 216410"
		except AttributeError:
			pass
		except TypeError:
			pass
	
	def variable_definition(self, row):
		self.Fund_Name = self.Reader_Sheet.cell(row=row, column=self.consts.FundNameColumn).value
		self.ISIN = self.Reader_Sheet.cell(row=row, column=self.consts.ISINColumn).value
		self.Designation_List = self.Reader_Sheet.cell(row=row, column=self.consts.DesignationColumn).value

