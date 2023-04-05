import pandas
import pandas as pd
import scipy as sc
import numpy as np
from scipy.stats import norm


def max_drawdown(return_series: pd.Series):
    """
    Takes a series of asset returns
    Computes and returns a Data Frame containing:
    the wealth index
    the previosu peaks
    percent max_drawdown
    """
    wealth_index = (1 + return_series).cumprod()
    previous_peaks = wealth_index.cummax()
    drawdowns = (wealth_index - previous_peaks) / previous_peaks
    return drawdowns.min()


def win_ratio(weekly_returns_list: list, sector_ret_list: list) -> float:
    wins = 0
    for idx, port_return in enumerate(weekly_returns_list):
        if port_return > 0.00 and port_return > sector_ret_list[idx]:
            wins += 1
        elif port_return < 0.00 and abs(port_return) < abs(sector_ret_list[idx]):
            wins += 1
    return wins / len(weekly_returns_list)


def capture_ratio(weekly_returns_list: list, sector_returns_list: list):
    positive_sector = [[i, sector_return] for i, sector_return in enumerate(
            sector_returns_list) if sector_return >= 00.00]
    positive_sector_indexes = [x[0] for x in positive_sector]
    positive_sector_list = [x[1] for x in positive_sector]
    negative_sector = [[i, sector_return] for i, sector_return in enumerate(
        sector_returns_list) if sector_return < 00.00]
    negative_sector_indexes = [x[0] for x in negative_sector]
    negative_sector_list = [x[1] for x in negative_sector]
    portfolio_pos_ret = [weekly_returns_list[i] for i in positive_sector_indexes]
    ucr = (sum(portfolio_pos_ret) / sum(positive_sector_list))
    portfolio_neg_ret = [weekly_returns_list[i] for i in negative_sector_indexes]
    dcr = (sum(portfolio_neg_ret) / sum(negative_sector_list))
    return ucr, dcr


def get_ffme_returns():
    """
    Load the Fama-French Dataset for the returns of the Top and Bottom Deciles by MarketCap
    """
    me_m = pd.read_csv("Portfolios_Formed_on_ME_monthly_EW.csv",
                       header=0, index_col=0, na_values=-99.99)
    rets = me_m[['Lo 10', 'Hi 10']]
    rets.columns = ['SmallCap', 'LargeCap']
    rets = rets / 100
    rets.index = pd.to_datetime(rets.index, format="%Y%m").to_period('M')
    return rets


def get_hfi_returns():
    """
    Load and format EDHEC Hedge Fund Index returns
    """
    hfi = pd.read_csv("edhec-hedgefundindices.csv",
                      header=0, index_col=0, parse_dates=True, na_values=-99.99)
    hfi = hfi / 100
    hfi.index = hfi.index.to_period('M')
    return hfi


# This is the kind of data that I am going to be working with.
def get_industry_returns():
    """
    Load and format Ken French 30 Industry Portfolios Value Weighted Monthly Returns
    """
    ind = pd.read_csv("ind30_m_vw_rets.csv", header=0, index_col=0, parse_dates=True) / 100  # Read returns CSV
    ind.index = pd.to_datetime(ind.index, format="%Y%M").to_period('M')  # Convert index with dates.
    ind.columns = ind.columns.str.strip()  # Remove unnecessary spaces, new chars at end of string.
    return ind


# R has a table of True or False. Because this is not used anywhere I don't know what it is given!
def semideviation(r):
    """
    Returns the semideviation of r. Must be a series or data frame
    """
    is_negative = r < 0
    # Give r a true or false arguement with delta degrees of freedom as 0. Divsor used in calculates is n - doff.
    return r[is_negative].std(ddof=0)


# Skewness is the deviation of the data from a normal distribution. Normally distributed data would have skew 0.
def skewness(r):
    """
    Alternative to scipy.stats.skew()
    Computes the skewness of the supplied Series or DataFrame
    Returns a float or a Series
    """
    demeaned_r = r - r.mean()
    # use the population stdev so set dof = 0
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r ** 3).mean()
    return exp / sigma_r ** 3


# Kurtosis is a measure of quantity of occurances greater differentiated from the mean (greater than 5 SDs from mean)
# Greater measure of kurtosis is indicative of very broadly distributed data.
def kurtosis(r):
    """
    Alternative to scipy.stats.kurt()
    Computes the kurtosis of the supplied Series or DataFrame
    Returns a float or a Series
    """
    demeaned_r = r - r.mean()
    # use the population stdev so set dof = 0
    sigma_r = r.std(ddof=0)
    exp = (demeaned_r ** 4).mean()
    return exp / sigma_r ** 4


