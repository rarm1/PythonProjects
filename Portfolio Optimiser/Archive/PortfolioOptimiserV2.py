# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 09:54:21 2022

@author: Richard Armstrong
"""
# TODO: I think what needs changing here is that the intraweek variance should be maximised otherwise the portfolio
#   will have good and bad weeks rather than offsetting performance.
import math

from itertools import combinations
from operator import itemgetter

import numpy as np
import pandas as pd

from strip_by_rrr import strip_main

MAX_OPERABLE_SIZE = 15
global DF


def desired_vg_translator(vg_quantiles, desired_vg):
    # I think we make this take lower constraints.
    return [0, 200]
    # if desired_vg <= 1:
    #     return [0, vg_quantiles[0]]
    # elif desired_vg >= 5:
    #     return [vg_quantiles[-1], 100000]
    # else:
    #     return [vg_quantiles[desired_vg - 2], vg_quantiles[desired_vg - 1]]


def desired_cap_translator(fund_cap, desired_cap):
    if desired_cap <= 1:
        return [0, fund_cap[0]]
    elif desired_cap >= 5:
        return [fund_cap[-1], 100000]
    else:
        return [fund_cap[desired_cap - 2], fund_cap[desired_cap - 1]]


def generate_potential_combinations(list_funds: list, vg_quantiles, fund_cap_quantiles, portfolio_length: int = 10):
    """
    Parameters
    ----------
    list_funds : list
        Fund names as well as information about each fund.
    vg_quantiles : np.Array
        Array of value growth quantiles
    fund_cap_quantiles : np.Array
        Array of cap quantiles
    portfolio_length : int, optional
        Desired length of portfolio. The default is 10.
    Returns
    -------
    combinations_arr : TYPE
        DESCRIPTION.
    """
    desired_gv = [1, 125]
    desired_cap = [0, 1000]
    combinations_arr = []
    viable_portfolios = 0
    to_check_cap = input("Check cap? y/n: ")
    if to_check_cap.lower() == 'y':
        desired_cap = int(input("Micro, small, balanced, large & giant cap: (please enter 1-5): "))
        desired_cap = desired_cap_translator(fund_cap_quantiles, desired_cap)
        to_check_cap = True
        print(desired_cap)
    else:
        to_check_cap = False
    to_check_gv = input("Check gv? y/n: ")
    if to_check_gv.lower() == 'y':
        desired_gv = int(input("Deep val, val, balanced, growth, high growth: (please enter 1-5): "))
        desired_gv = desired_vg_translator(vg_quantiles, desired_gv)
        to_check_gv = True
        print(desired_gv)
    else:
        to_check_gv = False

    # Multiple iterations
    """
    for execution in list_funds:
        if portfolio_length > len(execution):
            portfolio_length = len(execution)
        combos = list(combinations(execution, portfolio_length))
        for port in combos:
            gv = 0
            cap = 0
            for fund in port:
                gv += fund[1]
                cap += fund[2]
            else:
                write = True
                average_fund_cap = cap / portfolio_length
                average_fund_size = gv / portfolio_length
                # if to_check_gv:
                if desired_gv[0] < average_fund_size < desired_gv[1]:
                    write = True
                # if to_check_cap:
                if not desired_gv[0] < average_fund_cap < desired_gv[1]:
                    write = False
                if write:
                    viable_portfolios += 1
                    combinations_arr.append(port)
    """

    # Single iteration
    print(list_funds)
    print(portfolio_length)
    combos = list(combinations(list_funds, portfolio_length))
    print(combos)
    for port in combos:
        gv = 0
        cap = 0
        for fund in port:
            gv += fund[1]
            cap += fund[2]
        else:
            write = True
            average_fund_cap = cap / portfolio_length
            average_gv = gv / portfolio_length
            if to_check_gv:
                if not desired_gv[0] < average_gv < desired_gv[1]:
                    write = False
            if to_check_cap:
                if not desired_cap[0] < average_fund_cap < desired_cap[1]:
                    write = False
            print(write)
            if write:
                viable_portfolios += 1
                combinations_arr.append(port)
    print(f"A total of {viable_portfolios} viable portfolios found.")
    return combinations_arr


# TODO: I think that I want to move the check into here, or possibly before...
def split_funds_into_operable_lists(max_operations: int, all_funds: pd.DataFrame):
    """
    Parameters
    ----------
    max_operations : int
        DESCRIPTION.
    all_funds : pandas.DataFrame
        DESCRIPTION.

    Returns
    -------
    max_operable_fund_list : TYPE
        DESCRIPTION.
    """
    max_operable_fund_list = []
    for i in range(0, max_operations):
        if i + 1 == max_operations:
            a = list(all_funds.columns)[i * MAX_OPERABLE_SIZE:all_funds.shape[1]]  # Fund name
            b = list(all_funds.iloc[2][i * MAX_OPERABLE_SIZE:all_funds.shape[1]])  # Value Growth Score
            c = list(all_funds.iloc[1][i * MAX_OPERABLE_SIZE:all_funds.shape[1]])  # Average Market Cap
            to_append = list(zip(a, b, c))
            max_operable_fund_list.append(to_append)
        else:
            a = list(all_funds.columns)[(i * MAX_OPERABLE_SIZE):(i + 1) * MAX_OPERABLE_SIZE]  # Fund name
            b = list(all_funds.iloc[2])[i * MAX_OPERABLE_SIZE:(i + 1) * MAX_OPERABLE_SIZE]  # Value Growth Score
            c = list(all_funds.iloc[1])[i * MAX_OPERABLE_SIZE:(i + 1) * MAX_OPERABLE_SIZE]  # Average Market Cap
            to_append = list(zip(a, b, c))
            max_operable_fund_list.append(to_append)
    return max_operable_fund_list


def basic_ranking_gen(variance_arr: list, weighted_weekly_returns: list[list]):
    print(f"Variance of Variance: {sum(weighted_weekly_returns) / np.var(variance_arr)}")
    print(f"Variance of returns: {sum(weighted_weekly_returns) / np.var(weighted_weekly_returns)}")
    print(f"Final return: {weighted_weekly_returns[-1] / np.var(variance_arr)}")
    print(f"Sum returns: {sum(weighted_weekly_returns) / np.var(variance_arr)}")


def generate_weights(df, weights):
    print(df, weights)
    if weights is None:
        # Creates equally weighted portfolio
        weights = [1/df.shape[1] for _ in df.shape[1]]
        return weights
    else:
        return weights


def not_processed(df, processed):
    if not processed:
        # Drop unnecessary rows, isin, cap, gv score.
        df = df.drop(df.index[[0, 1, 2]])
        # Convert dataframe type to float.
        df = df.astype(float)
        # Divides dataframe by 100 to ensure that returns are percent change
        df = df / 100
    return df


def portfolioreturn(df, weights: list = None, processed: bool = True):
    weights = generate_weights(df, weights)
    df = not_processed(df, processed)
    return ((np.dot(df.mean(), weights)) + 1) ** len(df)


def portfoliocovariance(df, weights: list = None, processed: bool = True):
    weights = generate_weights(df, weights)
    df = not_processed(df, processed)
    return np.dot(np.dot(df.cov(), weights), weights)


def portfoliostd(df, weights: list = None, processed: bool = True):
    weights = generate_weights(df, weights)
    df = not_processed(df, processed)
    return np.dot(np.dot(df.cov(), weights), weights) ** (1 / 2)


def remove_duplicates(fund_names):
    _ = [i[1] for i in fund_names]
    fund_names_arr = [fund_name for portfolio in _ for fund_name in portfolio]
    counter_arr = []
    single_keys = list(dict.fromkeys(fund_names_arr))
    for fund_name in single_keys:
        counter_arr.append([fund_name, fund_names_arr.count(fund_name)])
    return sorted(counter_arr, key=itemgetter(1), reverse=True)


# Not used but good to have for future.
def sectorstd(sector2):
    return sector2.std()


def aggregate_funds(all_funds):
    a = list(all_funds.columns)  # Fund name
    b = list(all_funds.iloc[2])  # Value Growth Score
    c = list(all_funds.iloc[1])  # Average Market Cap
    return list(zip(a, b, c))


def sector_sorter_outerer(df):
    """
    :param df:
    :return:
    """
    '''
    Dataframes to generate:
    vs, vm, vl, = growth value within lower third gv scores and less than 1500 cap 
    bs, bm, bl, = growth value between lower third and upper third and between 1500 and 6000
    gs, gm, gl = growth value upper third and great than 6000
    '''
    # TODO: So I think what the next step is likely to be is to characterise each category as a model portfolio
    #   by doing this I will be able to generate suitable weightings for the classifications.
    #   I could also use this to inform the combinations, i.e. I want more funds from areas that I want
    #   to have a higher weighting.
    vg_scores = df.loc['Value-Growth Score (Long)'].values
    vg_triciles = list(np.quantile(vg_scores, q=np.arange(0, 1, 1 / 3)))

    df = df.T

    # Value Small
    vs = df[(
            (df['Average Market Cap (mil) (Long)'] < 1500) &
            (df['Value-Growth Score (Long)'] < vg_triciles[1])
    )].T

    # Value Mid
    vm = df[(
            ((df['Average Market Cap (mil) (Long)'] > 1500) &
             (df['Average Market Cap (mil) (Long)'] < 6000)) &
            (df['Value-Growth Score (Long)'] < vg_triciles[1])
    )].T

    # Value Large
    vl = df[(
            (df['Average Market Cap (mil) (Long)'] > 6000) &
            (df['Value-Growth Score (Long)'] < vg_triciles[1])
    )].T

    # Balanced Small
    bs = df[(
            (df['Average Market Cap (mil) (Long)'] < 1500) &
            ((df['Value-Growth Score (Long)'] > vg_triciles[1]) &
             (df['Value-Growth Score (Long)'] < vg_triciles[2]))
    )].T

    # Balanced Mid
    bm = df[(
            ((df['Average Market Cap (mil) (Long)'] > 1500) &
             (df['Average Market Cap (mil) (Long)'] < 6000)) &
            ((df['Value-Growth Score (Long)'] > vg_triciles[1]) &
             (df['Value-Growth Score (Long)'] < vg_triciles[2]))
    )].T

    # Balanced Large
    bl = df[(
            (df['Average Market Cap (mil) (Long)'] > 6000) &
            ((df['Value-Growth Score (Long)'] > vg_triciles[1]) &
             (df['Value-Growth Score (Long)'] < vg_triciles[2]))
    )].T

    # Growth Small
    gs = df[(
            (df['Average Market Cap (mil) (Long)'] < 1500) &
            (df['Value-Growth Score (Long)'] > vg_triciles[2])
    )].T

    # Growth Mid
    gm = df[(
            ((df['Average Market Cap (mil) (Long)'] > 1500) &
             (df['Average Market Cap (mil) (Long)'] < 6000)) &
            (df['Value-Growth Score (Long)'] > vg_triciles[2])
    )].T

    # Growth Large
    gl = df[(
            (df['Average Market Cap (mil) (Long)'] > 6000) &
            (df['Value-Growth Score (Long)'] > vg_triciles[2])
    )].T
    # print(vs, vm, vl, bs, bm, bl, gs, gm, gl)
    print((portfolioreturn(vs, processed=False)-1), portfoliostd(vs, processed=False))
    print((portfolioreturn(vm, processed=False)-1), portfoliostd(vm, processed=False))
    print((portfolioreturn(vl, processed=False)-1), portfoliostd(vl, processed=False))
    print((portfolioreturn(bs, processed=False)-1), portfoliostd(bs, processed=False))
    print((portfolioreturn(bm, processed=False)-1), portfoliostd(bm, processed=False))
    print((portfolioreturn(bl, processed=False)-1), portfoliostd(bl, processed=False))
    print((portfolioreturn(gs, processed=False)-1), portfoliostd(gs, processed=False))
    print((portfolioreturn(gm, processed=False)-1), portfoliostd(gm, processed=False))
    print((portfolioreturn(gl, processed=False)-1), portfoliostd(gl, processed=False))
    return vs, vm, vl, bs, bm, bl, gs, gm, gl


def main():
    """
    Main program execution. The hub of the program. No input, no return clause.
    :param:
    None
    :return:
    None
    """
    all_funds, sector = strip_main()
    # Divides dataframe by 100 to ensure that returns are percent change
    sector = sector.drop(sector.index[[0, 1, 2]])
    sector = sector.astype(float)
    sector = sector / 100

    # All Funds
    # max_operable_fund_list = aggregate_funds(all_funds)
    # vg_scores = [fund[1] for fund in max_operable_fund_list]
    # fund_caps = [fund[2] for fund in max_operable_fund_list]
    # vg_quantiles = np.quantile(vg_scores, q=np.arange(0.20, 1, 0.20))
    # fund_cap_quantiles = np.quantile(fund_caps, q=np.arange(0.20, 1, 0.20))

    # vs, vm, vl, bs, bm, bl, gs, gm, gl = sector_sorter_outerer(all_funds)

    # Multiple Iterations
    max_operations = math.ceil(all_funds.shape[1] / MAX_OPERABLE_SIZE)
    max_operable_fund_list = split_funds_into_operable_lists(max_operations, all_funds)
    vg_scores = [strategy[1] for strategy_list in max_operable_fund_list for strategy in strategy_list]
    fund_caps = [strategy[2] for strategy_list in max_operable_fund_list for strategy in strategy_list]
    vg_quantiles = np.quantile(vg_scores, q=np.arange(0.20, 1, 0.20))
    fund_cap_quantiles = np.quantile(fund_caps, q=np.arange(0.20, 1, 0.20))
    # # All executions
    combinations_arr = generate_potential_combinations(max_operable_fund_list, vg_quantiles,
                                                       fund_cap_quantiles, portfolio_length=int(len(
                                                        max_operable_fund_list)/1.1))
    sharpes = []

    sector_return = portfolioreturn(sector, [1])
    highest_sharpe = 1
    for adx in enumerate(combinations_arr):
        fund_names = [i[0] for i in adx[1]]
        df = pd.DataFrame(all_funds[fund_names])

        # Generate equally weighted portfolio
        weights = [1 / len(df.columns) for _ in enumerate(df.columns)]
        # Drop unnecessary columns - this drops the ISIN, Market Cap and VG Score
        df2 = df.drop(df.index[[0, 1, 2]])
        df2 = df2.astype(float)
        # Divides dataframe by 100 to ensure that returns are percent change
        df2 = df2 / 100

        # print(f"Sector return: {sector_return} sector SD: {sector_std}")
        portfolio_return = portfolioreturn(df2, weights)
        # portfolio_cov = portfoliocovariance(df2, weights)
        portfolio_std = portfoliostd(df2, weights)
        sharpe_ratio = (portfolio_return-sector_return) / portfolio_std
        # sharpe_ratio = portfolio_return
        # print(f"Sharpe Ratio: {sharpe_ratio}")
        execution_sharpes = [sharpe_ratio, fund_names]
        # Use the highest sharpe ratio
        if sharpe_ratio > highest_sharpe:
            highest_sharpe = sharpe_ratio
            execution_to_check = execution_sharpes
            # sharpes.append(execution_sharpes)
        # if sharpe_ratio > 1:
        #     sharpes.append(execution_sharpes)
        #     print(len(sharpes))
    top_ten = sorted(sharpes, reverse=True, key=itemgetter(0))
    best_port = sorted(sharpes, reverse=True, key=itemgetter(0))[0]
    # print(remove_duplicates(top_ten))
    # print(best_port[1])
    isins = all_funds[best_port[1]]
    # isins = all_funds[execution_to_check]
    isins.to_csv('out.csv')
    print("Completed")


if __name__ == '__main__':
    main()
