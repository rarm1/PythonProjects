# TODO: This is going to be relatively temporary as I will eventually be getting the targets from Model Database.
import pandas as pd
import json
class Targets:
    def __init__(self, scheme, schemes_dict):
        with open(r"assets\config.json") as f:
            config = json.load(f)
        filenames = config["filenames"]
        # filenames = {
        # #     "Margetts": r"X:\Fund Management\Regulated Schemes\Risk Rated\Dealing and Rebalancing\Risk Rated Targets Updated 15 05 2023.xlsx",
        # #     "Prima": r"X:\Fund Management\Regulated Schemes\PRIMA\Rebalancers\Dealing Targets\PRIMA Targets 15 05 2023.xlsx",
        # #     "Clarion": r"X:\Fund Management\Regulated Schemes\Clarion\Rebalancing\Clarion Targets 15 05 2023.xlsx"
        # }
        filename = filenames.get(scheme)
        if filename is None:
            raise ValueError(f"No filename found for scheme {scheme}")

        columns_to_use = ['ISIN', 'Fund Name', 'Target', 'Holding Change', 'Investment Area', 'Dealing Method']
        portfolio_names = list(schemes_dict[scheme].keys())
        try:
            targets = pd.read_excel(filename, sheet_name=portfolio_names, usecols=columns_to_use)
        except FileNotFoundError:
            print(f"File {filename} not found.")
            return

        self.designation_map = {}
        for portfolio_name, designation in schemes_dict[scheme].items():
            self.designation_map[designation] = targets[portfolio_name]

    def get_df_by_designation(self, designation):
        return self.designation_map.get(designation)


if __name__ == '__main__':
    scheme_designation = {
        "Margetts": {"Providence": 392125, "Select": 392126, "International": 392124, "Venture": 392128},
        "Prima": {"Cautious": 253275, "Balanced": 253277, "Adventurous": 253278},
        "Clarion": {"Explorer": 397792, "Meridian": 397874, "Navigator": 253302, "Prudence": 397789},
        "IBOSS": {"1": 564536, "2": 564541, "4": 564542, "6": 564543},
        "Tempus": {"Universal": 444780}
    }
    rr_targs = Targets("Margetts", scheme_designation)
    print(rr_targs.get_df_by_designation(392125).to_string())
    prima_targs = Targets("Prima", scheme_designation)
    print(prima_targs.get_df_by_designation(253275).to_string())
