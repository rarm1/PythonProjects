import pandas as pd
class RRTargets:
    def __init__(self):
        xlsx = pd.ExcelFile(r"X:\Fund Management\Fund Management Team Files\FM Personal Folders\Richard\PycharmProjects\Rebalancing\assets\Risk Rated Targets Updated 15 05 2023.xlsx")

        # Define the column names you want to load
        columns_to_use = ['ISIN', 'Fund Name', 'Target', 'Holding Change', 'Investment Area', 'Dealing Method']

        # Create a dict of dataframes for each sheet, loading only the specified columns
        rr_targets = {sheet_name: pd.read_excel(xlsx, sheet_name=sheet_name, usecols=columns_to_use) for
                      sheet_name in xlsx.sheet_names}
        for sheet_name, df in rr_targets.items():
            rr_targets[sheet_name] = df.dropna(subset=['Fund Name'])
        prov_targets = rr_targets['Providence Targets']
        sel_targets = rr_targets['Select Targets']
        int_targets = rr_targets['International Targets']
        ven_targets = rr_targets['Venture Targets']
        self.pID_map = {1: prov_targets, 2: sel_targets, 3: int_targets, 4: ven_targets}

    def get_df_by_pid(self, pid):
        return self.pID_map[pid]


if __name__ == '__main__':
    rr_targs = RRTargets()
    # print(rr_targs.get_df_by_pid(1))
