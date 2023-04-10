from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


# TODO: This should take into account whether trades are from progeny or not (for settle + 4)


class Email:
	def __init__(self):
		self.recipient_list = ['fundmanagers@margetts.com']
		self.subject = "Margetts Fund Management: Progeny Trades"
		self.Salutation = self.morning_afternoon()
	
	@staticmethod
	def morning_afternoon():
		now = datetime.now()
		if now.hour < 12:
			return "Good Morning"
		else:
			return "Good Afternoon"
	
	def write_email(self, trade_table, proof_table):
		body = f"{self.Salutation}, <br><br>" \
		       f"We would like to place the following trades please,<b> these are to settle T+4</b>.<br><br>" \
		       f"{trade_table}<br><br>" \
		       f"Please don't hesitate to get in touch if there is any further " \
		       f"information we are able to provide.<br><br>" \
		       f"Best Regards, <br><br>" \
		       f"{proof_table}"
		return body
	
	def save_email(self, trade_table, proof_table):
		msg = MIMEMultipart()
		msg['Subject'] = self.subject
		msg['To'] = "; ".join(self.recipient_list)
		body = self.write_email(trade_table, proof_table)
		part = MIMEText(body, 'html')
		msg.attach(part)
		with open("BrokerTest.eml", 'w') as outfile:
			outfile.write(msg.as_string())
