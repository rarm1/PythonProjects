import os
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Email:
	def __init__(self, agency, fund_details):
		self.recipient_list = ['richard.armstrong@margetts.com', 'fundmanagers@margetts.com']
		self.cc_list = ['cctest@gmail.com']
		self.FundName = fund_details.Fund_Name
		self.ISIN = fund_details.ISIN
		self.Designations = fund_details.Designation_List
		self.Agent = "Margetts Fund Management"
		self.Agency_Code = agency.Agency_Code
		self.ta_address = agency.Agent_Address
		self.Contact_Details = agency.Agent_Phone
		self.subject = self.subject_writer()
		self.Salutation = self.morning_afternoon()
		self.files = []
	
	def write_email(self):
		self.ta_address = '<br>'.join(self.ta_address.splitlines())
		return f"{self.Salutation}, <br><br>" \
		       f"" \
		       f"Please find attached the necessary documentation to open an account for the holding: <br><br>" \
		       f"" \
		       f"Fund Name: {self.FundName}<br>" \
		       f"ISIN: {self.ISIN}<br>" \
		       f"Designations: {self.Designations}<br>" \
		       f"Agent: {self.Agent}<br>" \
		       f"{self.Agency_Code + '<br>' if self.Agency_Code is not None else ''}<br>" \
		       f"The application form and relevant documents should be sent to: <br>" \
		       f"{self.ta_address}<br><br>" \
		       f"{',<br>'.join(self.Contact_Details.splitlines())}<br><br>" \
		       f"Should the application form or the TA request it: <br>" \
		       f"•             The initial investment amount is approximately Â£3m<br>" \
		       f"•             The subsequent investment amounts will be approximately Â£100K each<br>" \
		       f"•             The trading frequency will be ad hoc <br>" \
		       f"<br> We would be grateful if you would include the reference noted in the email subject in any" \
		       f" further correspondence and provide the account numbers once the accounts are open. <br><br>" \
		       f"Please let me know if you have any further requestions. <br><br>" \
		       f"Kind Regards<br>"
	
	def save_email(self, output):
		msg = MIMEMultipart()
		msg['Subject'] = self.subject
		msg['To'] = "; ".join(self.recipient_list)
		msg['cc'] = "; ".join(self.cc_list)
		part = MIMEText(self.write_email(), 'html')
		msg.attach(part)
		os.makedirs(output.Location, exist_ok=True)
		files = [output.AOL_pdf_filename, output.DA_pdf_filename]
		for file in files:
			with open(file, 'rb') as attachment:
				part = MIMEBase('application', 'octet-stream')
				part.set_payload(attachment.read())
				encoders.encode_base64(part)
				filename = "/".join(file.split("\\")[-1:])
				part.add_header('Content-Disposition', f'attachment; filename={filename}')
				msg.attach(part)
		with open(output.Location + self.FundName + ".eml", 'wb') as outfile:
			outfile.write(msg.as_bytes())
	
	def subject_writer(self):
		return f"(Ref: TBC) {self.FundName} - Account Opening for Designation {self.Designations}"
	
	@staticmethod
	def morning_afternoon():
		now = datetime.now()
		if now.hour < 12:
			return "Good Morning"
		else:
			return "Good Afternoon"
