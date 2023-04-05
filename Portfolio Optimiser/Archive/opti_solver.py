import numpy as np
import pandas as pd
import optimisation_lib as ol

df = pd.read_excel("Five Fund Returns.xlsx", sheet_name=0, skiprows=7, header=1, index_col=0, names=None)
df = df.dropna(subset=['ISIN'])

df = df.drop(df.columns[[0, 1, 2]], axis=1).astype(float)
df = df/100
sector = df.T.pop("IA UK All Companies")
df = df.drop("IA UK All Companies", axis=0)
# del df["IA UK All Companies"]
# del df.loc['IA UK All Companies']
df = df.T
# print(sector)
# print(dft)
# This point leaves us with a tidy dataframe with the sector taken out to be the 'standard'.
# The filename can be modified - UK All Companies Sector is the given input which is exported straight from Morningstar.
# print(dft)
# print(sector)
print(ol.sharpe_ratio(df, .003, 50))
print(ol.sharpe_ratio(sector, .003, 50))
