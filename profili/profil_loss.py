import pandas as pd
import numpy as np
import os
from calendar import isleap


PATH=os.path.abspath(os.getcwd())



################vhodni podatki########################
zacetno_leto = 2025
koncno_leto = 2050



#################################################

datoteka = "Projekcije_raba_EE_IJS_v2_ag.xlsx"
podatki = pd.read_excel(PATH +"\\"+ datoteka, sheet_name='RabaEE',skiprows=23,usecols="B:AB",nrows=10 )
podatki.set_index(podatki.columns[0], inplace=True)

datoteka2 = "ELES_povprecje.xlsx"
podatki2 = pd.read_excel(PATH +"\\"+ datoteka2)
podatki2.set_index(podatki2.columns[0], inplace=True)


time_series_per_year_LOSS_list = []
for year in range(zacetno_leto, koncno_leto + 1):
    # 1. Generate hourly timestamps for the entire year
    start = f"{year}-01-01 00:00"
    end = f"{year}-12-31 23:00"
    hourly_index = pd.date_range(start=start, end=end, freq='h')
    

    # 2. Create DataFrame
    df_LOSS = pd.DataFrame(index=hourly_index)

    # 3. Get data that we need
    norm_profil = podatki2['Normiran profil [MWh/TWh]']
    anual_LOSS = podatki.loc["izgube", year]/1000 # v TWh

    if isleap(year):
        #norm_profil = norm_profil.reset_index(drop=True)
        df_LOSS["Profil"] = norm_profil.values*anual_LOSS
        df_LOSS.index.name = "Časovna značka"

    else:
        norm_profil = norm_profil[~((norm_profil.index.month == 2) & (norm_profil.index.day == 29))]
        #norm_profil = norm_profil.reset_index(drop=True)

        df_LOSS["Profil"] = norm_profil.values*anual_LOSS
        df_LOSS.index.name = "Časovna značka"


    
    #time_series_per_year_OU[year] = df_OU
    #time_series_per_year_DU[year] = df_DU

    time_series_per_year_LOSS_list.append(df_LOSS)
# Concatenate all years after the loop
time_series_per_year_LOSS = pd.concat(time_series_per_year_LOSS_list)



print(time_series_per_year_LOSS.sum())