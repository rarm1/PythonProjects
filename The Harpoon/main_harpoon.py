import pandas as pd

from assets import file_id_reader
from assets.var_definitions import Report

def obtain_file():
	all_files = file_id_reader.list_all_files(exclusions=["Comparison Template v1.1.xlsx"])
	filename_user = file_id_reader.user_selected_file(all_files)
	filename = file_id_reader.file_name_generator(filename_user)[0]
	port_hold_df = pd.read_excel(filename, sheet_name="Portfolio holdings", header=None)
	port_comp_df = pd.read_excel(filename, sheet_name="Portfolio Comparison", header=None)
	perf_comp_df = pd.read_excel(filename, sheet_name="Performance Comparison", header=None)
	return port_hold_df, port_comp_df, perf_comp_df, filename


def harpoon():
	port_hold_df, port_comp_df, perf_comp_df, filename = obtain_file()
	rep = Report(port_hold_df, port_comp_df, perf_comp_df)
	with open(f'{filename[:-5]}.txt', 'w') as f:
		f.write(rep.intro_text)
		f.write(rep.asset_allocation_text)
		f.write(rep.performance_text)
		f.write(rep.ongoing_charges_text)


if __name__ == '__main__':
	harpoon()
