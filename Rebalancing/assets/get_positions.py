import pandas as pd
filename = r"X:\Fund Management\Fund Management Team Files\FM Personal " \
           r"Folders\Richard\PycharmProjects\Rebalancing\assets\Horizon Positions.xlsm"
class GetPositions:
    def __init__(self):
        self.positions_df = self._def_fund_positions_df()
        self.fund_trend_df = self._def_fund_trend_df()

    @staticmethod
    def _def_fund_positions_df():
        df = pd.read_excel(filename, sheet_name="Horizon Positions", skiprows=2, engine='openpyxl')
        df = df[["Designation", "pID", "PortfolioName", "ISIN", "SecurityNameShort",
                                          "BaseMidValue", "AssetTypeID"]]
        return df

    @staticmethod
    def _def_fund_trend_df():
        df = pd.read_excel(filename, sheet_name="Fund Trend", skiprows=8, engine='openpyxl')
        df.columns = df.iloc[0]
        df.drop(index=df.index[:1], inplace=True)
        return df

    def pid_positions(self, pID):
        return self.positions_df[self.positions_df["pID"] == pID]

    def designation_trend(self, designation):
        return self.fund_trend_df[self.fund_trend_df["Account Number"] == designation]


if __name__ == '__main__':
    positions = GetPositions()
    print(positions.pid_positions(1).to_string())
    print(positions.designation_trend("392125")['Net Assets'].values[0])
