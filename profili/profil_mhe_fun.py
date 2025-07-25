import pandas as pd
import numpy as np
import os
from calendar import isleap

def profil_mhe(scenarij):
    PATH=os.path.abspath(os.getcwd())
    ################vhodni podatki########################

    zacetno_leto = 2025
    koncno_leto = 2050

    if scenarij == "OU":
        skiprow = 63
    elif scenarij == "DUJE":
        skiprow = 74
    elif scenarij == "DUOVE":
        skiprow = 85

    #################################################

    datoteka = "Projekcije_raba_EE_IJS_v2_ag.xlsx"
    podatki = pd.read_excel(PATH +"\\"+ datoteka, sheet_name='Razprsena_proizvodnja_OVE',skiprows=skiprow ,usecols="B:AB",nrows=8 )
    podatki.set_index(podatki.columns[0], inplace=True)

    datoteka2 = "mhe_normalized.xlsx"
    podatki2 = pd.read_excel(PATH +"\\"+ datoteka2)
    podatki2.set_index(podatki2.columns[0], inplace=True)


    time_series_per_year_mhe_list = []
    for year in range(zacetno_leto, koncno_leto + 1):
        # 1. Generate hourly timestamps for the entire year
        start = f"{year}-01-01 00:00"
        end = f"{year}-12-31 23:00"
        hourly_index = pd.date_range(start=start, end=end, freq='h')
        
        # 2. Create DataFrame
        df_mhe = pd.DataFrame(index=hourly_index)

        # 3. Data from excel
        anual_total = podatki.loc["mhe",year] #je že normiran profil v MWh
        profil_norm = podatki2

        # 4. Determine days in year
        if isleap(year):
            #norm_profil = norm_profil.reset_index(drop=True)
            df_mhe["profil"] = profil_norm["Profil_norm"].values*anual_total
        else:
            profil_norm = profil_norm[~((profil_norm.index.month == 2) & (profil_norm.index.day == 29))]
            #obsevanje.reset_index(drop=True, inplace=True)
            df_mhe["profil"] = profil_norm["Profil_norm"].values*anual_total


        df_mhe.index.name = "Časovna značka"

        # 8. Save to dictionary
        #time_series_per_year_osnovni[year] = df
        time_series_per_year_mhe_list.append(df_mhe)

    time_series_per_year_mhe = pd.concat(time_series_per_year_mhe_list)

    return time_series_per_year_mhe




