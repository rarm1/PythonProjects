
# sectors = {
#     "BOND": ["UK Gilts", "UK Index Linked Gilts", "Sterling Corporate Bond", "Sterling Strategic Bond", "Sterling High Yield",
#              "USD Government Bond", "EUR Government Bond", "Global Government Bond", "Global Inflation Linked Bond",
#              "USD Corporate Bond", "EUR Corporate Bond", "Global Corporate Bond", "USD Mixed Bond", "EUR Mixed Bond",
#              "Global Mixed Bond", "USD High Yield Bond", "EUR High Yield Bond", "Global High Yield Bond",
#              "Global Emerging Markets Bond - Hard Currency", "Global Emerging Markets Bond - Local Currency",
#              "Global Emerging Markets Bond - Blended", "Specialist Bond", "Global Bonds", "Global Emerging Markets Bond",
#              "£ Corporate Bond", " GBP Government Bond", "GBP High Yield Bond",
#              "GBP Government Bond", "£ Strategic Bond", "GBP Government Bond", "UK INDEX LINKED BONDS",
#              "GLOBAL CORPORATE BONDS", "GLOBAL FLEXIBLE BOND-GBP HEDGED"],
#     "PROPERTY": ["UK Direct Property", "Property Other", "UK Property", "Property Other Sector", "Property",
#                  "PROPERTY - DIRECT UK"],
#     "COMMODITY": ["Commodities and Natural Resources"],
#     "ABSOLUTE RETURN": ["Targeted Absolute Return", "Target Absolute Return - Bonds"],
#     "UK": ["UK All Companies", "UK Smaller Companies"],
#     "UK EQUITY INCOME": ["UK Equity Income"],
#     "ASIA PACIFIC": ["Asia Pacific excluding Japan", "China/Greater China"],
#     "EUROPE": ["Europe including UK", "Europe excluding UK", "European Smaller Companies"],
#     "USA": ["North America", "North American Smaller Companies"],
#     "GLOBAL": ["Global", "SECTOR EQUITY INFRASTRUCTURE", "GLOBAL EQUITY INCOME"],
#     "EMERGING MARKETS": ["Global Emerging Markets", "India/Indian Subcontinent"],
#     "IA MIXED INVESTMENT": ["IA Mixed Investment 0-35% Shares", "IA Mixed Investment 20-60% Shares", "IA Mixed Investment 40-85% Shares"],
#     "JAPAN": ["Japan", "Japanese Smaller Companies"],
#     "CASH/MONEY MARKETS": ["Short Term Money Market", "Standard Money Market", "Money Market", "Money Markets"],
# }


# print(rr_targs.prov_targets.to_string())
# holdings_df = pd.read_excel(r"X:\Fund Management\Fund Management Team Files\FM Personal "
#                             r"Folders\Richard\PycharmProjects\Rebalancing\Horizon Positions.xlsm",
#                             sheet_name="Horizon Positions", skiprows=2, engine='openpyxl')
# holdings_df = holdings_df[["Designation", "pID", "PortfolioName", "ISIN", "SecurityNameShort", "BaseMidValue",
#                            "Sector", "AssetTypeID"]]
# holdings_df['Sector'] = holdings_df['Sector'].str.upper()
# # Reverse the dictionary to map from subsector to main sector
# reverse_sectors = {sub.upper(): main for main, sub_list in sectors.items() for sub in sub_list}
#
# # Replace the 'Sector' column
# holdings_df['SectorFound'] = holdings_df['Sector'].map(reverse_sectors).notna()
# holdings_df['Sector'] = holdings_df['Sector'].map(reverse_sectors).fillna(holdings_df['Sector'])
# # df['Sector'] = df['Sector'].map(reverse_sectors).fillna(df['Sector'])
#
# for scheme in schemes_dict:
#     for pID in schemes_dict[scheme]:
#         to_print = holdings_df.loc[(holdings_df["pID"] == pID)]
#         if not to_print.empty:
#             # print(f"\n{scheme} - {pID}")
#             print(to_print.loc[to_print["SectorFound"] == False].to_string())

# print(scheme)
# for designation in designations:
#     print(holdings_df.loc[(holdings_df["Designation"] == designation)])