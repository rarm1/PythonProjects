# def product_percentage_converted(arr: list, equally_weighted: bool = True, weightings: list = list) -> [list, float,
#                                                                                                         list]:
#     """
#     Parameters
#     ----------
#     arr : list
#         This list contains the weekly returns of the portfolio.
#     equally_weighted : bool, optional
#         This variable is not yet used in input. Determines whether portfolio is equal weight. The default is True.
#
#     weightings : list, optional
#         This variable is not yet used in input.
#         Determines the weighting of the portfolio if weights aren't equal.
#         The default is an empty list.
#     Returns
#     -------
#     [list, float, list]
#         Returns a variety of outputs to allow for greater flexibility in development. This can be reduced eventually.
#     return_arr : list
#         Probably the first to go in terms out output and post-processing.
#         Returns an array of weekly returns converted from decialised returns to percentage. I.e. instead of:
#         1.00 (To represent one percent growth) it will return 1.01.
#     Weekly variance : float
#         This calculates the variance of the intraweek returns.
#     weighted_returns_arr : list
#         This takes into account the weights. This does not function entirely as if the weightings are not equal, then,
#         variance will be skewed.
#     """
#
#     return_arr = []
#     without_one = []
#     weight = None
#     for i in arr:
#         return_arr.append(1 + (i / 100))
#         without_one.append(i / 100)
#     if equally_weighted:
#         weight = 1 / len(arr)
#     # This needs to be changed, not accurate. Final return can't be a sum it must be a multiplication.
#     if weight is None:
#         weighted_returns_arr = sum([a / weightings[i] for a, i in enumerate(return_arr)])
#     else:
#         # print(f"Return arr: {return_arr}")
#         # print(f"Weight: {weight}")
#         weighted_returns_arr = sum([(a * weight) for a in return_arr])
#         # print(f"Weighted returns arr: {weighted_returns_arr}")
#     weekly_variance = np.var(arr)
#     return return_arr, weekly_variance, weighted_returns_arr

#
# def portfolio_analysis(weekly_returns_for_portfolio: list):
#     """
#     Parameters
#     ----------
#     weekly_returns_for_portfolio : list
#         DESCRIPTION.
#     Returns
#     -------
#     None.
#     """
#     weekly_return_arr, variance_arr, weighted_weekly_returns_arr = [], [], []
#     # These returns are the individual weekly returns for each portfolio.
#     for weekly_returns_split_ports in weekly_returns_for_portfolio:
#         weekly_return, variance, weighted_weekly_returns = product_percentage_converted(weekly_returns_split_ports)
#         weekly_return_arr.append(weekly_return)
#         variance_arr.append(variance)
#         weighted_weekly_returns_arr.append(weighted_weekly_returns)
#     # TODO: Add return Clause
#     # print(f'Weekly returns for portfolio: {[sum(i) for i in weekly_returns_for_portfolio]}')
#     # print(f"Variance of variance (portfolio variance): {np.var(variance_arr)}")
#     # print(f"Weighted weekly returns{weighted_weekly_returns_arr}\n")
#     return variance_arr, weighted_weekly_returns_arr

####### Main ########
# UNCOMMENT ALL FROM HERE ##########
# array_of_all_funds_returns = []
# dataframe_funds = [list(all_funds[i][3:]) for i in combinations_arr[idx[0]][adx[0]]]
# fund_names = [all_funds[i].name for i in combinations_arr[idx[0]][adx[0]]]
# array_of_all_funds_returns = list(zip(*dataframe_funds))  # Creates the weekly returns
# # # TODO: Maybe if I could collect the names of the funds that are in the 'best' 50 portfolios
# # #   then I could get a list of the most commonly mentioned? I don't need to return fund names
# # #   in a function that collects them, I just need to pass them back in.
# # print(fund_names)
# variance_arr, weighted_weekly_returns = portfolio_analysis(array_of_all_funds_returns)
# basic_ranking_gen(variance_arr, weighted_weekly_returns)
# TO HERE ##############
