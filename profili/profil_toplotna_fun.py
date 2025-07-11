import pandas as pd
import numpy as np
import os
from calendar import isleap
from read_when2heat import branje_when2heat





def profil_toplotna():
    ################vhodni podatki########################
    zacetno_leto = 2025
    koncno_leto = 2050
    procent_flor_H = 20
    procent_radidator_H = 80
    percent_space_H = 80
    percent_water_H = 20
    percent_COM_water = 20
    percent_COM_space = 80





    PATH=os.path.abspath(os.getcwd())

    datoteka = "Projekcije_raba_EE_IJS_v2_ag.xlsx"
    podatki = pd.read_excel(PATH +"\\"+ datoteka, sheet_name='PodatkiONapravah',skiprows=82 ,usecols="F:AH",nrows=8 )
    podatki = podatki.drop(podatki.columns[1], axis=1)
    podatki.set_index(podatki.columns[0], inplace=True)
    podatki = podatki.round(0)

    prfiles_HP = branje_when2heat()

    ########################## COMERCIAL HEATING PUMP#########
    # Dictionary to hold time series for each year
    # time_series_per_year_comertial= {}
    # time_series_per_year_GSHP= {}
    # time_series_per_year_ASHP= {}
    # time_series_per_year_SANITARNE= {}
    time_series_per_year_comertial_list= []
    time_series_per_year_GSHP_list= []
    time_series_per_year_ASHP_list= []
    time_series_per_year_SANITARNE_list= []

    for year in range(zacetno_leto, koncno_leto +1):
        # 1. Generate hourly timestamps for the entire year
        start = f"{year}-01-01 00:00"
        end = f"{year}-12-31 23:00"
        hourly_index = pd.date_range(start=start, end=end, freq='h')
        

        # 2. Create DataFrame
        hourly_index.name = "Časovna značka"
        df_profile_el_demand_COM = pd.DataFrame(index=hourly_index)
        df_profile_el_demand_GSHP = pd.DataFrame(index=hourly_index)
        df_profile_el_demand_ASHP = pd.DataFrame(index=hourly_index)
        df_profile_el_demand_SANITARNE = pd.DataFrame(index=hourly_index)
        # 3. Get annual value from podatki
        #COM
        annual_total_COM = podatki.loc['Raba v storitvah - samo za toplotne črpalke', year]*1000  ##### odvisno katero toplotno hočemo GWh  v MWh *1000
        demand_water_COM = annual_total_COM*percent_COM_water/100
        demand_space_COM = annual_total_COM*percent_COM_space/100

        #GSHP
        annual_total_GSHP = podatki.loc['GSHP(Geosonde + kolektorske)', year]*1000  ##### odvisno katero toplotno hočemo GWh  v MWh *1000
        demand_water_GSHP = annual_total_GSHP*percent_water_H/100
        demand_space_H_GSHP = annual_total_GSHP*percent_space_H/100
        demand_space_floor_GSHP = demand_space_H_GSHP * procent_flor_H/100
        demand_space_radiator_GSHP = demand_space_H_GSHP * procent_radidator_H/100

        #ASHP
        annual_total_ASHP = podatki.loc['Zrak-voda', year]*1000  ##### odvisno katero toplotno hočemo GWh  v MWh *1000
        demand_water_ASHP = annual_total_ASHP*percent_water_H/100
        demand_space_H_ASHP = annual_total_ASHP*percent_space_H/100
        demand_space_floor_ASHP = demand_space_H_ASHP * procent_flor_H/100
        demand_space_radiator_ASHP = demand_space_H_ASHP * procent_radidator_H/100
        #SANITARNE
        annual_total_SANITARNE = podatki.loc['Sanitarne', year]*1000  ##### odvisno katero toplotno hočemo GWh  v MWh *1000


        # 4. Determine days in year
        if isleap(year):
            #COM
            profile_el_demand_space_COM = prfiles_HP["space_COM"]/prfiles_HP["GSHP_radiator"]
            total_el_demand_space_COM= profile_el_demand_space_COM.sum()
            scaling_factor = demand_space_COM / total_el_demand_space_COM
            final_profile_el_space_COM = profile_el_demand_space_COM*scaling_factor

            profile_el_demand_water_COM = prfiles_HP["water_COM"]/prfiles_HP["GSHP_water"]
            total_el_demand_water_COM= profile_el_demand_water_COM.sum()
            scaling_factor = demand_water_COM / total_el_demand_water_COM
            final_profile_el_water_COM = profile_el_demand_water_COM*scaling_factor

            #GSHP
            profile_el_demand_floor_GSHP = prfiles_HP["space_H"]/prfiles_HP["GSHP_floor"]
            total_el_demand_floor_GSHP= profile_el_demand_floor_GSHP.sum()
            scaling_factor = demand_space_floor_GSHP / total_el_demand_floor_GSHP
            final_profile_el_floor_GSHP = profile_el_demand_floor_GSHP*scaling_factor

            profile_el_demand_radiator_GSHP = prfiles_HP["space_H"]/prfiles_HP["GSHP_radiator"]
            total_el_demand_radiator_GSHP= profile_el_demand_radiator_GSHP.sum()
            scaling_factor = demand_space_radiator_GSHP / total_el_demand_radiator_GSHP
            final_profile_el_radiator_GSHP = profile_el_demand_radiator_GSHP*scaling_factor

            profile_el_demand_water_GSHP = prfiles_HP["all_water_H"]/prfiles_HP["GSHP_water"]
            total_el_demand_water_GSHP= profile_el_demand_water_GSHP.sum()
            scaling_factor = demand_water_GSHP / total_el_demand_water_GSHP
            final_profile_el_water_GSHP = profile_el_demand_water_GSHP*scaling_factor

            #ASHP
            profile_el_demand_floor_ASHP = prfiles_HP["space_H"]/prfiles_HP["ASHP_floor"]
            total_el_demand_floor_ASHP= profile_el_demand_floor_ASHP.sum()
            scaling_factor = demand_space_floor_ASHP / total_el_demand_floor_ASHP
            final_profile_el_floor_ASHP = profile_el_demand_floor_ASHP*scaling_factor

            profile_el_demand_radiator_ASHP = prfiles_HP["space_H"]/prfiles_HP["ASHP_radiator"]
            total_el_demand_radiator_ASHP= profile_el_demand_radiator_ASHP.sum()
            scaling_factor = demand_space_radiator_ASHP / total_el_demand_radiator_ASHP
            final_profile_el_radiator_ASHP = profile_el_demand_radiator_ASHP*scaling_factor

            profile_el_demand_water_ASHP = prfiles_HP["all_water_H"]/prfiles_HP["ASHP_water"]
            total_el_demand_water_ASHP= profile_el_demand_water_ASHP.sum()
            scaling_factor = demand_water_ASHP / total_el_demand_water_ASHP
            final_profile_el_water_ASHP = profile_el_demand_water_ASHP*scaling_factor

            #SANITARNE
            profile_el_demand_SAN = prfiles_HP["all_water_H"]/prfiles_HP["ASHP_water"]
            total_el_demand_SANITARNE= profile_el_demand_SAN.sum()
            scaling_factor = annual_total_SANITARNE / total_el_demand_SANITARNE
            final_profile_el_SANITARNE = profile_el_demand_SAN*scaling_factor

        else:
            # Drop all February 29 rows
            prfiles_HP_leap = prfiles_HP[~((prfiles_HP["month"] == 2) & (prfiles_HP["day"] == 29))]
            prfiles_HP_leap = prfiles_HP_leap.reset_index(drop=True)

            #COM
            profile_el_demand_space_COM = prfiles_HP_leap["space_COM"]/prfiles_HP_leap["GSHP_radiator"]
            total_el_demand_space_COM= profile_el_demand_space_COM.sum()
            scaling_factor = demand_space_COM / total_el_demand_space_COM
            final_profile_el_space_COM = profile_el_demand_space_COM*scaling_factor

            profile_el_demand_water_COM = prfiles_HP_leap["water_COM"]/prfiles_HP_leap["GSHP_water"]
            total_el_demand_water_COM= profile_el_demand_water_COM.sum()
            scaling_factor = demand_water_COM / total_el_demand_water_COM
            final_profile_el_water_COM = profile_el_demand_water_COM*scaling_factor


            #GSHP
            profile_el_demand_floor_GSHP = prfiles_HP_leap["space_H"]/prfiles_HP_leap["GSHP_floor"]
            total_el_demand_floor_GSHP= profile_el_demand_floor_GSHP.sum()
            scaling_factor = demand_space_floor_GSHP / total_el_demand_floor_GSHP
            final_profile_el_floor_GSHP = profile_el_demand_floor_GSHP*scaling_factor

            profile_el_demand_radiator_GSHP = prfiles_HP_leap["space_H"]/prfiles_HP_leap["GSHP_radiator"]
            total_el_demand_radiator_GSHP= profile_el_demand_radiator_GSHP.sum()
            scaling_factor = demand_space_radiator_GSHP / total_el_demand_radiator_GSHP
            final_profile_el_radiator_GSHP = profile_el_demand_radiator_GSHP*scaling_factor

            profile_el_demand_water_GSHP = prfiles_HP_leap["all_water_H"]/prfiles_HP_leap["GSHP_water"]
            total_el_demand_water_GSHP= profile_el_demand_water_GSHP.sum()
            scaling_factor = demand_water_GSHP / total_el_demand_water_GSHP
            final_profile_el_water_GSHP = profile_el_demand_water_GSHP*scaling_factor

            #ASHP
            profile_el_demand_floor_ASHP = prfiles_HP_leap["space_H"]/prfiles_HP_leap["ASHP_floor"]
            total_el_demand_floor_ASHP= profile_el_demand_floor_ASHP.sum()
            scaling_factor = demand_space_floor_ASHP / total_el_demand_floor_ASHP
            final_profile_el_floor_ASHP = profile_el_demand_floor_ASHP*scaling_factor

            profile_el_demand_radiator_ASHP = prfiles_HP_leap["space_H"]/prfiles_HP_leap["ASHP_radiator"]
            total_el_demand_radiator_ASHP= profile_el_demand_radiator_ASHP.sum()
            scaling_factor = demand_space_radiator_ASHP / total_el_demand_radiator_ASHP
            final_profile_el_radiator_ASHP = profile_el_demand_radiator_ASHP*scaling_factor

            profile_el_demand_water_ASHP = prfiles_HP_leap["all_water_H"]/prfiles_HP_leap["ASHP_water"]
            total_el_demand_water_ASHP= profile_el_demand_water_ASHP.sum()
            scaling_factor = demand_water_ASHP / total_el_demand_water_ASHP
            final_profile_el_water_ASHP = profile_el_demand_water_ASHP*scaling_factor
            
            #SANITARNE
            profile_el_demand_SAN = prfiles_HP_leap["all_water_H"]/prfiles_HP_leap["ASHP_water"]
            total_el_demand_SANITARNE= profile_el_demand_SAN.sum()
            scaling_factor = annual_total_SANITARNE / total_el_demand_SANITARNE
            final_profile_el_SANITARNE = profile_el_demand_SAN*scaling_factor



        df_profile_el_demand_COM["profil"] = (final_profile_el_space_COM.values + final_profile_el_water_COM.values).round(0)
        df_profile_el_demand_GSHP["profil"] = (final_profile_el_water_GSHP.values + final_profile_el_radiator_GSHP.values + final_profile_el_floor_GSHP.values).round(0)
        df_profile_el_demand_ASHP["profil"] = (final_profile_el_water_ASHP.values + final_profile_el_floor_ASHP.values + final_profile_el_radiator_ASHP.values).round(0)
        df_profile_el_demand_SANITARNE["profil"] = (final_profile_el_SANITARNE.values).round(0)
        # 8. Save to dictionary
        # time_series_per_year_comertial[year] = profile_el_demand_COM
        # time_series_per_year_GSHP[year] = profile_el_demand_GSHP
        # time_series_per_year_ASHP[year] = profile_el_demand_ASHP
        # time_series_per_year_SANITARNE[year] = profile_el_demand_SANITARNE
        time_series_per_year_comertial_list.append(df_profile_el_demand_COM)
        time_series_per_year_GSHP_list.append(df_profile_el_demand_GSHP)
        time_series_per_year_ASHP_list.append(df_profile_el_demand_ASHP)
        time_series_per_year_SANITARNE_list.append(df_profile_el_demand_SANITARNE)

    time_series_per_year_comertial = pd.concat(time_series_per_year_comertial_list)
    time_series_per_year_GSHP = pd.concat(time_series_per_year_GSHP_list)
    time_series_per_year_ASHP = pd.concat(time_series_per_year_ASHP_list)
    time_series_per_year_SANITARNE = pd.concat(time_series_per_year_SANITARNE_list)

    

    combined_profiles = time_series_per_year_comertial + time_series_per_year_GSHP + time_series_per_year_ASHP + time_series_per_year_SANITARNE
    combined_profiles.index.name = "Časovna značka"
    return  combined_profiles