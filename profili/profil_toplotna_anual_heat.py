import pandas as pd
import numpy as np
import os
from calendar import isleap
from read_when2heat import branje_when2heat


################vhodni podatki########################
zacetno_leto = 2025
koncno_leto = 2029
procent_flor_H = 20
procent_radidator_H = 80
percent_space_H = 80
percent_water_H = 20
percent_COM_water = 20
percent_COM_space = 80





PATH=os.path.abspath(os.getcwd())

datoteka = "Projekcije_raba_EE_IJS_v2_ag.xlsx"
podatki = pd.read_excel(PATH +"\\"+ datoteka, sheet_name='PodatkiONapravah',skiprows=82 ,usecols="F:AG",nrows=8 )
podatki = podatki.drop(podatki.columns[1], axis=1)
podatki.set_index(podatki.columns[0], inplace=True)
podatki = podatki.round(0)

prfiles_HP = branje_when2heat()

########################## COMERCIAL HEATING PUMP#########
# Dictionary to hold time series for each year
time_series_per_year_comertial= {}
time_series_per_year_GSHP= {}
time_series_per_year_ASHP= {}
time_series_per_year_SANITARNE= {}

for year in range(zacetno_leto, koncno_leto):
    # 1. Generate hourly timestamps for the entire year
    start = f"{year}-01-01 00:00"
    end = f"{year}-12-31 23:00"
    hourly_index = pd.date_range(start=start, end=end, freq='h')
    

    # 2. Create DataFrame
    df = pd.DataFrame(index=hourly_index)

    # 3. Get annual value from podatki
    #COM
    annual_total_COM = podatki.loc['Raba v storitvah - samo za toplotne črpalke', year]/1000  ##### odvisno katero toplotno hočemo GWh  v tWh /1000
    demand_water_COM = annual_total_COM*percent_COM_water/100
    demand_space_COM = annual_total_COM*percent_COM_space/100

    #GSHP
    annual_total_GSHP = podatki.loc['GSHP(Geosonde + kolektorske)', year]/1000  ##### odvisno katero toplotno hočemo GWh  v tWh /1000
    demand_water_GSHP = annual_total_GSHP*percent_water_H/100
    demand_space_H_GSHP = annual_total_GSHP*percent_space_H/100
    demand_space_floor_GSHP = demand_space_H_GSHP * procent_flor_H/100
    demand_space_radiator_GSHP = demand_space_H_GSHP * procent_radidator_H/100

    #ASHP
    annual_total_ASHP = podatki.loc['Zrak-voda', year]/1000  ##### odvisno katero toplotno hočemo GWh  v tWh /1000
    demand_water_ASHP = annual_total_ASHP*percent_water_H/100
    demand_space_H_ASHP = annual_total_ASHP*percent_space_H/100
    demand_space_floor_ASHP = demand_space_H_ASHP * procent_flor_H/100
    demand_space_radiator_ASHP = demand_space_H_ASHP * procent_radidator_H/100
    #SANITARNE
    annual_total_SANITARNE = podatki.loc['Sanitarne', year]/1000  ##### odvisno katero toplotno hočemo GWh  v tWh /1000


    # 4. Determine days in year
    if isleap(year):
        #COM
        prifile_heat_demand_space_COM = prfiles_HP["space_COM"]*demand_space_COM 
        prifile_heat_demand_water_COM = prfiles_HP["water_COM"]*demand_water_COM

        profile_el_demand_space_COM = prifile_heat_demand_space_COM/prfiles_HP["GSHP_radiator"]
        profile_el_demand_water_COM = prifile_heat_demand_water_COM/prfiles_HP["GSHP_water"]

        #GSHP
        prifile_heat_demad_water_GSHP = prfiles_HP["all_water_H"]*demand_water_GSHP
        prifile_heat_demad_floor_GSHP = prfiles_HP["space_H"]*demand_space_floor_GSHP 
        prifile_heat_demad_radiator_GSHP = prfiles_HP["space_H"]*demand_space_radiator_GSHP 

        profile_el_demand_floor_GSHP = prifile_heat_demad_floor_GSHP/prfiles_HP["GSHP_floor"]
        profile_el_demand_radiator_GSHP = prifile_heat_demad_radiator_GSHP/prfiles_HP["GSHP_radiator"]
        profile_el_demand_water_GSHP = prifile_heat_demad_water_GSHP/prfiles_HP["GSHP_water"]

        #ASHP
        prifile_heat_demad_water_ASHP = prfiles_HP["all_water_H"]*demand_water_ASHP
        prifile_heat_demad_floor_ASHP = prfiles_HP["space_H"]*demand_space_floor_ASHP 
        prifile_heat_demad_radiator_ASHP = prfiles_HP["space_H"]*demand_space_radiator_ASHP 

        profile_el_demand_floor_ASHP = prifile_heat_demad_floor_ASHP/prfiles_HP["ASHP_floor"]
        profile_el_demand_radiator_ASHP = prifile_heat_demad_radiator_ASHP/prfiles_HP["ASHP_radiator"]
        profile_el_demand_water_ASHP = prifile_heat_demad_water_ASHP/prfiles_HP["ASHP_water"]

        #SANITARNE
        prifile_heat_demand_SANITARNE = prfiles_HP["all_water_H"]*annual_total_SANITARNE 
        profile_el_demand_SANITARNE = prifile_heat_demand_SANITARNE/prfiles_HP["ASHP_water"]

    else:
        # Drop all February 29 rows
        prfiles_HP_leap = prfiles_HP[~((prfiles_HP["month"] == 2) & (prfiles_HP["day"] == 29))]
        prfiles_HP_leap = prfiles_HP_leap.reset_index(drop=True)

        #COM
        prifile_heat_demand_space_COM = prfiles_HP_leap["space_COM"]*demand_space_COM 
        prifile_heat_demand_water_COM = prfiles_HP_leap["water_COM"]*demand_water_COM

        profile_el_demand_space_COM = prifile_heat_demand_space_COM/prfiles_HP_leap["GSHP_radiator"]
        profile_el_demand_water_COM = prifile_heat_demand_water_COM/prfiles_HP_leap["GSHP_water"]

        #GSHP
        prifile_heat_demad_water_GSHP = prfiles_HP_leap["all_water_H"]*demand_water_GSHP
        prifile_heat_demad_floor_GSHP = prfiles_HP_leap["space_H"]*demand_space_floor_GSHP 
        prifile_heat_demad_radiator_GSHP = prfiles_HP_leap["space_H"]*demand_space_radiator_GSHP 

        profile_el_demand_floor_GSHP = prifile_heat_demad_floor_GSHP/prfiles_HP_leap["GSHP_floor"]
        profile_el_demand_radiator_GSHP = prifile_heat_demad_radiator_GSHP/prfiles_HP_leap["GSHP_radiator"]
        profile_el_demand_water_GSHP = prifile_heat_demad_water_GSHP/prfiles_HP_leap["GSHP_water"]

        #ASHP
        prifile_heat_demad_water_ASHP = prfiles_HP_leap["all_water_H"]*demand_water_ASHP
        prifile_heat_demad_floor_ASHP = prfiles_HP_leap["space_H"]*demand_space_floor_ASHP 
        prifile_heat_demad_radiator_ASHP = prfiles_HP_leap["space_H"]*demand_space_radiator_ASHP 

        profile_el_demand_floor_ASHP = prifile_heat_demad_floor_ASHP/prfiles_HP_leap["ASHP_floor"]
        profile_el_demand_radiator_ASHP = prifile_heat_demad_radiator_ASHP/prfiles_HP_leap["ASHP_radiator"]
        profile_el_demand_water_ASHP = prifile_heat_demad_water_ASHP/prfiles_HP_leap["ASHP_water"]
        
        #SANITARNE
        prifile_heat_demand_SANITARNE = prfiles_HP_leap["all_water_H"]*annual_total_SANITARNE 
        profile_el_demand_SANITARNE = prifile_heat_demand_SANITARNE/prfiles_HP_leap["ASHP_water"]

    profile_el_demand_COM = round(profile_el_demand_space_COM + profile_el_demand_water_COM,0)
    profile_el_demand_GSHP = round(profile_el_demand_water_GSHP + profile_el_demand_radiator_GSHP + profile_el_demand_floor_GSHP,0)
    profile_el_demand_ASHP = round(profile_el_demand_water_ASHP + profile_el_demand_floor_ASHP + profile_el_demand_radiator_ASHP,0)
    profile_el_demand_SANITARNE = round(profile_el_demand_SANITARNE,0)
    # 8. Save to dictionary
    time_series_per_year_comertial[year] = profile_el_demand_COM
    time_series_per_year_GSHP[year] = profile_el_demand_GSHP
    time_series_per_year_ASHP[year] = profile_el_demand_ASHP
    time_series_per_year_SANITARNE[year] = profile_el_demand_SANITARNE


    print(len(time_series_per_year_GSHP[2028]))