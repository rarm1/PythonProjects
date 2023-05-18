import os
import pandas as pd
from Rebalancing.assets.pid_desig_get_set import PIDScheme

HEADERS = ["FMDealingCode", "TradeIdentifier", "TradeFileDate", "SchemeIdentifier", "SecurityName",
           "SecurityIdentifier", "NewSecurity", "Direction", "DealType", "Value",
           "SettlementCurrency", "PreviouslyReported", "Notes"]

TRADE_FILE_PATH = r"X:\Fund Management\Fund Management Team Files\FM Personal " \
                  r"Folders\Richard\PycharmProjects\Rebalancing\assets\trade_files"

class TradeWriter:
    def __init__(self, all_funds, pid_lookup=PIDScheme()):
        self.all_funds = all_funds
        self.pid_lookup = pid_lookup
        self.trade_sheet = pd.DataFrame(columns=HEADERS)
        self._create_trade_file()
        self.traded = self.identify_trades()
        self.populate_trade_sheet()

    def _create_trade_file(self):
        if not os.path.exists(TRADE_FILE_PATH):
            os.makedirs(TRADE_FILE_PATH)

    def identify_trades(self):
        return self.all_funds[self.all_funds["Traded"] == True].reset_index(drop=True)

    def populate_trade_sheet(self):
        # Populate fields of trade sheet
        self.trade_sheet["SecurityName"] = self.traded["Description"]
        self.trade_sheet["SecurityIdentifier"] = self.traded["ISIN"]
        self.trade_sheet["NewSecurity"] = self.traded["Initial Market Value"].apply(lambda x: "Y" if x == 0 else "N")
        self.trade_sheet["Direction"] = self.traded["Trade Amount"].apply(lambda x: "Buy" if x > 0 else "Sell")
        self._get_deal_type()
        self.trade_sheet["Value"] = round(abs(self.traded["Trade Amount"]), 2)
        self.trade_sheet["SettlementCurrency"] = "GBP"
        self.trade_sheet["PreviouslyReported"] = "N"
        self.trade_sheet["Notes"] = "Rebalancing"
        self.trade_sheet["FMDealingCode"] = "RICHARD"
        self.trade_sheet["TradeIdentifier"] = range(1, len(self.traded) + 1)
        self.trade_sheet["TradeFileDate"] = pd.to_datetime("today").strftime("%d/%m/%Y")
        self.trade_sheet["SchemeIdentifier"] = self.pid_lookup.get_pid(designation=self.traded["Designation"].values[0])
        # Check if the file already exists
        if os.path.isfile(os.path.join(TRADE_FILE_PATH, "manager_date.csv")):
            # If it does, open in append mode and don't write the header
            self.trade_sheet.to_csv(os.path.join(TRADE_FILE_PATH, "manager_date.csv"), mode='a', header=False, index=False)
        else:
            # If it doesn't exist, create a new one and write the header
            self.trade_sheet.to_csv(os.path.join(TRADE_FILE_PATH, "manager_date.csv"), index=False)
        print(f"{self.trade_sheet.to_string()}")

    def _get_deal_type(self):
        self.trade_sheet.loc[self.traded["% Holding"] == 0, "DealType"] = "SellAll"
        self.trade_sheet.loc[self.traded["Asset Type"] == "UCITS ETFs", "DealType"] = "UNIT"
        self.trade_sheet.loc[
            (self.traded["% Holding"] != 0) & (self.traded["Asset Type"] != "UCITS ETFs"), "DealType"] = "CASH"


if __name__ == '__main__':
    df = pd.read_csv(r"X:\Fund Management\Fund Management Team Files\FM Personal Folders\Richard\PycharmProjects\Rebalancing\assets\Output.csv")
    TradeWriter(df)
