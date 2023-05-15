import pandas as pd
import openpyxl as xl
filename = r"X:\Fund Management\Fund Management Team Files\FM Personal Folders\Richard\PycharmProjects\Rebalancing" \
           r"\assets\FM Data for Rebalance 4 (Flat v2).xlsx"
class GetPositions:
    def __init__(self):
        self.positions_df = self._def_fund_positions_df()
        self.scheme_totals_df = self._def_scheme_totals()
        self.dilution_df = self._def_dilution_df()

    @staticmethod
    def _def_fund_positions_df():
        df = pd.read_excel(filename, sheet_name="PortfolioHoldings", engine='openpyxl')
        df = df[["Designation", "Account Name", "ISIN", "Description", "Base Market Value", "Asset Type"]]
        return df


    @staticmethod
    def _def_scheme_totals():
        df = pd.read_excel(filename, sheet_name="Scheme_Totals", engine='openpyxl')
        df.drop(index=df.index[:1], inplace=True)
        df["Fund Number"] = df["Fund Number"].astype(int)
        return df

    @staticmethod
    def _def_dilution_df():
        df = pd.read_excel(filename, sheet_name="Cashflows", engine='openpyxl',
                           dtype={'Designation': int, 'PortfolioName': str, 'CashFlow': float})
        df = df[["Designation", "PortfolioName", "CashFlow"]]
        return df

    def pid_positions(self, pID):
        return self.positions_df[self.positions_df["pID"] == pID]

    def designation_positions(self, designation):
        return self.positions_df[self.positions_df["Designation"] == designation]

    def designation_trend(self, designation):
        return self.scheme_totals_df[self.scheme_totals_df["Fund Number"] == designation]

    def get_nav(self, designation):
        return self.designation_trend(designation)['OEIC Net Assets'].values[0]

    def get_cashflow(self, **kwargs):
        if 'Designation' in kwargs:
            return self.dilution_df[self.dilution_df["Designation"] == kwargs['Designation']]["CashFlow"].values[0]
        elif 'PortfolioName' in kwargs:
            return self.dilution_df[self.dilution_df["PortfolioName"] == kwargs['PortfolioName']]["CashFlow"].values[0]


if __name__ == '__main__':
    positions = GetPositions()
    print(f"Positions using Designation: {positions.designation_positions(392125).to_string()}")
    print(f"Fund Trend using Designation: {positions.designation_trend(392125).to_string()}")
    print(f"Cashflow using Designation: {positions.get_cashflow(Designation=392125)}")
    print(f"Cashflow using PortfolioName: {positions.get_cashflow(PortfolioName='Providence Strategy')}")
