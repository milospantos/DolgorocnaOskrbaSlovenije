import pandas as pd
import numpy as np
import os
from calendar import isleap



def profil_odjema(scenarij):

    PATH=os.path.abspath(os.getcwd())
    datoteka = "Projekcije_raba_EE_IJS_v2_ag.xlsx"
    podatki = pd.read_excel(PATH +"\\"+ datoteka, sheet_name='RabaEE',skiprows=23,usecols="B:AB",nrows=8)
    podatki.set_index(podatki.columns[0], inplace=True)

    datoteka2 = "ELES_povprecje5.xlsx"

    podatki2 = pd.read_excel(PATH +"\\"+ datoteka2)
    podatki2.set_index(podatki2.columns[0], inplace=True)
    podatki2["leto"] =podatki2.index.year

    #########################
    ### VHODNI PODATKI

    zacetno_leto = 2025
    koncno_leto = 2050


    if scenarij =="OU":
        vrstica = "Razlika koncna raba OU"
    elif scenarij == "DU":
        vrstica = "Razlika koncna raba DU"



    for year in range(zacetno_leto, koncno_leto + 1):
        # 3. Get data that we need

        anual_consumption = podatki.loc[vrstica, year]/1000 # v TWh
        #anual_consumption_DO = podatki.loc["Razlika DU  [GWh]", year]/1000 # v TWh

        mask = podatki2["leto"] == year
        podatki2.loc[mask, "profil"] = podatki2.loc[mask, "Normiran profil [MWh/TWh]"] * anual_consumption

    podatki2 = podatki2.drop(["Normiran profil [MWh/TWh]", "leto"],axis=1)
    podatki2.index.name = "Časovna značka"

    return podatki2