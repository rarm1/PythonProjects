# TODO: How about scoring each fund by its sharpe ratio. Lose the bottom half of performers. Then try combining funds
#   By maximising (minimising?) the sharpe ratio.
import numpy as np
import pandas as pd
import math
import timeit

def compare_one(df):
    excluded = []
    fund_cumulative_return = []
    for col in df.columns:
        quant_nan = 0
        cumulative = 1.00
        for ret in df[col][3:]:
            if math.isnan(ret):
                quant_nan += 1
                ret = 0.00
            if np.isnan(ret):
                ret = 0.00
            cumulative *= 1.00 + (ret / float(100))
        if len(df[col][3:]) / 4 < quant_nan:
            excluded.append(col)
            continue
        fund_cumulative_return.append([col, cumulative])


def compare_two(df):
    for col in df.columns:
        print(df[col][3:].isnull().sum())


def find_include_and_exclude(df):
    excluded = []
    fund_cumulative_return = []
    for col in df.columns:
        quant_nan = 0
        cumulative = 1.00
        print(df[col][3:].isnull().sum())
        for ret in df[col][3:]:
            if math.isnan(ret):
                quant_nan += 1
                ret = 0.00
            if np.isnan(ret):
                ret = 0.00
            cumulative *= 1.00 + (ret / float(100))
        if len(df[col][3:]) / 4 < quant_nan:
            excluded.append(col)
            continue
        fund_cumulative_return.append([col, cumulative])
    return df.drop(excluded, axis=1), fund_cumulative_return


def organise_dataframes(included, df):
    headers = []
    to_append = []
    [headers.append(included[i][0]) for i in range(len(included))]
    [to_append.append(included[i][1]) for i in range(len(included))]
    to_append = pd.DataFrame(to_append, index=headers, columns=['Cumulative Return']).T
    return pd.concat([df, to_append], axis=0, ignore_index=False)


def filter_funds_gv_score(df, gv_quantiles):
    dv_dict, v_dict, b_dict, g_dict, hg_dict = {}, {}, {}, {}, {}
    for fund in df:
        if df[fund]['VG Score'] < gv_quantiles[0]:
            dv_dict[fund] = df[fund]['Cumulative Return']
        elif gv_quantiles[0] < df[fund]['VG Score'] < gv_quantiles[1]:
            v_dict[fund] = df[fund]['Cumulative Return']
        elif gv_quantiles[1] < df[fund]['VG Score'] < gv_quantiles[2]:
            b_dict[fund] = df[fund]['Cumulative Return']
        elif gv_quantiles[2] < df[fund]['VG Score'] < gv_quantiles[3]:
            g_dict[fund] = df[fund]['Cumulative Return']
        elif gv_quantiles[3] < df[fund]['VG Score']:
            hg_dict[fund] = df[fund]['Cumulative Return']

    def dictionary_filter(dict_in: dict) -> list:
        dv_mean = np.mean([dict_in[i] for i in dict_in])
        to_return = [i for i in dict_in if dict_in[i] < dv_mean]
        return to_return

    dv_dict = dictionary_filter(dv_dict)
    v_dict = dictionary_filter(v_dict)
    b_dict = dictionary_filter(b_dict)
    g_dict = dictionary_filter(g_dict)
    hg_dict = dictionary_filter(hg_dict)
    nested = [dv_dict, v_dict, b_dict, g_dict, hg_dict]

    def filter_by_sharpe(nested):
        funds_with_sharpe = []
        for classification in nested:
            for idx, fund in enumerate(classification):
                classification[idx] = [fund, (df[fund][-1]/df[fund][3:-1].std())]
            average_std = np.mean([i[1] for i in classification])
            print(average_std)
    filter_by_sharpe(nested)
    for classification in nested:
        for fund in classification:
            df.pop(fund[0])
    return df


def main():
    data_frame = pd.read_excel("Correlation Data One.xlsx", skiprows=8, index_col=0, header=0, sheet_name="Sheet1").T
    data_frame = data_frame.dropna(subset=["VG Score"], inplace=False, axis=1)
    df, fund_cumulative_return = find_include_and_exclude(data_frame)
    sector = df.pop('IA UK All Companies')
    df = organise_dataframes(fund_cumulative_return, df)
    gv_quantiles = list(df.iloc[2].quantile([.2, .4, .6, .8]))
    df = filter_funds_gv_score(df, gv_quantiles)


if __name__ == '__main__':
    main()
