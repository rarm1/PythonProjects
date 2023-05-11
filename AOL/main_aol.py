import os
import pathlib
import time
from pathlib import Path

import comtypes.client
import docx

from agency import Agency
from constants import Constants
import constants as const
from email_creation import Email
from fund_details import FundDetails
from input_document import InputDocument
from output_document import OutputDocument


def allowable_execution(row: int) -> object:
	if InputDocument().Reader_Sheet.cell(row=row, column=Constants().FundNameColumn).value is None:
		return False
	else:
		return True


def create_new_document(filepath, fund, agent):
	search = []
	constants = Constants()
	doc_to_read = docx.Document(filepath)
	for paragraph in doc_to_read.paragraphs:
		for idx, r in enumerate(paragraph.runs):
			replace = False
			if "{" in r.text:
				search = []
				for letter in r.text:
					if letter == "{":
						replace = True
					if replace:
						search.append(letter)
					if letter == "}":
						break
				search = "".join(search)
			if replace:
				replacement_text = str
				to_search = search[1:-1]
				if "date" in to_search.lower():
					replacement_text = r.text.replace(search, const.date_format)
				elif "fund_name" in to_search.lower():
					replacement_text = r.text.replace(search, fund.Fund_Name)
				elif "isin" in to_search.lower():
					replacement_text = r.text.replace(search, fund.ISIN)
				elif "designation_list" in to_search.lower():
					replacement_text = r.text.replace(search, constants.Designation_List)
				
				elif "addr" in to_search.lower():
					replacement_text = r.text.replace(search, fund.BNYAddress)
				elif "agency_code" in to_search.lower():
					if agent.Agency_Code is None:
						replacement_text = r.text.replace(search, "")
					else:
						replacement_text = r.text.replace(search, agent.Agency_Code)
				paragraph.runs[idx].text = replacement_text
	filepath = Path(filepath)
	doc_to_read.save(filepath)


def process_fund(row):
	if allowable_execution(row):
		print(f"Iteration: {row - 1}")
		fund = FundDetails(row)
		out = OutputDocument()
		agent = Agency(row)
		out.AOL_Filename = f'{fund.Fund_Name} AOL {Constants().Designation_List}.docx'
		out.DA_Filename = f'{fund.Fund_Name} DA {Constants().Designation_List}.docx'
		current_path = str(pathlib.Path().parent.resolve())
		current_path = str(current_path)
		out.Location = pathlib.Path(current_path, fund.Fund_Name)
		if not os.path.exists(out.Location):
			os.makedirs(out.Location)
		out.create_files()
		out.AOL_pdf_filename = str(pathlib.Path(out.AOL_Written_File_Path).with_suffix(".pdf"))
		out.DA_pdf_filename = str(pathlib.Path(out.DA_Written_File_Path).with_suffix(".pdf"))
		create_new_document(out.AOL_Written_File_Path, fund, agent)
		create_new_document(out.DA_Written_File_Path, fund, agent)
		word = comtypes.client.CreateObject('Word.Application')
		word.Visible = False
		doc1 = word.Documents.Open(os.path.abspath(out.AOL_Written_File_Path))
		doc1.SaveAs(out.AOL_pdf_filename, 17)
		doc2 = word.Documents.Open(os.path.abspath(out.DA_Written_File_Path))
		doc2.SaveAs(out.DA_pdf_filename, 17)
		word.Quit()
		email = Email(agent, fund)
		email.save_email(out)


def main():
	input_document = InputDocument()
	input_sheet = input_document.Reader_Sheet
	for row in range(2, input_sheet.max_row + 1):
		process_fund(row)


if __name__ == '__main__':
	start_time = time.time()
	
	main()
	
	end_time = time.time()
	total_time = end_time - start_time
	
	print(f"Program completed in {total_time} seconds.")
