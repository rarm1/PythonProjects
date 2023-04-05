# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 08:30:44 2022

@author: DKon1
"""
from timeit import timeit
import pandas as pd
import scipy as sc
import numpy as np
from numpy import ndarray
from scipy.stats import norm
import optimisation_lib as edhec

# Globals
RFR = 0.01
DF = pd.read_excel("Optimiser Data 9 Funds.xlsx", sheet_name='Sheet1', header=0, index_col=0)
GV_SCORES = DF.iloc[0]
DF.drop(DF.index[[0]], inplace=True, axis=0)
DF.dropna(axis=1, how='any', inplace=True)
DF = DF.astype(float)  # Cast to floats.
DF = DF / 100  # Change to percentage returns


def get_metrics(weights):
    port_ret = edhec.portfolio_return(weights, edhec.annualise_rets(DF, 52))
    port_vol = edhec.portfolio_vol(weights, DF.cov())
    return port_ret / port_vol


def port_sharpe(weightings):
    return get_metrics(weightings) * -1  # Because scipy only minimises what we're optimising.


# TODO: Add weighted growth value score in here. Let THIS be the marker for whether gv is reached, not another function.
def tolerance_calc(weightings) -> bool:
    weighted_gv_scores = [GV_SCORES.iloc[idx] * weight for idx, weight in enumerate(weightings) if  # Create array
                          # of weighted growth value scores
                          weight > 0.01]  # if the weighting is greater than 1%, do we want it otherwise?
    if np.sum(weighted_gv_scores) == 217.40:
        return True
    else:
        return False
    # '''
    # if weightings * gv scores within tolerance
    # return True
    # else:
    # return false
    # :param weightings:
    # :return:
    # '''
    # pass


def weightings_contraint(weightings):
    gv_within_tolerance = tolerance_calc(weightings)
    if (np.sum(weightings) - 1) == 0 and gv_within_tolerance:
        print("Within success condition")
        return 0.0  # What equality functions target is 0. Therefore, 0 is the success in this case. It is not bitwise
        # as I thought initially.
    else:
        # print(np.sum(weightings) - 1)
        return np.sum(weightings) - 1


def growth_value_contraint(weightings):
    print(GV_SCORES)
    weighted_gv_scores = [GV_SCORES.iloc[idx] * weight for idx, weight in enumerate(weightings) if  # Create array
                          # of weighted growth value scores
                          weight > 0.01]  # if the weighting is greater than 1%, do we want it otherwise?
    if 175 > np.sum(weighted_gv_scores) > 100:  # if the sum of weighted growth value scores is within tolerance, davai.
        # print(np.sum(weighted_gv_scores))
        return 0.0
    else:
        # print(np.sum(weighted_gv_scores))
        return np.sum(weighted_gv_scores) - 150


def optimise():
    # TODO: So do I need to generate a model for weighted GV scores? What would that look like?
    # target_approximate_gv = 150
    first_weights = np.array(np.repeat(1 / DF.shape[1], DF.shape[1]))
    # first_gvs = np.array(np.repeat(150 / DF.shape[1], DF.shape[1]))
    lb, ub = ([0.0, 1])
    bnds = tuple([(lb, ub) for _ in np.repeat(1 / DF.shape[1], DF.shape[1])])
    weight_cons = {'type': 'eq', 'fun': weightings_contraint}
    # gv_cons = {'type': 'eq', 'fun': growth_value_contraint}
    # cons = [weight_cons, gv_cons]
    print("Process for Weights")
    results = sc.optimize.minimize(port_sharpe,
                                   first_weights,  # If testing for weights
                                   # first_gvs,  # if testing for GVS
                                   method="SLSQP",
                                   bounds=bnds,
                                   # constraints=gv_cons,
                                   constraints=weight_cons
                                   )
    print(results)
    weights = results.x
    print("~"*50)
    # print("Process for Growth Values")
    # results = sc.optimize.minimize(get_metrics,
    #                                # first_weights,  # If testing for weights
    #                                first_gvs,  # if testing for GVS
    #                                method="SLSQP",
    #                                args=weights,
    #                                bounds=bnds,
    #                                constraints=gv_cons,
    #                                # constraints=weight_cons
    #                                )
    # print(results)
    return results.x


optimised_weights = optimise()
# optimised_weights_index = [[weighting, df.columns[index]] for index, weighting in enumerate(
#     optimised_weights)]
# print(sorted(optimised_weights_index, reverse=True))
# print([print(value) for value in sorted(optimised_weights_index, reverse=True)])
# [print(str(round(weight, 2)*100) + "%") for weight in optimised_weights if weight > 0]
# port_ret = edhec.portfolio_return(optimised_weights, ann_rets)
# port_vol = edhec.portfolio_vol(optimised_weights, covmat)
# print(f"Sharpe Ratio: {port_ret / port_vol}")


# Explanation of output.
# fun: Value of the objective function
# jac: Jacobian value of objective function
# message: Exit message.
# nfev: Number of evalations of the objective function
# nit: Number of iterations performed by optimiser
# njev: number of it's Jacobian evaluations
# status: exit code. https://github.com/scipy/scipy/blob/main/scipy/optimize/slsqp/slsqp_optmz.f#L117 - line 115.
# success: boolean: Whether exec was a success
# x:   solution of the optimisation
