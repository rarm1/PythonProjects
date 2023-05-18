from datetime import date, datetime

import docx

today = datetime.now()
user_input = input("What is the date of the AOL? (Press Enter to use today's date)")
if user_input != "":
	date_format = (datetime.strptime(user_input, "%d/%m/%Y")).strftime('%A %d %B %Y')
else:
	date_format = date(day=today.day, month=today.month, year=today.year).strftime('%A %d %B %Y')

class Constants:
	def __init__(self):
		self.date_format = date_format
		self.designations = [352885, 352887, 352889]
		self.designations_str = [str(i) for i in self.designations]
		self.Designation_List = ", ".join(self.designations_str)
		self.AOL_Template_Doc = docx.Document("AOL_Template_4.docx")
		self.DA_Template_Doc = docx.Document("DA_Template_4.docx")
		self.fund_list_filename = "AFH Template AOL, DA, Email.xlsx"
		self.FundNameColumn = 1
		self.AgentCodeColumn = 2
		self.ISINColumn = 3
		self.TAAddressColumn = 4
		self.TAPhoneFaxColumn = 5
