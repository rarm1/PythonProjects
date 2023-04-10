from datetime import date, datetime

import docx


class Constants:
	def __init__(self):
		self.today = datetime.now()
		self.date_format = date(day=self.today.day, month=self.today.month, year=self.today.year).strftime('%A %d %B '
		                                                                                                   '%Y')
		self.designations = [116011, 116018, 116043, 116048]
		self.designations_str = [str(i) for i in self.designations]
		self.Designation_List = ", ".join(self.designations_str)
		self.AOL_Template_Doc = docx.Document("AOL_Template_4.docx")
		self.DA_Template_Doc = docx.Document("DA_Template_4.docx")
		self.fund_list_filename = "Fund_List_V4.xlsx"
		self.FundNameColumn = 1
		self.AgentCodeColumn = 2
		self.ISINColumn = 3
		self.TAAddressColumn = 4
		self.TAPhoneFaxColumn = 5
