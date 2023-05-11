import pandas as pd
import re
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Read the Excel file into a DataFrame
file_path = 'Progeny 2 Account Numbers.xlsx'
df = pd.read_excel(file_path)

# Group by sales rep name and email
grouped = df.groupby(['Sales rep name', 'Sales rep email']).agg({
    'Security Name': list,
    'ISIN': list,
    'Account Number 303484': lambda x: list(set(x)),
    'Account Number 303559': lambda x: list(set(x)),
    'Account Number 303566': lambda x: list(set(x)),
    'Agency Number': 'first'
}).reset_index()



def create_email(row):
    funds = '\n'.join([f'{name} ({isin})' for name, isin in zip(row['Security Name'], row['ISIN'])])
    agency_code_line = f"Our agent code is {row['Agency Number']}." if not pd.isnull(row['Agency Number']) else ''

    email_body = f"""Good afternoon {row['Sales rep name']},<br><br>
    I hope you are well!<br><br>
    We have opened some accounts with you ahead of the launch of our Progeny 2 funds, we will be seeding these accounts next week.<br><br>
    I just wanted to confirm you are able to waive any minimum investment amounts for the seeding period, please?<br><br>
    For reference, we are looking to invest in the following funds:<br>
    {funds}<br><br>
    I have included a list of our account numbers below.<br>
    Designation 303484 – {', '.join(map(str, row['Account Number 303484']))}<br><br>
    Designation 303559 – {', '.join(map(str, row['Account Number 303559']))}<br><br>
    Designation 303566 – {', '.join(map(str, row['Account Number 303566']))}<br><br>
    {agency_code_line}<br><br>
    I would appreciate if you could confirm minimum investment amounts can be waived.<br><br>
    Many thanks!<br><br>
    Kind regards,<br><br>
    Jenny"""

    return email_body

emails = []

for index, row in grouped.iterrows():
    email = create_email(row)
    emails.append([email, row['Sales rep email']])

for email, sales_reps in emails:
    msg = MIMEMultipart()
    msg['Subject'] = "Margetts & Progeny 2 Fund Launch - Seeding Period"

    msg['To'] = sales_reps
    part = MIMEText(email, 'html')
    msg.attach(part)

    valid_filename = re.sub(r'[^\w\.-]+', '_', sales_reps)

    with open(valid_filename + ".eml", 'w') as outfile:
        outfile.write(msg.as_string())