# Test of goodness of fit. The closer to 0 the more extremely normally the data is distributed.
def is_normal(r, level=0.01):
    """
    Applies the Jarque-Bera test to determine if a Series is normal or not
    Test is applied at the 1% level by default
    Returns True if the Hypothesis of normalit is accepted, Fals otherwise
    """
    statistic, p_value = sc.stats.jarque_bera(r)
    return p_value > level


def var_historic(returns_df, level=5):
    """
    VaR Historic
    """
    if isinstance(returns_df, pd.DataFrame):
        """
        Check if this is a dataframe. If it is, call the function on every column of this dataframe.
        """
        return returns_df.aggregate(var_historic, level=level)
    elif isinstance(returns_df, pd.Series):
        return -np.percentile(returns_df, level)
    else:
        raise TypeError("Expected r to be series of dataframe")


# Value at risk is the acceptable chance of acceptable losses over a set timeframe.
def var_gaussian(returns_df, level=5, modified=False):
    """
    r
    Returns the Parametric Gaussian VaR of a Seriens or DataFrame.
    If "modified" is True, then the modified VaR is returned,
    using the Cornish-Fisher modification
    
    """
    # compute the Z score assuming it was Gaussian
    z = norm.ppf(level / 100)
    if modified:
        s = skewness(returns_df)
        k = kurtosis(returns_df)
        z = (z +
             (z ** 2 - 1) * s / 6 +
             (z ** 3 - 3 * z) * (k - 3) / 24 -
             (2 * z ** 3 - 5 * z) * (s ** 2) / 36
             )
    return -(returns_df.mean() + z * returns_df.std(ddof=0))


def cvar_historic(returns_df, level=5):
    """
    Computes the Conditional VaR of Series or DataFrame
    """
    if isinstance(returns_df, pd.Series):
        is_beyond = returns_df <= -var_historic(returns_df, level=level)
        return -returns_df[is_beyond].mean()
    elif isinstance(returns_df, pd.DataFrame):
        return returns_df.aggregate(cvar_historic, level=level)
    else:
        raise TypeError("Expected r to be a Series or DataFrame")


def annualise_rets(returns_df, periods_per_year) -> float:
    """
    Anualises returns.
    :param returns_df: pandas.DataFrame
        Dataframe containing returns
    :param periods_per_year: int
        Quantity of periods per year. IE weekly returns would take 52.
    :return: pandas.Dataframe
        Dataframe containing annualised returns from the year.
    """
    compounded_growth = (1 + returns_df).prod()
    n_periods = returns_df.shape[0]
    return compounded_growth ** (periods_per_year / n_periods) - 1


def annualise_vol(returns_df, periods_per_year) -> float:
    """
    Annualises the vol of a set of returns
    Should infer the periods per year as an improvement
    """
    return returns_df.std() * (periods_per_year ** 0.5)


def sharpe_ratio(returns_df: pandas.DataFrame, risk_free_rate: float = 0.01, periods_per_year: int = None):
    """
    Compute annualised sharpe ratio of a set of returns
    """
    # If amount of periods isn't given strictly, then it can use the shape of the dataframe to get this information.
    if periods_per_year is None:
        periods_per_year = returns_df.shape[0]
    rf_per_period = (1 + risk_free_rate) ** (1 / periods_per_year) - 1  # Convert the Rf rate to per period
    excess_ret = returns_df - rf_per_period
    ann_ex_ret = annualise_rets(excess_ret, periods_per_year)
    ann_vol = annualise_vol(returns_df, periods_per_year)
    return float(ann_ex_ret / ann_vol)


def portfolio_return(weights, returns):
    """
    Weights -> Returns
    """
    return weights.T @ returns


def portfolio_vol(weights, covmat):
    """
    weights->Vol
    """
    return (weights.T @ covmat @ weights) ** 0.5


