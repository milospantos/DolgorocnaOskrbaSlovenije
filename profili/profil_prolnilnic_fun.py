import pandas as pd
import numpy as np
import os
from calendar import isleap


def dela_prost_dan(data):
    dela_prosti_dnevi = ('01-01', '01-02', '02-08', '04-27', '05-01', '05-02', '06-25', '08-15', '10-31', '11-01', '12-25', '12-26')    
    # data['Časovna značka'] = pd.to_datetime(data.index)   
    # data.set_index('Časovna značka', drop=False, inplace=True)
    # data['Month']=data.index.month
    # data['Hour']=data.index.hour
    data['Day']=data.index.weekday +1  #1 - Monday, 7 - Sunday
    # data['Sezona']=data['Month'].isin([1,2,11,12]).astype(int)  #Višja sezona
    data['Dela prost dan']=data.index.strftime('%m-%d').isin(dela_prosti_dnevi).astype(int)
    data.loc[(data['Day'].isin([6,7])),'Dela prost dan']=1
    return data

def get_season(ts):
    month = ts.month
    if month in [6, 7, 8]:
        return 'summer'
    elif month in [12, 1, 2]:
        return 'winter'
    else:
        return 'autumn_spring'

def profil_polnilnic():

    ################vhodni podatki########################
    ###osnovni
    # procent_cez_dan = 30
    # procent_cez_noc = 100 - procent_cez_dan
    # zacetno_leto = 2025
    # koncno_leto = 2050
    # ura_noc = 21
    # ura_jutro = 7

    ##############################################################

    PATH=os.path.abspath(os.getcwd())

    datoteka = "Projekcije_raba_EE_IJS_v2_ag.xlsx"
    podatki = pd.read_excel(PATH +"\\"+ datoteka, sheet_name='PodatkiONapravah',skiprows=66,usecols="F:AL",nrows=13 )
    podatki = podatki.drop(podatki.columns[1], axis=1)
    podatki.set_index(podatki.columns[0], inplace=True)
    podatki = podatki.round(0)

    ########################## OSNOVNI PROFIL#########
    # Dictionary to hold time series for each year
    #time_series_per_year_osnovni = {}
    # time_series_per_year_osnovni_list = []

    # for year in range(zacetno_leto, koncno_leto + 1):
    #     # 1. Generate hourly timestamps for the entire year
    #     start = f"{year}-01-01 00:00"
    #     end = f"{year}-12-31 23:00"
    #     hourly_index = pd.date_range(start=start, end=end, freq='h')
        

    #     # 2. Create DataFrame
    #     df = pd.DataFrame(index=hourly_index)

    #     # 3. Get annual value from podatki
    #     annual_total = podatki.loc['Elektrika v prometu', year]  ##### odvisno kater promet hočemo

    #     # 4. Determine days in year
    #     num_days = 366 if isleap(year) else 365

    #     # 5. Compute daily total
    #     daily_total = annual_total*1000 / num_days   # damo v MWh

    #     # 6. Compute hourly values
    #     night_value = (daily_total * procent_cez_dan/100) / (24-ura_noc+ura_jutro)  # night hours
    #     day_value   = (daily_total * procent_cez_noc/100) / (ura_noc-ura_jutro)  # day hours

    #     # 7. Assign value based on hour
    #     def assign_value(hour):
    #         return night_value if hour >= ura_noc or hour < ura_jutro else day_value

    #     df['profil'] = df.index.hour.map(assign_value)
    #     df.index.name = "Časovna značka"
    #     #df = df.reset_index().rename(columns={'index': 'Časovna značka'})

    #     # 8. Save to dictionary
    #     #time_series_per_year_osnovni[year] = df
    #     time_series_per_year_osnovni_list.append(df)
    
    # time_series_per_year_osnovni = pd.concat(time_series_per_year_osnovni_list)

    ########################## NAPREDNI PROFIL#########
    ####napredni
    zacetno_leto_n = 2025
    koncno_leto_n = 2050
            ############# AVTOMOBILI DOMAČI
    procent_vikend = 30          # nam pove koliko flote se bo polnilo tekom vikenda
    procent_delavnik = 100 - procent_vikend     # nam pove koliko flote se bo polnilo preko tedna

    procent_work_avti_00_06 = 25
    procent_work_avti_06_10 = 10
    procent_work_avti_10_18 = 20
    procent_work_avti_18_22 = 35
    procent_work_avti_22_00= 10

    procent_weekend_avti_00_06 = 15
    procent_weekend_avti_06_10 = 10
    procent_weekend_avti_10_18 = 40
    procent_weekend_avti_18_22 = 25
    procent_weekend_avti_22_00= 10


            ########## ŽIČNICE
    ura_jutro_ž = 8
    ura_vecer_ž = 17
            ########## VLAKI
    ura_vecer_vlaki = 23
    ura_jutro_vlaki = 6
    
    procent_tovorni_vlak_dan = 60
    procent_tovorni_vlak_noc = 40
            ########## TOVORNA VOZILA
    procent_vikend_tovorna = 15             # nam pove koliko flote se bo polnilo tekom vikenda
    procent_delavnik_tovorna = 100 - procent_vikend_tovorna     # nam pove koliko flote se bo polnilo preko tedna

    procent_cez_dan_vik_tovorna = 40      # nam pove koliko se avtomobili polnijo tekom neva oz. ponoči
    procent_cez_noc_vik_tovorna = 100 - procent_cez_dan_vik_tovorna

    ura_noc_vik_tovorna = 18    # kdaj se začne noč pri vekendu
    ura_jutro_vik_tovorna = 10

    procent_del_00_06 = 50
    procent_del_06_09 = 5
    procent_del_09_17 = 20
    procent_del_17_20 = 10
    procent_del_20_00 = 15

            ########## AVTOBUSI
    procent_vikend_avtobusi = 25             # nam pove koliko flote se bo polnilo tekom vikenda
    procent_delavnik_avtobusi = 100 - procent_vikend_avtobusi     # nam pove koliko flote se bo polnilo preko tedna

    procent_avtobusi_00_06 = 45
    procent_avtobusi_06_09 = 10
    procent_avtobusi_09_15 = 15
    procent_avtobusi_15_20 = 10
    procent_avtobusi_20_00 = 20
            ########## TUJI AVTI

    procent_poletje = 60
    procent_zima = 20
    procent_jesen_pomald = 20

    procent_tuji_vikend = 65
    procent_tuji_delavnik = 100 - procent_tuji_vikend

    procent_tuji_00_06 = 5
    procent_tuji_06_10 = 20
    procent_tuji_10_14 = 30
    procent_tuji_14_22 = 40
    procent_tuji_22_00 = 5

    # Dictionary to hold time series for each year
    time_series_per_year_avto_list = []
    time_series_per_year_zicnice_list = []
    time_series_per_year_vlaki_list = []
    time_series_per_year_tovorna_vozila_list = []
    time_series_per_year_avtobusi_list = []
    time_series_per_year_tuji_avti_list = []


    for year in range(zacetno_leto_n, koncno_leto_n + 1):
        # 1. Generate hourly timestamps for the entire year
        start = f"{year}-01-01 00:00"
        end = f"{year}-12-31 23:00"
        hourly_index = pd.date_range(start=start, end=end, freq='h')

        num_days = 366 if isleap(year) else 365
        # 2. Create DataFrame
        df_avto = pd.DataFrame(index=hourly_index)
        df_avto = dela_prost_dan(df_avto)
        df_zicnice = df_avto.copy()
        df_vlaki = df_avto.copy()
        df_tovorna_vozila = df_avto.copy()
        df_avtobusi = df_avto.copy()
        df_tuji_avti = df_avto.copy()

        # 3. Get annual value from podatki
        #annual_total = podatki.loc['Elektrika v prometu', year]
        annual_total_avti = podatki.loc['Osebni avtomobili - domači', year]  ##### odvisno kater promet hočemo
        annual_total_ziznice = podatki.loc['Ostalo (žičnice)', year]
        annual_total_tovorni_vlaki =  podatki.loc['Tovorni vlaki', year]
        annual_total_potniski_vlaki = podatki.loc["Potniški vlaki", year]
        annual_total_tovorna_vozila = podatki.loc["Lahka tovorna vozila", year] + podatki.loc['Težka tovorna vozila', year]+podatki.loc["Vlačilci - domači", year] + podatki.loc['Vlačilci - tuji', year]
        annual_total_avtobusi = podatki.loc["Avtobusi", year]
        annual_total_tuji_avti = podatki.loc["Osebni avtomobili - tuji", year]

        ############## DOMAČI avtomobili
        daily_flags = df_avto['Dela prost dan'].groupby(df_avto.index.date).first()
        # Count days
        num_work_days = (daily_flags == 0).sum()
        num_weekend_days = (daily_flags == 1).sum()
        annual_weekend_day_avti = annual_total_avti*procent_vikend/100/num_weekend_days*1000  #v MWh plus procenti, za en dan poraba
        annual_work_day_avti = annual_total_avti*procent_delavnik/100/num_work_days*1000
        # 6. Compute hourly values for weekdays
        work_avti_00_06 = (annual_work_day_avti * procent_work_avti_00_06/100) / (6)  
        work_avti_06_10 = (annual_work_day_avti * procent_work_avti_06_10/100) / (3)  
        work_avti_10_18 = (annual_work_day_avti * procent_work_avti_10_18/100) / (6)  
        work_avti_18_22 = (annual_work_day_avti * procent_work_avti_18_22/100) / (5)
        work_avti_22_00 = (annual_work_day_avti * procent_work_avti_22_00/100) / (4)
        # 7. Compute hourly values for weekends
        weekend_avti_00_06 = (annual_weekend_day_avti * procent_weekend_avti_00_06/100) / (6)  
        weekend_avti_06_10 = (annual_weekend_day_avti * procent_weekend_avti_06_10/100) / (3)  
        weekend_avti_10_18 = (annual_weekend_day_avti * procent_weekend_avti_10_18/100) / (6)  
        weekend_avti_18_22 = (annual_weekend_day_avti * procent_weekend_avti_18_22/100) / (5)
        weekend_avti_22_00 = (annual_weekend_day_avti * procent_weekend_avti_22_00/100) / (4)
        # 7. Assign value based on hour
        def assign_value_domaci(ts):
            hour = ts.hour
            day_type = df_avto.loc[ts, 'Dela prost dan']  # 0 = workday, 1 = weekend/holiday

            if day_type == 0:  # Workday
                if 0 <= hour < 6:
                    return work_avti_00_06
                elif 6 <= hour < 10:
                    return work_avti_06_10
                elif 10 <= hour < 18:
                    return work_avti_10_18
                elif 18 <= hour < 22:
                    return work_avti_18_22
                elif 22 <= hour < 24:
                    return work_avti_22_00
                else:
                    return 0
            else:  # Weekend or holiday
                if 0 <= hour < 6:
                    return weekend_avti_00_06
                elif 6 <= hour < 10:
                    return weekend_avti_06_10
                elif 10 <= hour < 18:
                    return weekend_avti_10_18
                elif 18 <= hour < 22:
                    return weekend_avti_18_22
                elif 22 <= hour < 24:
                    return weekend_avti_22_00
                else:
                    return 0

        df_avto['profil'] = df_avto.index.to_series().apply(assign_value_domaci)
        # 8. Save to dictionary
        df_avto = df_avto.drop(["Day", "Dela prost dan"],axis=1)
        df_avto.index.name = "Časovna značka"
        time_series_per_year_avto_list.append(df_avto)

        ############# ŽIČNICE
        daily_total_ziznice = annual_total_ziznice*1000 / num_days   # damo v MWh

        night_value_ziznice = 0
        day_value_ziznice   = daily_total_ziznice / (ura_vecer_ž-ura_jutro_ž)  # day hours

        def assign_value_zicnica(hour):
            return night_value_ziznice if hour >= ura_vecer_ž or hour < ura_jutro_ž else day_value_ziznice

        df_zicnice['profil'] = df_zicnice.index.hour.map(assign_value_zicnica)
        df_zicnice = df_zicnice.drop(["Day", "Dela prost dan"],axis=1)
        df_zicnice.index.name = "Časovna značka"
        time_series_per_year_zicnice_list.append(df_zicnice)

        ################ VLAKI
        daily_total_potniski = annual_total_potniski_vlaki*1000 / num_days   # damo v MWh
        daily_total_tovorni = annual_total_tovorni_vlaki*1000 / num_days

        night_value_vlaki = daily_total_tovorni * procent_tovorni_vlak_noc/100 /(24-ura_vecer_vlaki+ura_jutro_vlaki)
        day_value_vlaki   = daily_total_tovorni * procent_tovorni_vlak_dan/100 /(ura_vecer_vlaki-ura_jutro_vlaki) + daily_total_potniski/(ura_vecer_vlaki-ura_jutro_vlaki) # day hours

        def assign_value_vlaki(hour):
            return night_value_vlaki if hour >= ura_vecer_vlaki or hour < ura_jutro_vlaki else day_value_vlaki

        df_vlaki['profil'] = df_vlaki.index.hour.map(assign_value_vlaki)
        df_vlaki = df_vlaki.drop(["Day", "Dela prost dan"],axis=1)
        df_vlaki.index.name = "Časovna značka"
        time_series_per_year_vlaki_list.append(df_vlaki)

        ############### TOVORNA VOZILA
        daily_flags = df_tovorna_vozila['Dela prost dan'].groupby(df_tovorna_vozila.index.date).first()
        # Count days
        num_work_days_tovorna = (daily_flags == 0).sum()
        num_weekend_days_tovorna = (daily_flags == 1).sum()
        annual_weekend_day_tovorna = annual_total_tovorna_vozila*procent_vikend_tovorna/100/num_weekend_days_tovorna*1000  #v MWh plus procenti, za en dan poraba
        annual_work_day_tovorna = annual_total_tovorna_vozila*procent_delavnik_tovorna/100/num_work_days_tovorna*1000
        # 6. Compute hourly values for workdays
        work_tovorni_00_06 = (annual_work_day_tovorna * procent_del_00_06/100) / (6)  
        work_tovorni_06_09 = (annual_work_day_tovorna * procent_del_06_09/100) / (3)  
        work_tovorni_09_17 = (annual_work_day_tovorna * procent_del_09_17/100) / (8)  
        work_tovorni_17_20 = (annual_work_day_tovorna * procent_del_17_20/100) / (3)
        work_tovorni_20_00 = (annual_work_day_tovorna * procent_del_20_00/100) / (4)
        # 7. Compute hourly values for weekends
        night_value_weekend_tovorni = (annual_weekend_day_tovorna * procent_cez_noc_vik_tovorna/100) / (24-ura_noc_vik_tovorna+ura_jutro_vik_tovorna)  # night hours
        day_value_weekend_tovorni   = (annual_weekend_day_tovorna * procent_cez_dan_vik_tovorna/100) / (ura_noc_vik_tovorna-ura_jutro_vik_tovorna)  

        # 7. Assign value based on hour
        def assign_value_tovorna(ts):
            hour = ts.hour
            day_type = df_tovorna_vozila.loc[ts, 'Dela prost dan']  # 0 = workday, 1 = weekend/free

            if day_type == 0:  # Workday
                if 0 <= hour < 6:
                    return work_tovorni_00_06
                elif 6 <= hour < 9:
                    return work_tovorni_06_09  # Note: your percent is 06-09 but variable says 06_10
                elif 9 <= hour < 17:
                    return work_tovorni_09_17  # variable says 09_17, you named 10_14 — please confirm ranges
                elif 17 <= hour < 20:
                    return work_tovorni_17_20  # variable says 17_20, but named 14_22 — check ranges carefully
                elif 20 <= hour < 24:
                    return work_tovorni_20_00
                else:
                    return 0
            else:  # Weekend or holiday
                if hour >= ura_noc_vik_tovorna or hour < ura_jutro_vik_tovorna:
                    return night_value_weekend_tovorni
                else:
                    return day_value_weekend_tovorni

        df_tovorna_vozila['profil'] = df_tovorna_vozila.index.to_series().apply(assign_value_tovorna)
        # 8. Save to dictionary
        df_tovorna_vozila = df_tovorna_vozila.drop(["Day", "Dela prost dan"],axis=1)
        df_tovorna_vozila.index.name = "Časovna značka"
        time_series_per_year_tovorna_vozila_list.append(df_tovorna_vozila)

        ######################### AVTOBUSI
        daily_flags = df_avtobusi['Dela prost dan'].groupby(df_avtobusi.index.date).first()
        # Count days
        num_work_days_avtobusi = (daily_flags == 0).sum()
        num_weekend_days_avtobusi = (daily_flags == 1).sum()
        annual_weekend_day_avtobusi = annual_total_avtobusi*procent_vikend_avtobusi/100/num_weekend_days_avtobusi*1000  #v MWh plus procenti, za en dan poraba
        annual_work_day_avtobusi = annual_total_avtobusi*procent_delavnik_avtobusi/100/num_work_days_avtobusi*1000
        # 6. Compute hourly values for workdays
        work_avtobusi_00_06 = (annual_work_day_avtobusi * procent_avtobusi_00_06/100) / (6)  
        work_avtobusi_06_09 = (annual_work_day_avtobusi * procent_avtobusi_06_09/100) / (3)  
        work_avtobusi_09_15 = (annual_work_day_avtobusi * procent_avtobusi_09_15/100) / (6)  
        work_avtobusi_15_20 = (annual_work_day_avtobusi * procent_avtobusi_15_20/100) / (5)
        work_avtobusi_20_00 = (annual_work_day_avtobusi * procent_avtobusi_20_00/100) / (4)
        # 7. Compute hourly values for weekends
        weekend_avtobusi_00_06 = (annual_weekend_day_avtobusi * procent_avtobusi_00_06/100) / (6)  
        weekend_avtobusi_06_09 = (annual_weekend_day_avtobusi * procent_avtobusi_06_09/100) / (3)  
        weekend_avtobusi_09_15 = (annual_weekend_day_avtobusi * procent_avtobusi_09_15/100) / (6)  
        weekend_avtobusi_15_20 = (annual_weekend_day_avtobusi * procent_avtobusi_15_20/100) / (5)
        weekend_avtobusi_20_00 = (annual_weekend_day_avtobusi * procent_avtobusi_20_00/100) / (4)
        # 7. Assign value based on hour
        def assign_value_avtobusi(ts):
            hour = ts.hour
            day_type = df_avtobusi.loc[ts, 'Dela prost dan']  # 0 = workday, 1 = weekend/holiday

            if day_type == 0:  # Workday
                if 0 <= hour < 6:
                    return work_avtobusi_00_06
                elif 6 <= hour < 9:
                    return work_avtobusi_06_09
                elif 9 <= hour < 15:
                    return work_avtobusi_09_15
                elif 15 <= hour < 20:
                    return work_avtobusi_15_20
                elif 20 <= hour < 24:
                    return work_avtobusi_20_00
                else:
                    return 0
            else:  # Weekend or holiday
                if 0 <= hour < 6:
                    return weekend_avtobusi_00_06
                elif 6 <= hour < 9:
                    return weekend_avtobusi_06_09
                elif 9 <= hour < 15:
                    return weekend_avtobusi_09_15
                elif 15 <= hour < 20:
                    return weekend_avtobusi_15_20
                elif 20 <= hour < 24:
                    return weekend_avtobusi_20_00
                else:
                    return 0

        df_avtobusi['profil'] = df_avtobusi.index.to_series().apply(assign_value_avtobusi)
        # 8. Save to dictionary
        df_avtobusi = df_avtobusi.drop(["Day", "Dela prost dan"],axis=1)
        df_avtobusi.index.name = "Časovna značka"
        time_series_per_year_avtobusi_list.append(df_avtobusi)

        ################## AVTOMOBILI TUJI
        df_tuji_avti['season'] = df_tuji_avti.index.to_series().apply(get_season)
        df_summer = df_tuji_avti[df_tuji_avti['season'] == 'summer']
        daily_flags_summer = df_summer['Dela prost dan'].groupby(df_summer.index.date).first()
        df_winter = df_tuji_avti[df_tuji_avti['season'] == 'winter']
        daily_flags_winter = df_winter['Dela prost dan'].groupby(df_winter.index.date).first()
        df_other = df_tuji_avti[df_tuji_avti['season'] == 'autumn_spring']
        daily_flags_other = df_other['Dela prost dan'].groupby(df_other.index.date).first()
        # Count days
        num_work_days_summer = (daily_flags_summer == 0).sum()
        num_weekend_days_summer = (daily_flags_summer == 1).sum()
        num_work_days_winter = (daily_flags_winter == 0).sum()
        num_weekend_days_winter = (daily_flags_winter == 1).sum()
        num_work_days_other = (daily_flags_other == 0).sum()
        num_weekend_days_other = (daily_flags_other == 1).sum()

        summer_total = annual_total_tuji_avti*procent_poletje/100
        winter_total = annual_total_tuji_avti*procent_zima/100
        other_total = annual_total_tuji_avti*procent_jesen_pomald/100

        summer_weekend_day = summer_total*procent_tuji_vikend/100/num_weekend_days_summer*1000  #v MWh plus procenti, za en dan poraba
        summer_work_day = summer_total*procent_tuji_delavnik/100/num_work_days_summer*1000

        winter_weekend_day = winter_total*procent_tuji_vikend/100/num_weekend_days_winter*1000  #v MWh plus procenti, za en dan poraba
        winter_work_day = winter_total*procent_tuji_delavnik/100/num_work_days_winter*1000

        other_weekend_day = other_total*procent_tuji_vikend/100/num_weekend_days_other*1000  #v MWh plus procenti, za en dan poraba
        other_work_day = other_total*procent_tuji_delavnik/100/num_work_days_other*1000


        # 6. Compute hourly values for summer
        work_summer_00_06 = (summer_work_day * procent_tuji_00_06/100) / (6)  
        work_summer_06_10 = (summer_work_day * procent_tuji_06_10/100) / (4)  
        work_summer_10_14 = (summer_work_day * procent_tuji_10_14/100) / (4)  
        work_summer_14_22 = (summer_work_day * procent_tuji_14_22/100) / (8)
        work_summer_22_00 = (summer_work_day * procent_tuji_22_00/100) / (2)
        weekend_summer_00_06 = (summer_weekend_day * procent_tuji_00_06/100) / (6)  
        weekend_summer_06_10 = (summer_weekend_day * procent_tuji_06_10/100) / (4) 
        weekend_summer_10_14 = (summer_weekend_day * procent_tuji_10_14/100) / (4) 
        weekend_summer_14_22 = (summer_weekend_day * procent_tuji_14_22/100) / (8) 
        weekend_summer_22_00 = (summer_weekend_day * procent_tuji_22_00/100) / (2) 
        # 7. Compute hourly values for winter
        work_winter_00_06 = (winter_work_day * procent_tuji_00_06/100) / (6)  
        work_winter_06_10 = (winter_work_day * procent_tuji_06_10/100) / (4)  
        work_winter_10_14 = (winter_work_day * procent_tuji_10_14/100) / (4)  
        work_winter_14_22 = (winter_work_day * procent_tuji_14_22/100) / (8)
        work_winter_22_00 = (winter_work_day * procent_tuji_22_00/100) / (2)
        weekend_winter_00_06 = (winter_weekend_day * procent_tuji_00_06/100) / (6)  
        weekend_winter_06_10 = (winter_weekend_day * procent_tuji_06_10/100) / (4) 
        weekend_winter_10_14 = (winter_weekend_day * procent_tuji_10_14/100) / (4) 
        weekend_winter_14_22 = (winter_weekend_day * procent_tuji_14_22/100) / (8) 
        weekend_winter_22_00 = (winter_weekend_day * procent_tuji_22_00/100) / (2) 
        # 8. Compute hourly values for other
        work_other_00_06 = (other_work_day * procent_tuji_00_06/100) / (6)  
        work_other_06_10 = (other_work_day * procent_tuji_06_10/100) / (4)  
        work_other_10_14 = (other_work_day * procent_tuji_10_14/100) / (4)  
        work_other_14_22 = (other_work_day * procent_tuji_14_22/100) / (8)
        work_other_22_00 = (other_work_day * procent_tuji_22_00/100) / (2)
        weekend_other_00_06 = (other_weekend_day * procent_tuji_00_06/100) / (6)  
        weekend_other_06_10 = (other_weekend_day * procent_tuji_06_10/100) / (4) 
        weekend_other_10_14 = (other_weekend_day * procent_tuji_10_14/100) / (4) 
        weekend_other_14_22 = (other_weekend_day * procent_tuji_14_22/100) / (8) 
        weekend_other_22_00 = (other_weekend_day * procent_tuji_22_00/100) / (2)

        # 7. Assign value based on hour
        def assign_value_tuji(ts):
            hour = ts.hour
            day_type = df_tuji_avti.loc[ts, 'Dela prost dan']  # 0 = workday, 1 = weekend/free
            season = df_tuji_avti.loc[ts, 'season']

            # Define which hourly values to use based on season and day_type
            if season == 'summer':
                if day_type == 0:  # workday
                    if 0 <= hour < 6:
                        return work_summer_00_06
                    elif 6 <= hour < 10:
                        return work_summer_06_10
                    elif 10 <= hour < 14:
                        return work_summer_10_14
                    elif 14 <= hour < 22:
                        return work_summer_14_22
                    elif 22 <= hour < 24:
                        return work_summer_22_00
                else:  # weekend
                    if 0 <= hour < 6:
                        return weekend_summer_00_06
                    elif 6 <= hour < 10:
                        return weekend_summer_06_10
                    elif 10 <= hour < 14:
                        return weekend_summer_10_14
                    elif 14 <= hour < 22:
                        return weekend_summer_14_22
                    elif 22 <= hour < 24:
                        return weekend_summer_22_00

            elif season == 'winter':
                if day_type == 0:  # workday
                    if 0 <= hour < 6:
                        return work_winter_00_06
                    elif 6 <= hour < 10:
                        return work_winter_06_10
                    elif 10 <= hour < 14:
                        return work_winter_10_14
                    elif 14 <= hour < 22:
                        return work_winter_14_22
                    elif 22 <= hour < 24:
                        return work_winter_22_00
                else:  # weekend
                    if 0 <= hour < 6:
                        return weekend_winter_00_06
                    elif 6 <= hour < 10:
                        return weekend_winter_06_10
                    elif 10 <= hour < 14:
                        return weekend_winter_10_14
                    elif 14 <= hour < 22:
                        return weekend_winter_14_22
                    elif 22 <= hour < 24:
                        return weekend_winter_22_00

            else:  # autumn_spring (other)
                if day_type == 0:  # workday
                    if 0 <= hour < 6:
                        return work_other_00_06
                    elif 6 <= hour < 10:
                        return work_other_06_10
                    elif 10 <= hour < 14:
                        return work_other_10_14
                    elif 14 <= hour < 22:
                        return work_other_14_22
                    elif 22 <= hour < 24:
                        return work_other_22_00
                else:  # weekend
                    if 0 <= hour < 6:
                        return weekend_other_00_06
                    elif 6 <= hour < 10:
                        return weekend_other_06_10
                    elif 10 <= hour < 14:
                        return weekend_other_10_14
                    elif 14 <= hour < 22:
                        return weekend_other_14_22
                    elif 22 <= hour < 24:
                        return weekend_other_22_00

            # Fallback if none matched
            return 0


        df_tuji_avti['profil'] = df_tuji_avti.index.to_series().apply(assign_value_tuji)
        # 8. Save to dictionary
        df_tuji_avti = df_tuji_avti.drop(["Day", "season",  "Dela prost dan"],axis=1)
        df_tuji_avti.index.name = "Časovna značka"
        time_series_per_year_tuji_avti_list.append(df_tuji_avti)

    ####################### DEFINIRANJE PROFILOV
    time_series_per_year_avto = pd.concat(time_series_per_year_avto_list)
    time_series_per_year_zicnice = pd.concat(time_series_per_year_zicnice_list)
    time_series_per_year_vlaki = pd.concat(time_series_per_year_vlaki_list)
    time_series_per_year_tovorna_vozila = pd.concat(time_series_per_year_tovorna_vozila_list)
    time_series_per_year_avtobusi = pd.concat(time_series_per_year_avtobusi_list)
    time_series_per_year_tuji_avti = pd.concat(time_series_per_year_tuji_avti_list)

    combined_profiles = time_series_per_year_avto + time_series_per_year_zicnice + time_series_per_year_vlaki + time_series_per_year_tovorna_vozila + time_series_per_year_avtobusi + time_series_per_year_tuji_avti
    combined_profiles.index.name = "Časovna značka"



    return combined_profiles








