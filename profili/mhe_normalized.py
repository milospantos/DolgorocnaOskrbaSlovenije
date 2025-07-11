import pandas as pd
import numpy as np
import os
from calendar import isleap


PATH=os.path.abspath(os.getcwd())

datoteka21 = "ELES_2023.xlsx"
podatki21 = pd.read_excel(PATH +"\\"+ datoteka21)
podatki21['Hour_num'] = podatki21['ura'].str.extract(r"H(\d{2})").astype(int) - 1

# Combine date and hour into one datetime
podatki21['datum'] = pd.to_datetime(podatki21['datum'], format="%d.%m.%Y") + pd.to_timedelta(podatki21['Hour_num'], unit='h')

# Set as index
podatki21.set_index('datum', inplace=True)

# Optionally drop the temporary columns
podatki21.drop(columns=['Hour_num', 'ura'], inplace=True)

datoteka22 = "ELES_2022.xlsx"
podatki22 = pd.read_excel(PATH +"\\"+ datoteka22)
podatki22['Hour_num'] = podatki22['ura'].str.extract(r"H(\d{2})").astype(int) - 1

# Combine date and hour into one datetime
podatki22['datum'] = pd.to_datetime(podatki22['datum'], format="%d.%m.%Y") + pd.to_timedelta(podatki22['Hour_num'], unit='h')

# Set as index
podatki22.set_index('datum', inplace=True)

# Optionally drop the temporary columns
podatki22.drop(columns=['Hour_num', 'ura'], inplace=True)

datoteka23 = "ELES_2024.xlsx"
podatki23 = pd.read_excel(PATH +"\\"+ datoteka23)
podatki23['Hour_num'] = podatki23['ura'].str.extract(r"H(\d{2})").astype(int) - 1

# Combine date and hour into one datetime
podatki23['datum'] = pd.to_datetime(podatki23['datum'], format="%d.%m.%Y") + pd.to_timedelta(podatki23['Hour_num'], unit='h')

# Set as index
podatki23.set_index('datum', inplace=True)

# Optionally drop the temporary columns
podatki23.drop(columns=['Hour_num', 'ura'], inplace=True)






datoteka11 = "mhe_2023.csv"
podatki11 = pd.read_csv(PATH +"\\"+ datoteka11)
podatki11['Datum'] = pd.to_datetime(
    podatki11['MTU'].str.extract(r"(^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})")[0],
    format="%d.%m.%Y %H:%M"
)
podatki11.set_index('Datum', inplace=True)

datoteka12 = "mhe_2022.csv"
podatki12 = pd.read_csv(PATH +"\\"+ datoteka12)
podatki12['Datum'] = pd.to_datetime(
    podatki12['MTU'].str.extract(r"(^\d{2}\.\d{2}\.\d{4} \d{2}:\d{2})")[0],
    format="%d.%m.%Y %H:%M"
)
podatki12.set_index('Datum', inplace=True)

datoteka13 = "mhe_2024.csv"
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


df["Razlika"] = podatki11["Hydro Run-of-river and poundage - Actual Aggregated [MW]"] + podatki11["Hydro Pumped Storage - Actual Aggregated [MW]"]- podatki21["hidro"]
df1["Razlika"] = podatki12["Hydro Run-of-river and poundage - Actual Aggregated [MW]"] + podatki12["Hydro Pumped Storage - Actual Aggregated [MW]"]- podatki22["hidro"]
df2["Razlika"] = podatki13["Hydro Run-of-river and poundage - Actual Aggregated [MW]"] + podatki13["Hydro Pumped Storage - Actual Aggregated [MW]"]- podatki23["hidro"]


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
output_path = PATH + "\\mhe_normalized.xlsx"
#hourly_profile.to_excel(output_path)



