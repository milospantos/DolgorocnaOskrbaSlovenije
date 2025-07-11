import pandas as pd
import numpy as np
import os
from calendar import isleap

def profil_loss(podatki2):
    PATH=os.path.abspath(os.getcwd())



    ################vhodni podatki########################
    zacetno_leto = 2025
    koncno_leto = 2050



    #################################################

    datoteka = "Projekcije_raba_EE_IJS_v2_ag.xlsx"
    podatki = pd.read_excel(PATH +"\\"+ datoteka, sheet_name='RabaEE',skiprows=23,usecols="B:AB",nrows=10)
    podatki.set_index(podatki.columns[0], inplace=True)

    podatki2 = podatki2.copy()
    podatki2["leto"] =podatki2.index.year
    scaled_losses = pd.DataFrame(index=podatki2.index)

    for year in range(zacetno_leto, koncno_leto + 1):
        # 3. Get data that we need

        annual_loss = podatki.loc["izgube", year]*1000 # v MWh


        mask = podatki2["leto"] == year
        original_profile = abs(podatki2.loc[mask, "profil"])
        normalized_profile = original_profile / original_profile.sum()
        scaled_profile = normalized_profile * annual_loss

        scaled_losses.loc[mask, "profil"] = scaled_profile

    podatki2 = podatki2.drop(["leto"],axis=1)
    scaled_losses.index.name = "Časovna značka"



    return scaled_losses