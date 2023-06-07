import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.max_rows', None)
file_locations = [
    r"X:\Fund Management\Regulated Schemes\Aequitas\Dealing and Targets\Aequitas Targets Horizon Positions.xlsx",
    r"X:\Fund Management\Regulated Schemes\Tempus\Dealing\Rebalancing\Tempus 07 06 2023 Targets Horizion "
    r"Positions.xlsx",
    r"X:\Fund Management\Regulated Schemes\Risk Rated\Dealing and Rebalancing\Risk Rated Targets Horizon "
    r"Positions.xlsx",
    r"X:\Fund Management\Regulated Schemes\PRIMA\Rebalancers\Dealing Targets\PRIMA Targets 07 06 2023 v1.3 Horizon "
    r"Details.xlsx",
    r"X:\Fund Management\Regulated Schemes\IBOSS\Dealing\Rebalancer sheets Excel and Templates\IBOSS Targets updated "
    r"15 05 2023 Horizon Positions.xlsx",
    r"X:\Fund Management\Regulated Schemes\Clarion\Rebalancing\Clarion Targets 15 05 2023 Horizon Positions.xlsx"
]

funds = []
for file in file_locations:
    df = pd.read_excel(file, sheet_name=None, index_col=None)
    for sheet in df.keys():
        df[sheet]['Sheet Name'] = sheet  # Add 'Sheet Name' column
        funds.append(df[sheet])

# Concatenate all dataframes in the list
fund_df = pd.concat(funds, ignore_index=True)

# Convert to lower case before grouping
fund_df_unique = fund_df.copy()
fund_df_unique['Fund Name'] = fund_df_unique['Fund Name'].str.lower()
fund_df_unique['Investment Area'] = fund_df_unique['Investment Area'].str.lower()
fund_df_unique['Horizon Investment Area'] = fund_df_unique['Horizon Investment Area'].str.lower()
fund_df_unique['Horizon Asset Class Name'] = fund_df_unique['Horizon Asset Class Name'].str.lower()

# Now apply groupby
fund_df_unique = fund_df_unique.groupby(['Fund Name', 'Investment Area', 'Horizon Investment Area', 'Horizon Asset Class Name'])['Sheet Name'].apply(', '.join).reset_index()

# You can then convert the first letter of each word to uppercase if required
fund_df_unique['Fund Name'] = fund_df_unique['Fund Name'].str.title()
fund_df_unique['Investment Area'] = fund_df_unique['Investment Area'].str.title()
fund_df_unique['Horizon Investment Area'] = fund_df_unique['Horizon Investment Area'].str.title()
fund_df_unique['Horizon Asset Class Name'] = fund_df_unique['Horizon Asset Class Name'].str.title()

# Sort the dataframe by 'Fund Name'
fund_df_unique = fund_df_unique.sort_values(by='Fund Name')


# Write the dataframe to excel
fund_df_unique.to_excel("unique_funds.xlsx", index=False)
