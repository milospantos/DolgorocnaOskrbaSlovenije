import pandas as pd
import numpy as np
import os
import random



import numpy as np
import random



def branje_when2heat():

    path_to_file = os.path.join(os.getcwd(), "when2heatSI.xlsx")
    # Read the Excel file; assuming headers are in row 3 (0-indexed = row 4, A5 visually)
    #cols_to_read = list(range(5)) + [11, 12]
    # Branje podatkov s pravilnimi stolpci
    data = pd.read_excel(path_to_file, header=3,skiprows=range(4, 87666))
    # Preimenuj prvi stolpec v 'time' in pretvori v datetime
    data.rename(columns={data.columns[0]: "time"}, inplace=True)
    data["time"] = pd.to_datetime(data["time"], utc=True)

    data.rename(columns={data.columns[1]: "ASHP_floor"}, inplace=True)
    data.rename(columns={data.columns[2]: "ASHP_radiator"}, inplace=True)
    data.rename(columns={data.columns[3]: "ASHP_water"}, inplace=True)
    data.rename(columns={data.columns[4]: "GSHP_floor"}, inplace=True)
    data.rename(columns={data.columns[5]: "GSHP_radiator"}, inplace=True)
    data.rename(columns={data.columns[6]: "GSHP_water"}, inplace=True)
    data.rename(columns={data.columns[7]: "space_COM"}, inplace=True)
    data.rename(columns={data.columns[8]: "heat_profile_space_MFH"}, inplace=True)
    data.rename(columns={data.columns[9]: "heat_profile_space_SHF"}, inplace=True)
    data.rename(columns={data.columns[10]: "water_COM"}, inplace=True)
    data.rename(columns={data.columns[11]: "heat_profile_water_MHF"}, inplace=True)
    data.rename(columns={data.columns[12]: "heat_profile_water_SHF"}, inplace=True)
    data.rename(columns={data.columns[13]: "all_water_H"}, inplace=True)
    data.rename(columns={data.columns[14]: "space_H"}, inplace=True)




    data["year"] = data["time"].dt.year
    data["month"] = data["time"].dt.month
    data["day"] = data["time"].dt.day
    data["hour"] = data["time"].dt.hour

    # Filter years and months (season)
    data = data[(data["year"].between(2019, 2022))]

    # Group by day/hour to get average profile across years
    grouped = data.groupby(["month", "day", "hour"]).mean(numeric_only=True).reset_index()





    return grouped.reset_index()






    



