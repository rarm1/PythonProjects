# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 08:30:44 2022

@author: RArm1
"""
import io
from operator import itemgetter

import matplotlib.pyplot as plt
import numpy as np
# TODO: I think using the pd.correl function would let me select funds that are highly uncorrelated.
import pandas
import scipy as sc
import xlsxwriter as xl
from numpy import ndarray

import strip_by_rrr as rrr

# Globals / bound definitions.
GENERATED_PORTFOLIO_RETURNS_DF = pandas.DataFrame()
df, sector = rrr.strip_main()

df._drop_na(axis=1, how='any', inplace=True)
isin_df = df.iloc[[0]]
isin_list = isin_df.values.tolist()[0]
cap_df = df.iloc[[1]]
gv_df = df.iloc[[2]]
df.drop(df.index[[0, 1, 2]], inplace=True, axis=0)
df.rename_axis(mapper=None, axis=1, inplace=True)
df = df.astype(float)
df /= 100
covmat = df.cov()

sector.drop(sector.index[[0, 1, 2]], inplace=True)
sector.astype(float)
sector /= 100
sector_var = sector.var()

positive_sector = sector.loc[sector > 0.0]
sector_ret_list = sector.values.tolist()
positive_sector_indexes = [idx for idx, sector_ret in enumerate(sector_ret_list) if sector_ret > 0.00]
positive_sector_list = positive_sector.values.tolist()
sum_positive_returns_sector = sum(positive_sector_list)

negative_sector = sector.loc[sector <= 0.00]
negative_sector_indexes = [idx for idx, sector_ret in enumerate(sector_ret_list) if sector_ret <= 0.00]
negative_sector_list = negative_sector.values.tolist()
sum_negative_returns_sector = sum(negative_sector_list)

excess_returns_dataframe = df.copy()
for col in excess_returns_dataframe:
	excess_returns_dataframe[col] -= sector
excess_returns_dataframe = excess_returns_dataframe.astype('float')

sector_start = 1
sector_time_series = [sector_start]
for sec_ret in range(sector.shape[0]):
	sector_start *= sector[sec_ret] + 1
	sector_time_series.append(sector_start)

lower_bound_threshold = gv_df.min().min()
upper_bound_threshold = gv_df.max().max()
growth_value_bounds = [100, 150, 200]
cap_bounds = [1500, 4500, 7500]
# ann_rets = opt_lib.annualise_rets(df, 52)
iteration_count = 0

workbook = xl.Workbook("Output Test Correll Min Func Full Dataset.xlsx")

# CONTS
global WORKSHEET
GV_BEING_RUN = 0
RFR = 0.01
PORT_NAMES = ['Small Value', 'Small Core', 'Small Growth',
              'Mid Value', 'Mid Balanced', 'Mid Growth',
              'Large Value', 'Large Balanced', 'Large Growth']


# The idea of this function is that it should aim for the lowest level of correlation between the funds.
def correlation_func(weights):
	"""

	:param weights:
	:return:
	"""
	global iteration_count
	iteration_count += 1
	print(f"\rGrowth Value Bracket: {PORT_NAMES[GV_BEING_RUN]}. Iteration number: {iteration_count}", end="")
	return (weights @ excess_returns_dataframe.corr().T).min()


def weightings_contraint(weights: list) -> float:
	"""

	:param weights:
	:return:
	"""
	if np.sum(weights) - 1.00 == 0.00:  # If the sum of float value minus one is 0 then we're at a 'full' portfolio.
		return 0.0
	else:
		return np.sum(weights) - 1  # This returns so the program knows how far off from goal weights we are.


def growth_value_contraint(weights: list) -> np.ndarray:
	"""

	:param weights:
	:return:
	"""
	return np.dot(weights, gv_df.T)


def cap_constraint(weights):
	"""

	:param weights:
	:return:
	"""
	return np.dot(weights, cap_df.T)


def optimise(target_gvs, target_cap):
	"""

	:param target_gvs:
	:param target_cap:
	:return:
	"""
	global GV_BEING_RUN
	lb, ub = 0.0, 0.1
	bounds = (lb, ub)
	first_weights: ndarray = np.repeat(1 / df.shape[1], df.shape[1])
	weighting_bounds = [bounds for _ in range(df.shape[1])]
	bnds = weighting_bounds
	weight_cons = {'type': 'eq', 'fun': weightings_contraint}
	gv_cons = {'type': 'eq', 'fun': lambda weights: target_gvs - growth_value_contraint(weights)}
	cap_cons = {'type': 'eq', 'fun': lambda weights: target_cap - cap_constraint(weights)}
	
	cons = {"Weight": weight_cons, "Growth Value": gv_cons, "Size": cap_cons}
	results = sc.optimize.minimize(correlation_func,
	                               x0=first_weights,
	                               # args=covmat,
	                               method="SLSQP",
	                               bounds=bnds,
	                               constraints=cons
	                               # , options={'disp': True}
	                               )
	GV_BEING_RUN += 1
	print()
	return results.x


def port_generator():
	"""

	:return:
	"""
	all_ports_ex_zero = []
	all_ports_inc_zero = []
	for gv_target in growth_value_bounds:
		for cap in cap_bounds:
			# gv_target, cap = 150, 6000
			output_arr = optimise(gv_target, cap)
			including_zeros_arr = []
			excluding_zeros_arr = []
			for idx, weighting in enumerate(output_arr):
				including_zeros_arr.append([df.columns[idx], str(round(weighting, 2) * 100) + '%'])
				if round(weighting, 2) != 0.00:
					excluding_zeros_arr.append([df.columns[idx], str(round(weighting, 2) * 100) + '%',
					                            isin_list[idx]])
			funds = []
			weightings = []
			for fund, weighting, isin in excluding_zeros_arr:
				funds.append(fund)
				weightings.append(weighting)
			all_ports_ex_zero.append(excluding_zeros_arr)
			all_ports_inc_zero.append(including_zeros_arr)
	return all_ports_ex_zero


def time_series(suggested_portfolio):
	"""

	:param suggested_portfolio:
	:return:
	"""
	fund_names = [fund_name[0] for fund_name in suggested_portfolio]
	portfolio_df = df[fund_names].copy()
	for fund_name, weighting_str in suggested_portfolio:
		weighting = float(weighting_str) / 100
		portfolio_df[fund_name] *= weighting
	starting_point = 1
	time_series_suggested_port = [starting_point]
	weekly_returns = []
	for idx in range(portfolio_df.shape[0]):
		weekly_return = (np.sum(portfolio_df.iloc[idx]))
		weekly_returns.append(weekly_return)
		starting_point *= (weekly_return + 1)
		time_series_suggested_port.append(starting_point)
	return time_series_suggested_port, weekly_returns


def write_returns_graph(weekly_returns):
	"""

	:param weekly_returns:
	"""
	img_data = io.BytesIO()
	plt.plot(np.array(sector_time_series), c='blue', label='Sector')
	plt.plot(np.array(weekly_returns), c='red', label='Suggested Portfolio')
	plt.title('Returns')
	plt.legend()
	plt.savefig(img_data, format='png')
	WORKSHEET.insert_image(10, 12, '', {'image_data': img_data})
	plt.close()


def write_weightings_graph(data, labels):
	"""

	:param data:
	:param labels:
	"""
	img_data = io.BytesIO()
	plt.pie(data, labels=labels)
	plt.title('Holdings')
	plt.savefig(img_data, format='png')
	WORKSHEET.insert_image(10, 3, '', {'image_data': img_data})
	plt.close()


def maths_functions(df1: pandas.DataFrame):
	"""

	:param df1:
	"""
	WORKSHEET.write(0, 5, "Sharpe Ratio")
	# WORKSHEET.write(1, 5, opt_lib.sharpe_ratio(df1))
	#
	# upside_capture_ratio, downside_capture_ratio = opt_lib.capture_ratio(weekly_returns_list, sector_ret_list)
	# WORKSHEET.write(0, 6, "Upside Capture Ratio")
	# WORKSHEET.write(1, 6, upside_capture_ratio)
	#
	# WORKSHEET.write(0, 7, "Downside Capture Ratio")
	# WORKSHEET.write(1, 7, downside_capture_ratio)
	
	WORKSHEET.write(0, 8, "Portfolio SD")
	WORKSHEET.write(1, 8, df1.std())
	
	WORKSHEET.write(0, 9, "Drawdown")


# WORKSHEET.write(1, 9, opt_lib.max_drawdown(pandas.Series(weekly_returns_list)))

# win_ratio = (opt_lib.win_ratio(weekly_returns_list, sector_ret_list))
# WORKSHEET.write(0, 10, "Win Ratio")
# WORKSHEET.write(1, 10, win_ratio)


def function_main():
	"""

	:return:
	"""
	global WORKSHEET, GENERATED_PORTFOLIO_RETURNS_DF
	all_ports_ex_zero = port_generator()
	all_returns_arr = []
	for idx, port in enumerate(all_ports_ex_zero):
		WORKSHEET = workbook.add_worksheet(PORT_NAMES[idx])
		WORKSHEET.write(0, 0, "Strategy")
		WORKSHEET.write(0, 1, "ISIN")
		WORKSHEET.write(0, 2, "Weighting")
		for i, [fund_name, weighting, isin] in enumerate(port):
			WORKSHEET.write(i + 1, 0, fund_name)
			WORKSHEET.write(i + 1, 1, isin)
			WORKSHEET.write(i + 1, 2, weighting)
		suggested_portfolio = [[fund[0], round(float(fund[1][:-1]), 2)] for fund in port]
		portfolio_sorted_weightings = sorted(suggested_portfolio, key=itemgetter(1))
		time_series_portfolio, weekly_returns_arr = time_series(portfolio_sorted_weightings)
		GENERATED_PORTFOLIO_RETURNS_DF[PORT_NAMES[idx]] = weekly_returns_arr
		df_for_portfolio = pandas.DataFrame(weekly_returns_arr)
		all_returns_arr.append(time_series_portfolio)
		# This can be inserted back in to add in graphs if we need them.
		# """
		fund_names_arr = [fund[0] for fund in portfolio_sorted_weightings]
		weights_arr = [fund[1] for fund in portfolio_sorted_weightings]
		write_weightings_graph(weights_arr, fund_names_arr)
		write_returns_graph(time_series_portfolio)
		# """
		# TOADD: Function in here that writes the 'maths' to each document. This will include things such as sharpe
		# ratio, win ratio, max_drawdown, standard deviation, up/downside capture.
		maths_functions(df_for_portfolio)
	return all_returns_arr


def main():
	"""

	"""
	all_returns_arr = function_main()
	worksheet = workbook.add_worksheet("Portfolio Comparison")
	img_data = io.BytesIO()
	plt.plot(np.array(sector_time_series), c='blue', label='Sector')
	plt.title('Returns')
	worksheet.write(0, 0, "Investment Style")
	worksheet.write(0, 1, "Total Return")
	for i, port in enumerate(all_returns_arr):
		worksheet.write(i + 1, 0, PORT_NAMES[i])
		worksheet.write_number(i + 1, 1, port[-1])
		plt.plot(np.array(port), label=PORT_NAMES[i])
	plt.legend()
	plt.savefig(img_data, format='png')
	worksheet.insert_image(4, 4, '', {'image_data': img_data})
	plt.close()
	workbook.close()


if __name__ == '__main__':
	main()
	print("Complete")
