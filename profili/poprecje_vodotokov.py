import pandas as pd
import numpy as np
import os
from calendar import isleap


zacetno_leto = 2025
koncno_leto = 2050

PATH=os.path.abspath(os.getcwd())

#izgled koncne datoteke
datoteka = "sava4_vodotok_pred_catez.xls"
podatki = pd.read_excel(PATH +"\\"+ datoteka, sheet_name=None)
df = podatki["hid_arhiv"] 

df.columns = ["Datum", "Pretok"]

# Convert 'Datum' to datetime
df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y", errors="coerce")

# Convert 'Pretok' to float (replace comma with dot)
df["Pretok"] = df["Pretok"].astype(str).str.replace(",", ".").astype(float)

# Create "day of year" column (month & day only)
df["DayOfYear"] = df["Datum"].dt.strftime("%m-%d")

# Group by DayOfYear and calculate the average
daily_avg = df.groupby("DayOfYear")["Pretok"].mean()


time_series_per_year_list = []
for year in range(zacetno_leto, koncno_leto + 1):
    # Generate hourly timestamps for entire year
    # start = f"{year}-01-01 00:00"
    # end = f"{year}-12-31 23:00"
    # hourly_index = pd.date_range(start=start, end=end, freq='h')

    if not isleap(year):
        daily_avg_filtered = daily_avg[~(daily_avg.index == "02-29")]
    else:
        daily_avg_filtered = daily_avg
    # Reconstruct daily_avg_df with proper dates for the current year
    daily_avg_df = daily_avg_filtered.reset_index()
    daily_avg_df["Datum"] = pd.to_datetime(f"{year}-" + daily_avg_df["DayOfYear"], format="%Y-%m-%d")
    daily_avg_df = daily_avg_df.sort_values("Datum").reset_index(drop=True)

    # List to hold the hourly profile
    hourly_rows = []

    for i in range(len(daily_avg_df) - 1):
        start_day = daily_avg_df.loc[i, "Datum"]
        end_day = daily_avg_df.loc[i + 1, "Datum"]
        
        start_value = daily_avg_df.loc[i, "Pretok"]
        end_value = daily_avg_df.loc[i + 1, "Pretok"]

        hourly_values = np.linspace(start_value, end_value, 24)
        for h in range(24):
            timestamp = start_day + pd.Timedelta(hours=h)
            hourly_rows.append({"Časovna značka": timestamp, "Pretok": hourly_values[h]})

    # Handle last day
    last_day = daily_avg_df.iloc[-1]
    for h in range(24):
        timestamp = last_day["Datum"] + pd.Timedelta(hours=h)
        hourly_rows.append({"Časovna značka": timestamp, "Pretok": last_day["Pretok"]})

    # Build interpolated DataFrame
    interpolated_df = pd.DataFrame(hourly_rows).set_index("Časovna značka")

    # Append to list
    time_series_per_year_list.append(interpolated_df)

time_series_per_year = pd.concat(time_series_per_year_list)
output_path = "sava_pred_catez_2025-2050.xlsx"  # or any desired path
time_series_per_year.to_excel(output_path)