from AOL.Resources.constants import Constants


class Agency:
	def __init__(self, row):
		self.const = Constants()
		self.Reader_Sheet = self.const.Reader_Sheet
		self.Agency_Code = None
		self.Agent_Address = None
		self.Agent_Phone = None
		self.fetch_vars(row)
	
	def fetch_vars(self, row):
		self.Agency_Code = self.Reader_Sheet.cell(row=row, column=self.const.AgentCodeColumn).value
		if self.Agency_Code is not None:
			self.Agency_Code = "Agency Code: " + str(self.Agency_Code)
		self.Agent_Address = self.Reader_Sheet.cell(row=row, column=self.const.TAAddressColumn).value
		self.Agent_Phone = self.Reader_Sheet.cell(row=row, column=self.const.TAPhoneFaxColumn).value