def plot_ef2(n_points, er, cov):
    """
    Plot the 2-asset efficient frontier
    """
    if er.shape[0] != 2 or er.shape[0] != 2:
        raise ValueError("plot_ef2 can only plot 2 asset frontier")
    weights = [np.array([w, 1 - w]) for w in np.linspace(0, 1, n_points)]
    rets = [portfolio_return(w, er) for w in weights]
    vols = [portfolio_vol(w, cov) for w in weights]
    ef = pd.DataFrame({"R": rets, "Vol": vols})
    return ef.plot.line(x="Vol", y="R", style=".-")


def optimal_weights(n_points, er, cov):
    """
    Generates a list of weights to run the optimizer on
    """
    target_rs = np.linspace(er.min(), er.max(), n_points)
    weights = [minimize_vol(target_return, er, cov) for target_return in target_rs]
    return weights


def gmv(cov):
    """
    Returns the weights of the global minimum vol portfolio
    given covariance matrix    
    """
    n = cov.shape[0]
    return msr(0, np.repeat(1, n), cov)


def plot_ef(n_points, er, cov, show_cml=False, style='.-', rf=0, show_ew=False, show_gmv=False):
    """
    Plot the multi-asset efficient frontier
    :param n_points:
    :param er:
    :param cov:
    :param show_cml:
    :param style:
    :param rf:
    :param show_ew:
    :param show_gmv:
    :return:
    """
    weights = optimal_weights(n_points, er, cov)
    rets = [portfolio_return(w, er) for w in weights]
    vols = [portfolio_vol(w, cov) for w in weights]
    ef = pd.DataFrame({"Returns": rets, "Volatility": vols})
    ax = ef.plot.line(x="Volatility", y="Returns", style=style)

    if show_gmv:
        n = er.shape[0]
        w_gmv = gmv(cov)
        r_gmv = portfolio_return(w_gmv, er)
        vol_gmv = portfolio_vol(w_gmv, cov)
        # display GMV
        ax.plot([vol_gmv], [r_gmv], color="midnightblue", marker="o", markersize=12)

    if show_ew:
        n = er.shape[0]
        w_ew = np.repeat(1 / n, n)
        r_ew = portfolio_return(w_ew, er)
        vol_ew = portfolio_vol(w_ew, cov)
        # display EW
        ax.plot([vol_ew], [r_ew], color="goldenrod", marker="o", markersize=12)

    if show_cml:
        ax.set_xlim(left=0)
        rf = 0.1
        w_msr = msr(rf, er, cov)
        r_msr = portfolio_return(w_msr, er)
        vol_msr = portfolio_vol(w_msr, cov)
        # Add CML
        cml_x = [0, vol_msr]
        cml_y = [rf, r_msr]
        ax.plot(cml_x, cml_y, color="green", marker="o", linestyle="dashed", markersize=12, linewidth=2)

    return ax


# FIXME: This function doesn't work.
# def target_is_met(w, er):
#     return target_return - erk.portfolio_return(w, er)


def minimize_vol(target_return, er, cov):
    """
    target_return -> W
    """
    n = er.shape[0]
    init_guess = np.repeat(1 / n, n)
    bounds = ((0.0, 1.0),) * n
    return_is_target = {
        'type': 'eq',
        'args': (er,),
        'fun': lambda weights, er: target_return - portfolio_return(weights, er)
    }
    weights_sum_to_1 = {
        'type': 'eq',
        'fun': lambda weights: np.sum(weights) - 1
    }
    results = sc.optimize.minimize(portfolio_vol, init_guess,
                                   args=(cov,), method="SLSQP",
                                   options={'disp': False},
                                   constraints=(return_is_target, weights_sum_to_1),
                                   bounds=bounds
                                   )
    return results.x


def msr(rf, er, cov):
    """
    RiskFree + er + cov -> max sharpe
    """
    n = er.shape[0]
    init_guess = np.repeat(1 / n, n)
    bounds = ((0.0, 1.0),) * n
    weights_sum_to_1 = {
        'type': 'eq',
        'fun': lambda weights: np.sum(weights) - 1}

    def neg_sharpe_ratio(weights, rf, er, cov):
        """
        Returns the negative of the sharpe ratio, given weights
        """
        r = portfolio_return(weights, er)
        vol = portfolio_vol(weights, cov)
        return ((r - rf) / vol) *-1

    results = sc.optimize.minimize(neg_sharpe_ratio, init_guess,
                                   args=(rf, er, cov,), method="SLSQP",
                                   options={'disp': False},
                                   constraints=(weights_sum_to_1),
                                   bounds=bounds
                                   )
    return results.x
