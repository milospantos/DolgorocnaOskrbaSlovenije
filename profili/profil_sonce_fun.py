import pandas as pd
import numpy as np
import os
from calendar import isleap



def profil_sonce(scenarij):

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


    datoteka2 = "Projekcije_raba_EE_IJS_v2_ag.xlsx"
    podatki = pd.read_excel(PATH +"\\"+ datoteka2, sheet_name='Razprsena_proizvodnja_OVE',skiprows=skiprow ,usecols="B:AB",nrows=6 )
    podatki.set_index(podatki.columns[0], inplace=True)


    ########################################################
    koeficienti = [1.068600929, 1.074967068, 1.079479835,	1.082845745,	1.085452695,	1.087531377,	1.093160903,	1.097626883,
    1.101256265,	1.104263991, 1.106797181,	1.111865508,	1.116243163,	1.120062319,	1.123423447,	1.126404282,	1.131195786,
    1.135529629,	1.139468393,	1.143063747,	1.146358726,	1.150891022,	1.155168083,	1.159210879,	1.163038144,	1.166666667]
    # Create DataFrame
    df_koef = pd.DataFrame({
        "Year": list(range(2025, 2051)),
        "Koeficient": koeficienti
    })
    df_koef.set_index("Year", inplace=True)


    datoteka = "osvetljitev_celje.xlsx"
    profil_proiz = pd.read_excel(PATH +"\\"+ datoteka)
    profil_proiz.set_index(profil_proiz.columns[0], inplace=True)
    profil_proiz.index = pd.to_datetime(profil_proiz.index)
    profil_proiz.loc[profil_proiz["Soncno sevanje (W/m2)"] < 1, "Soncno sevanje (W/m2)"] = 0


    sestevek = profil_proiz["Soncno sevanje (W/m2)"].sum()



    time_series_per_year_distribucija_list = []
    time_series_per_year_prenos_list = []
    for year in range(zacetno_leto, koncno_leto + 1):
        # 1. Generate hourly timestamps for the entire year
        start = f"{year}-01-01 00:00"
        end = f"{year}-12-31 23:00"
        hourly_index = pd.date_range(start=start, end=end, freq='h')
        
        # 2. Create DataFrame
        df_dist = pd.DataFrame(index=hourly_index)
        df_prenos = pd.DataFrame(index=hourly_index)
        # 3. Get annual value from podatki
        skupna_moc_dist = podatki.loc["Samooskrba",year] + podatki.loc["Srednje",year]
        letna_energija_dist = skupna_moc_dist * df_koef.loc[year, "Koeficient"]*1000
        koeficienti2 = letna_energija_dist/sestevek

        skupna_moc_prenos = podatki.loc["Velike",year] + podatki.loc["Samostoječe",year]
        letna_energija_prenos = skupna_moc_prenos * df_koef.loc[year, "Koeficient"]*1000
        koeficienti3 = letna_energija_prenos/sestevek

        obsevanje = profil_proiz
        # 4. Determine days in year
        if isleap(year):
            #norm_profil = norm_profil.reset_index(drop=True)
            df_dist["profil"] = obsevanje["Soncno sevanje (W/m2)"].values*koeficienti2
            df_prenos["profil"] = obsevanje["Soncno sevanje (W/m2)"].values*koeficienti3
        else:
            obsevanje = obsevanje[~((obsevanje.index.month == 2) & (obsevanje.index.day == 29))]
            #obsevanje.reset_index(drop=True, inplace=True)
            df_dist["profil"] = obsevanje["Soncno sevanje (W/m2)"].values*koeficienti2
            df_prenos["profil"] = obsevanje["Soncno sevanje (W/m2)"].values*koeficienti3

        df_dist.index.name = "Časovna značka"
        df_prenos.index.name = "Časovna značka"
        #df = df.reset_index().rename(columns={'index': 'Časovna značka'})

        # 8. Save to dictionary
        #time_series_per_year_osnovni[year] = df
        time_series_per_year_distribucija_list.append(df_dist)
        time_series_per_year_prenos_list.append(df_prenos)

    time_series_per_year_distribucija = pd.concat(time_series_per_year_distribucija_list)
    time_series_per_year_prenos = pd.concat(time_series_per_year_prenos_list)

    return time_series_per_year_distribucija, time_series_per_year_prenos