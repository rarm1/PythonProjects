import pandas as pd
class Targets:
    def __init__(self, scheme, schemes_dict):
        # PRIMA portfolio names are Cautious, Balanced and adventurous
        rr_filename = r"X:\Fund Management\Regulated Schemes\Risk Rated\Dealing and Rebalancing\Risk Rated Targets Updated 15 05 2023.xlsx"
        prima_filename = r"X:\Fund Management\Regulated Schemes\PRIMA\Rebalancers\Dealing Targets\PRIMA Targets 15 05 2023.xlsx"
        clarion_filename = r"X:\Fund Management\Regulated Schemes\Clarion\Rebalancing\Clarion Targets 15 05 2023.xlsx"
        if scheme == "Margetts":
            filename = pd.ExcelFile(rr_filename)
        elif scheme == "Prima":
            filename = pd.ExcelFile(prima_filename)
        elif scheme == "Clarion":
            filename = pd.ExcelFile(clarion_filename)

        columns_to_use = ['ISIN', 'Fund Name', 'Target', 'Holding Change', 'Investment Area', 'Dealing Method']
        portfolio_names = list(schemes_dict[scheme].keys())
        targets = pd.read_excel(filename, sheet_name=portfolio_names, usecols=columns_to_use)
        if scheme == "Margetts":
            prov_targets = targets['Providence']
            sel_targets = targets['Select']
            int_targets = targets['International']
            ven_targets = targets['Venture']
            self.designation_map = {392125: prov_targets, 392126: sel_targets, 392124: int_targets, 392128: ven_targets}
        elif scheme == "Prima":
            cautious_targets = targets['Cautious']
            balanced_targets = targets['Balanced']
            adventurous_targets = targets['Adventurous']
            self.designation_map = {253275: cautious_targets, 253277: balanced_targets, 253278: adventurous_targets}
        elif scheme == "Clarion":
            prudence_targets = targets['Prudence']
            meridian_targets = targets['Meridian']
            explorer_targets = targets['Explorer']
            navigator_targets = targets['Navigator']
            self.designation_map = {397789: prudence_targets, 397874: meridian_targets, 397792: explorer_targets, 253302: navigator_targets}


    def get_df_by_designation(self, designation):
        return self.designation_map[designation]


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
