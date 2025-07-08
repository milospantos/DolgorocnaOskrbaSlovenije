import pandas as pd
import numpy as np
import os
from calendar import isleap


PATH=os.path.abspath(os.getcwd())
################vhodni podatki########################

zacetno_leto = 2025
koncno_leto = 2050


datoteka11 = "au2023.csv"
podatki11 = pd.read_csv(PATH +"\\"+ datoteka11)
podatki11['Datum'] = pd.to_datetime(
    podatki11['MTU'].str.extract(r"(^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})")[0],
    format="%d.%m.%Y %H:%M"
)
podatki11.set_index('Datum', inplace=True)

datoteka12 = "au2022.csv"
podatki12 = pd.read_csv(PATH +"\\"+ datoteka12)
podatki12['Datum'] = pd.to_datetime(
    podatki12['MTU'].str.extract(r"(^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})")[0],
    format="%d.%m.%Y %H:%M"
)
podatki12.set_index('Datum', inplace=True)

datoteka13 = "au2024.csv"
podatki13 = pd.read_csv(PATH +"\\"+ datoteka13)
podatki13['Datum'] = pd.to_datetime(
    podatki13['MTU'].str.extract(r"(^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})")[0],
    format="%d.%m.%Y %H:%M"
)
podatki13.set_index('Datum', inplace=True)

#podatki.set_index(podatki.columns[0], inplace=True)

df = pd.DataFrame()
df1 = pd.DataFrame()
df2 = pd.DataFrame()
df_combined = pd.DataFrame()


df["Razlika"] = podatki11["Wind Onshore - Actual Aggregated [MW]"]
df1["Razlika"] = podatki12["Wind Onshore - Actual Aggregated [MW]"]
df2["Razlika"] = podatki13["Wind Onshore - Actual Aggregated [MW]"]


pov = (df["Razlika"].sum()+df1["Razlika"].sum()+df2["Razlika"].sum())/3
# Combine all into one DataFrame
df_all = pd.concat([df1, df, df2])
df_all = df_all.sort_index() 

leap_year_index = pd.date_range(start="2000-01-01 00:00", end="2000-12-31 23:00", freq="h")  # 8784 hours

# Step 3: Create hour-of-year index (0 to 8783)
df_all["hour_of_year"] = ((df_all.index.dayofyear - 1) * 24 + df_all.index.hour)

# Step 4: Average across the same hour of the year
hourly_profile = df_all.groupby("hour_of_year")["Razlika"].mean().reset_index()

# Step 5: Assign 2000 timestamps as index
hourly_profile["Datetime"] = leap_year_index
hourly_profile.set_index("Datetime", inplace=True)

# ✅ FIX: Normalize AFTER averaging
total_sum = hourly_profile["Razlika"].sum()
hourly_profile["Profil_norm"] = hourly_profile["Razlika"] / total_sum *1000

# Optionally drop raw values
hourly_profile = hourly_profile[["Profil_norm"]]

# Test sum again
print("Sum of normalized profile:", hourly_profile["Profil_norm"].sum())

# Multiply by 409
#hourly_profile["nov"] = hourly_profile["Profil_norm"] * 409
#print("Sum of scaled profile:", hourly_profile["nov"].sum())
# Step 7: Save to Excel
output_path = PATH + "\\wind_normalized_au.xlsx"
#hourly_profile.to_excel(output_path)

