# # TODO: Best way to link fund group to specific strategies. Dictionary with fund group as key and list of strategies as value?
import pandas as pd
from Rebalancing.assets.rr_targets import RRTargets
from Rebalancing.assets.get_positions import GetPositions
from Rebalancing.assets.pid_design_get_set import PIDScheme
pd.set_option('display.max_columns', 50)
pd.set_option('display.max_colwidth', 100)
pd.set_option('display.max_rows', None)

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


def compare_holdings(df_positions, df_targets, designation):

    pass


def main():
    positions = GetPositions()
    rr_targs = RRTargets()
    pid_scheme = PIDScheme()
    for _, pid_dict in schemes_dict.items():
        for scheme_name, pID in pid_dict.items():
            # compare_holdings(positions.pid_positions(pID), rr_targs.get_df_by_pid(pID), pid_scheme.get_df_by_pid(pID)
            print(scheme_name)
            print(positions.pid_positions(pID).to_string())
            print(rr_targs.get_df_by_pid(pID).to_string())
            # print("\n\n")

if __name__ == '__main__':
    main()
