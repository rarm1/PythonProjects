import pandas as pd
from Rebalancing.assets.rr_targets import RRTargets
from Rebalancing.assets.get_positions import GetPositions
from Rebalancing.assets.pid_desig_get_set import PIDScheme
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.max_rows', None)
pd.options.display.float_format = '{:.4f}'.format

schemes_dict = {
    "Margetts": {"Providence": 1,
        "Select": 2,
        "International": 3,
        "Venture": 4}
    # "Prima": [169, 171, 172],
    # "Clarion": [69, 70, 71, 177],
    # "IBOSS": [123, 125, 126, 127],
    # "Tempus": [195]
}

# Equities are as follows:
# UK
# UK EQUITY INCOME
# ASIA PACIFIC
# EUROPE
# USA
# GLOBAL
# EMERGING MARKETS
# IA 20-60%
# IA 0-35%
# JAPAN

asset_groups = {
    "Bonds": ["Bond", "Property", "Commodity", "Absolute Return"],
    "Equities": ["UK", "UK EQUITY INCOME", "ASIA PACIFIC", "EUROPE", "USA", "GLOBAL", "EMERGING MARKETS", "IA 20-60%", "IA 0-35%", "JAPAN"],
}

def compare_holdings(df_positions, df_targets, designation):

    pass


# I could bring all targets documents into one dataframe, then filter by designation/pID
def main():
    positions = GetPositions()
    rr_targs = RRTargets()
    pid_scheme = PIDScheme()

    # Get individual PIDs from the schemes_dict
    for scheme, pids in schemes_dict.items():
        for pid in pids.values():
            designation = pid_scheme.get_designation(pid=pid)
            fund_positions = positions.pid_positions(pid)
            fund_targets = rr_targs.get_df_by_pid(pid)
            fund_cashflow = positions.get_cashflow(Designation=designation)
            fund_nav = positions.get_nav(designation) + fund_cashflow

            fund_positions = fund_positions.merge(fund_targets[['ISIN', 'Target', 'Investment Area']], on="ISIN", how="left")
            fund_positions.rename(columns={'Target': '% Target'}, inplace=True)

            fund_positions["% Holdings"] = fund_positions["BaseBidValue"] / fund_nav
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


            fund_positions.to_csv(f"{pid_scheme.get_name(pid)}.csv", index=False)

    # prov_positions['Target Value'] = prov_positions['% Target'] * prov_nav
    # prov_positions['Fund Difference from Target'] = prov_positions['Target Value'] - prov_positions['BaseBidValue']


    # for _, pid_dict in schemes_dict.items():
    #     for scheme_name, pID in pid_dict.items():
    #         # compare_holdings(positions.pid_positions(pID), rr_targs.get_df_by_pid(pID), pid_scheme.get_df_by_pid(pID)
    #         print(scheme_name)
    #         print(positions.pid_positions(pID).to_string())
    #         print(rr_targs.get_df_by_pid(pID).to_string())
    #         # print("\n\n")

if __name__ == '__main__':
    main()
