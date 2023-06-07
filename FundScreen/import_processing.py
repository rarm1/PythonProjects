import sys
import chardet
import pandas as pd

from assets import file_id_reader


class ImportProcessing:
    def __init__(self, filetype: str = ".csv"):
        self.filetype = filetype
        self.df = None
        self.performance_dataframes = {}
        self.index_dataframes = {}
        self.na_dataframes = {}
        self.filename = self._get_filename()
        self._load_data()
        self.reader_df = self.df
        self._process_data()

    def _get_filename(self):
        all_files = file_id_reader.list_all_files(file_type=self.filetype)  # Get all files in directory
        print(all_files)
        if len(all_files) == 1:  # If only one file, return it
            return all_files[0]
        else:
            filename_user = file_id_reader.user_selected_file(all_files)  # If multiple files, ask user to select
            return file_id_reader.file_name_generator(filename_user)[0]

    def _load_data(self):  # Flexibility in filetype. Can be csv or xlsx
        if "csv" in self.filename:  # If csv, read csv
            rawdata = open(self.filename, 'rb').read()
            result = chardet.detect(rawdata)
            encoding = result['encoding']
            self.df = pd.read_csv(self.filename, encoding=encoding)
        elif "xlsx" in self.filename:  # If xlsx, read xlsx
            self.df = pd.read_excel(self.filename, sheet_name=0, index_col=None)

    def _process_data(self):
        self.df = self._clean_data(self.df)
        self.df, index_cols_found = self._clean_index_tracking(self.df)
        performance_datapoint_indexes, performance_datapoint_names = self._get_performance_datapoints()
        self.performance_dataframes = self._get_dataframes(self.df, performance_datapoint_indexes, performance_datapoint_names)
        if index_cols_found:
            self.performance_dataframes, self.index_dataframes = self._pop_index_funds(self.performance_dataframes)
        self.performance_dataframes, self.na_dataframe = self._remove_rows_with_too_many_nas(
            self.performance_dataframes)

    @staticmethod
    def _clean_data(df):
        df = df.iloc[7:, :].reset_index(drop=True)  # Remove first 7 rows (predictable format)
        df.columns = df.iloc[0, :].tolist()  # Set column names to first row
        df.dropna(subset=['ISIN'], inplace=True)  # Drop rows with no ISIN
        return df.iloc[1:, :].reset_index(drop=True)

    def _get_performance_datapoints(self):
        perf_datapoints = self.reader_df.iloc[5, :].dropna()  # Get performance datapoints
        performance_datapoint_indexes = [int(index.split(':')[1].strip()) for index in perf_datapoints.index]  # Get
        # indexes of performance datapoints presents as group/investment: up capture ratio. Split on colon, take second.
        performance_datapoint_names = perf_datapoints.values.tolist()  # Get names of performance datapoints
        return performance_datapoint_indexes, performance_datapoint_names

    @staticmethod
    def _get_dataframes(df, performance_datapoint_indexes, performance_datapoint_names):
        static_cols = df.iloc[:, :performance_datapoint_indexes[0]]  # Get static columns, before performance data.
        dataframes = {}
        if len(performance_datapoint_indexes) == 0:
            sys.exit("No performance datapoints found")  # Code has no purpose without performance datapoints.

        for idx, datapoint in enumerate(performance_datapoint_names):
            if idx == len(performance_datapoint_names) - 1:  # If last datapoint, take all columns after last index
                dataframes[datapoint] = df.iloc[:, performance_datapoint_indexes[idx]:]
            else:
                dataframes[datapoint] = df.iloc[:, performance_datapoint_indexes[idx]:performance_datapoint_indexes[
                idx + 1]]  # Take columns between indexes
        for idx, dataframe in enumerate(dataframes.keys()):
            dataframes[dataframe] = pd.concat([static_cols, dataframes[dataframe]], axis=1)  # Add static columns
        return dataframes

    @staticmethod
    def _remove_rows_with_too_many_nas(dataframes):
        # General function to remove rows with too many NA's. Made to take all indexes with too many NA's and remove
        # at once to maintain DF shape to enable processing later.
        too_many_na = {}
        all_indexes_to_drop = []
        for key, df in dataframes.items():
            thresh = len(df.columns) * 0.5  # Set threshold for NA's. Enables tweaking.
            all_indexes_to_drop.append(df[df.isna().sum(axis=1) > thresh].index.tolist())

        # flatten list of lists and remove duplicates
        all_indexes_to_drop = list(set([index for sublist in all_indexes_to_drop for index in sublist]))

        for key, df in dataframes.items():
            too_many_na[key] = df.loc[all_indexes_to_drop]  # Set rows with too many NA's
            dataframes[key].drop(too_many_na[key].index, inplace=True)  # Drop rows with too many NA's
            dataframes[key].reset_index(drop=True, inplace=True)  # Reset indexes
            too_many_na[key].reset_index(drop=True, inplace=True)  # Reset indexes

        return dataframes, too_many_na

    @staticmethod
    def _clean_index_tracking(df):
        index_cols_found = False  # Flag to check if index tracking columns are present
        try:
            df['Index Fund'] = df['Index Fund'].replace('Yes', True).replace('No', False)  # Set vars boolean
            df['Index Fund'] = df['Index Fund'].astype(bool)  # Define as boolean
            index_cols_found = True  # Set flag to True
        except KeyError:
            print("No Index Fund column found")
        try:
            df['Enhanced Index'] = df['Enhanced Index'].replace('Yes', True).replace('No', False)  # Set vars boolean
            df['Enhanced Index'] = df['Enhanced Index'].astype(bool)  # Define as boolean
            index_cols_found = True  # Set flag to True
        except KeyError:
            print("No Enhanced Index column found")
        return df, index_cols_found

    @staticmethod
    def _pop_index_funds(performance_dataframes):
        index_fund_dfs = {}
        condition_index, condition_enhanced = False, False  # Flags to check if index tracking columns are present
        condition1, condition2 = None, None  # Conditions for index funds
        for key, df in performance_dataframes.items():
            try:
                condition1 = (df['Index Fund'] == True)  # Set condition for index funds
                condition_index = True
            except KeyError:
                pass
            try:
                condition2 = (df['Enhanced Index'] == True)  # Set condition for enhanced index funds
                condition_enhanced = True
            except KeyError:
                pass
            if condition_index and condition_enhanced:  # If both columns present, use both conditions
                condition = condition1 | condition2
            elif condition_index:
                condition = condition1
            elif condition_enhanced:
                condition = condition2
            else:
                condition = None
            index_fund_df = df[condition]  # Set index fund DF based on conditions.
            df.drop(index_fund_df.index, inplace=True)  # Drop index fund rows from performance DF
            df.reset_index(drop=True, inplace=True)  # Reset indexes
            index_fund_dfs[key] = index_fund_df  # Add index fund DF to dict
        for key, df in index_fund_dfs.items():
            df.reset_index(drop=True, inplace=True)  # Reset indexes
        return performance_dataframes, index_fund_dfs

    @staticmethod
    def print_(to_print):
        if isinstance(to_print, pd.DataFrame):
            print(to_print.to_string())
        elif isinstance(to_print, dict):
            for key, df in to_print.items():
                print(key)
                print(df)
                print()
        else:
            print(to_print)

if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)
    pd.set_option('display.max_rows', None)

    import_processing = ImportProcessing(filetype=".xlsx")
