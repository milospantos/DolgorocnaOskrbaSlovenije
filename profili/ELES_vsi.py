import pandas as pd
import numpy as np
import os
from calendar import isleap

PATH=os.path.abspath(os.getcwd())
datoteka = "ELES_vse_2024_1.csv"
podatki = pd.read_csv(PATH +"\\"+ datoteka)


datoteka2 = "ELES_vse_2024_2.csv"
podatki2 = pd.read_csv(PATH +"\\"+ datoteka2)

datoteka3 = "ELES_vse_2023_1.csv"
podatki3 = pd.read_csv(PATH +"\\"+ datoteka3)


datoteka4 = "ELES_vse_2023_2.csv"
podatki4 = pd.read_csv(PATH +"\\"+ datoteka4)

datoteka5 = "mhe_2024.csv"
entso = pd.read_csv(PATH +"\\"+ datoteka5)

podatki_all = pd.concat([podatki3, podatki4], ignore_index=True) #, podatki3, podatki4

# Step 1: Convert 'začetek intervala (UTC)' to datetime
podatki_all['začetek intervala (local)'] = pd.to_datetime(podatki_all['začetek intervala (local)'], dayfirst=True).sort_index()

podatki_all['datum'] = podatki_all['začetek intervala (local)'].dt.date
podatki_all['mesec_dan'] = podatki_all['začetek intervala (local)'].dt.strftime('%m-%d')

# Extract hour
podatki_all['ura'] = podatki_all['začetek intervala (local)'].dt.hour

# podatki_avce = podatki_all[podatki_all["vir"] == "ČHE Avče Gen"].groupby(["datum", "ura"]).agg({
#     "energija (MWh)": "sum",
#     "moč (MW)": "mean"  # or 'max', 'sum', etc., depending on what you want
# }).reset_index()


podatki_sonce = podatki_all[podatki_all["vir"] == "ČHE Avče Gen"].groupby(["mesec_dan", "ura"]).agg({
    "energija (MWh)": "sum",
    "moč (MW)": "mean"  # or 'max', 'sum', etc., depending on what you want
}).reset_index()



#podatki_sonce["norm"] = podatki_sonce["energija (MWh)"]/podatki_sonce["energija (MWh)"].sum()

#podatki_sonce.to_excel(PATH + "\\ELES_biomasa_2024.xlsx", index=True)

print(entso["Fossil Oil - Actual Aggregated [MW]"].sum())

print(podatki_all["energija (MWh)"].sum())
print(podatki_sonce["energija (MWh)"].sum())

