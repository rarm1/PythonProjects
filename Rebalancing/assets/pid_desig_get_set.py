import pandas as pd
class PIDScheme:
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        df = pd.read_excel(r"X:\Fund Management\Fund Management Team Files\FM Personal "
                           r"Folders\Richard\PycharmProjects\Rebalancing\assets\scheme_list_desig.xlsm",
                           sheet_name="Source", engine='openpyxl', skiprows=2)
        df.columns = df.iloc[0]
        df.drop(index=df.index[:1], inplace=True)
        self.df = df[["pID", "PortfolioLongName", "Designation"]]

    def get_designation(self, pid):
        return int(self.df[self.df["pID"] == pid]["Designation"].values[0])

    def get_name(self, pid):
        return self.df[self.df["pID"] == pid]["PortfolioLongName"].values[0]

    def get_pid(self, designation):
        df = self.df[self.df["Designation"].notna()].copy()

        return df[df['Designation'].dropna().astype(int) == designation.astype(int)]["pID"].values[0]


if __name__ == '__main__':
    pid_scheme = PIDScheme()

    print(pid_scheme.get_designation(pid=1))
    print(pid_scheme.get_name(pid=1))
