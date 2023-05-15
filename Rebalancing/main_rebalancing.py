import pandas as pd
import os
from Rebalancing.assets.targets import Targets
from Rebalancing.assets.get_positions import GetPositions
from Rebalancing.assets.pid_desig_get_set import PIDScheme
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
            "Margetts": {"Providence": 392125, "Select": 392126, "International": 392124, "Venture": 392128},
            "Prima": { "Cautious": 253275, "Balanced": 253277, "Adventurous": 253278},
            "Clarion": {"Explorer": 397792,"Meridian": 397874,"Navigator": 253302,"Prudence": 397789}
            # "IBOSS": { "1": 564536, "2": 564541, "4": 564542, "6": 564543},
            # "Tempus": {"Universal": 444780}
        }

asset_groups = {
    "Bonds": ["Bond", "Property", "Commodity", "Absolute Return"],
    "Equities": ["UK", "UK EQUITY INCOME", "ASIA PACIFIC", "EUROPE", "USA", "GLOBAL", "EMERGING MARKETS", "IA 20-60%", "IA 0-35%", "JAPAN"],
    "Cash/Money Markets": ["CASH/MONEY MARKETS"],
}


def main():
    positions = GetPositions()
    pid_scheme = PIDScheme()

    for range, dictionary in scheme_designation.items():
        targets = Targets(range, scheme_designation)
        os.makedirs(range, exist_ok=True)
        for scheme_name, designation in dictionary.items():
            print(scheme_name, designation)
            fund_positions = positions.designation_positions(designation)
            fund_targets = targets.get_df_by_designation(designation)
            # Margetts class doesn't make too much sense. I could just use the RRTargets class for all schemes.
            fund_cashflow = positions.get_cashflow(Designation=designation)
            fund_nav = positions.get_nav(designation) + fund_cashflow

            fund_positions = fund_positions.merge(fund_targets[['ISIN', 'Target', 'Investment Area']], on="ISIN", how="left")
            fund_positions.rename(columns={'Target': '% Target'}, inplace=True)

            fund_positions["% Holdings"] = fund_positions["Base Market Value"] / fund_nav
            fund_positions["% Fund Difference"] = fund_positions["% Holdings"] - fund_positions["% Target"]


            fund_positions['% Sector Target'] = fund_positions.groupby('Investment Area')['% Target'].transform('sum')
            fund_positions['% Sector Holding'] = fund_positions.groupby('Investment Area')['% Holdings'].transform('sum')
            fund_positions['% Sector Difference'] = fund_positions['% Sector Target'] - fund_positions['% Sector Holding']

            fund_positions['Bucket'] = fund_positions['Investment Area'].str.lower().map(
                lambda x: next((k for k, v in asset_groups.items() if x in [item.lower() for item in v]), None))

            fund_positions['% Bucket Target'] = fund_positions.groupby('Bucket')['% Target'].transform('sum')
            fund_positions['% Bucket Current'] = fund_positions.groupby('Bucket')['% Holdings'].transform('sum')
            fund_positions['% Bucket Difference'] = fund_positions['% Bucket Target'] - fund_positions['% Bucket Current']

            fund_positions['Fund Over/Under'] = fund_positions['% Fund Difference'].map(lambda x: "Over" if x > 0.01 else
            "Under" if x < -0.01 else "On Target")
            # I now need to find which Buckets and which Sectors are over/under target by over 50 basis points: 0.005
            fund_positions['Sector Over/Under'] = fund_positions['% Sector Difference'].map(lambda x: "Over" if x > 0.005 else
            "Under" if x < -0.005 else "On Target")
            fund_positions['Bucket Over/Under'] = fund_positions['% Bucket Difference'].map(lambda x: "Over" if x > 0.005 else
            "Under" if x < -0.005 else "On Target")

            print(fund_positions.to_string())

            print(rf"{range}\{scheme_name}.csv")
            fund_positions.to_csv(rf"{range}\{scheme_name}.csv", index=False)

    # prov_positions['Target Value'] = prov_positions['% Target'] * prov_nav
    # prov_positions['Fund Difference from Target'] = prov_positions['Target Value'] - prov_positions['BaseBidValue']


    # for _, pid_dict in schemes_dict.items():
    #     for scheme_name, pID in pid_dict.items():
    #         # compare_holdings(positions.pid_positions(pID), rr_targs.get_df_by_designation(pID), pid_scheme.get_df_by_designation(pID)
    #         print(scheme_name)
    #         print(positions.pid_positions(pID).to_string())
    #         print(rr_targs.get_df_by_designation(pID).to_string())
    #         # print("\n\n")

if __name__ == '__main__':
    main()
