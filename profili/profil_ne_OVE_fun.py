import pandas as pd
import numpy as np
import os
from calendar import isleap


def profil_ne_OVE(scenarij):
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
    podatki = pd.read_excel(PATH +"\\"+ datoteka, sheet_name='Razprsena_proizvodnja_OVE',skiprows=skiprow ,usecols="B:AB",nrows=11)
    podatki.set_index(podatki.columns[0], inplace=True)



    time_series_per_year_NEOVE_list = []
    for year in range(zacetno_leto, koncno_leto + 1):
        # 1. Generate hourly timestamps for the entire year
        start = f"{year}-01-01 00:00"
        end = f"{year}-12-31 23:00"
        hourly_index = pd.date_range(start=start, end=end, freq='h')
        
        # 2. Create DataFrame
        df_NEOVE = pd.DataFrame(index=hourly_index)


        # 3. Data from excel
        anual_total = podatki.loc["neobnovljivi viri",year]*1000 # iz GWh v MWh




        # 4. Determine days in year
        if isleap(year):
            daily_total = anual_total/366
            houly_total = daily_total/24
            df_NEOVE["profil"] = houly_total

        else:

            daily_total = anual_total/365
            houly_total = daily_total/24
            df_NEOVE["profil"] = houly_total

        df_NEOVE.index.name = "Časovna značka"


        # 8. Save to dictionary
        #time_series_per_year_osnovni[year] = df
        time_series_per_year_NEOVE_list.append(df_NEOVE)

    time_series_per_year_NEOVE = pd.concat(time_series_per_year_NEOVE_list)

    return time_series_per_year_NEOVE