import pandas as pd
import os
from Rebalancing.assets.targets import Targets
from Rebalancing.assets.get_positions import GetPositions
from Rebalancing.assets.trading_algo import TradingAlgo

pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:.4f}'.format

schemes_dict = {
    "Margetts": [1, 2, 3, 4],
    "Prima": [169, 171, 172],
    "Clarion": [69, 70, 71, 177]
    # "IBOSS": [123, 125, 126, 127],
    # "Tempus": [195]
}

scheme_designation = {
            # "Margetts": {"Providence": 392125, "Select": 392126, "International": 392124, "Venture": 392128},
            # "Prima": { "Cautious": 253275, "Balanced": 253277, "Adventurous": 253278},
            "Clarion": {"Explorer": 397792,"Meridian": 397874,"Navigator": 253302,"Prudence": 397789}
            # "IBOSS": { "IBOSS 1": 564536, "IBOSS 2": 564541, "IBOSS 4": 564542, "IBOSS 6": 564543},
            # "Tempus": {"Tempus Universal": 444780}
        }

asset_groups = {
    "Bonds": ["Bond", "Property", "Commodity", "Absolute Return"],
    "Equities": ["UK", "UK EQUITY INCOME", "ASIA PACIFIC", "EUROPE", "USA", "GLOBAL", "EMERGING MARKETS", "IA 20-60%", "IA 0-35%", "JAPAN"],
    "Cash/Money Markets": ["CASH/MONEY MARKETS"],
}




def main():
    positions = GetPositions()

    for manager, dictionary in scheme_designation.items():
        targets = Targets(manager, scheme_designation)
        os.makedirs(manager, exist_ok=True)
        for scheme_name, designation in dictionary.items():
            print(scheme_name, designation)
            fund_positions = positions.designation_positions(designation)
            fund_targets = targets.get_df_by_designation(designation)
            fund_cashflow = positions.get_cashflow(Designation=designation)
            fund_nav = positions.get_nav(designation) + fund_cashflow

            fund_positions = fund_positions.merge(fund_targets[['ISIN', 'Target', 'Investment Area']], on="ISIN", how="left")
            fund_positions.rename(columns={'Target': '% Target'}, inplace=True)


            # if any of the above are not on target, initialise the trading class
            # if fund_positions['Fund Over/Under'].any() != "On Target" or fund_positions['Sector Over/Under'].any() != "On Target" or fund_positions['Bucket Over/Under'].any() != "On Target":
            trading_algo = TradingAlgo(fund_positions, fund_nav)


            # trade_funds(fund_positions, fund_nav)

            # print(fund_positions.to_string())
            #
            # print(rf"{manager}\{scheme_name}.csv")
            fund_positions.to_csv(rf"{manager}\{scheme_name}.csv", index=False)


if __name__ == '__main__':
    main()
