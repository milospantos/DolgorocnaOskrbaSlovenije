import pandas as pd
import numpy as np
import os


PATH=os.path.abspath(os.getcwd())

#izgled koncne datoteke
datoteka = "vhodni_podatki_za_model2.xlsx"
datoteka_out = "vhodni_podatki_za_model2.xlsx"
podatki = pd.read_excel(PATH +"\\"+ datoteka, sheet_name=None)

#podatki o  elektrarnah
datoteka2 = "SeznamElektrarn_vse_mk_nov.xlsx"
elektrarne = pd.read_excel(PATH +"\\"+ datoteka2)


###### DODAJANJE HIDRO
podatki_hidro_df = elektrarne.loc[(elektrarne["Tehnologija"]== "hydr")]

rows_hydro = []
for elektrarna in range(len(podatki_hidro_df)):
    name = podatki_hidro_df.iloc[elektrarna]["Ime"]
    type = podatki_hidro_df.iloc[elektrarna]["Tehnologija"]
    capital_cost = podatki_hidro_df.iloc[elektrarna]["CAPEX (EUR/MW)"]
    marginal_cost = podatki_hidro_df.iloc[elektrarna]["Variabilni obratovani stroški (EUR/MWh)"]
    active = True
    build_year = podatki_hidro_df.iloc[elektrarna]["Leto izgradnje"]
    life_time = podatki_hidro_df.iloc[elektrarna]["Življenjska doba"]
    p_nom = podatki_hidro_df.iloc[elektrarna]["Pmax (MW)"]
    eff = 1
    ramp_up_limit = podatki_hidro_df.iloc[elektrarna]["Hitrost spremembe moči navzgor (MW/min)"]/p_nom*60
    ramp_down_limit = podatki_hidro_df.iloc[elektrarna]["Hitrost spremembe moči navzdol (MW/min)"]/p_nom*60
    ramp_limit_start = 1
    ramp_limit_shutdown = 1
    fuel = "hydro"
    co2 = 0
    country = "Slovenia"
    x = None
    y = None
    commitable = True
    min_up_time = podatki_hidro_df.iloc[elektrarna]["Minimalni čas obratovanja (min)"]
    min_down_time = 0
    startup_cost = podatki_hidro_df.iloc[elektrarna]["Zagonski strošek (EUR/MW ali podobno)"]
    shutdown_cost = podatki_hidro_df.iloc[elektrarna]["Zaustavitveni strošek (EUR/MW ali podobno)"]
    standby_cost = 0
    inflow_source = podatki_hidro_df.iloc[elektrarna]["Porečje"]
    H = podatki_hidro_df.iloc[elektrarna]["Neto padec (m)"]
    V_min = podatki_hidro_df.iloc[elektrarna]["Minimalni volumen bazena (m3)"]
    V_max = podatki_hidro_df.iloc[elektrarna]["Maksimalni volumen bazena (m3)"]
    bio_min = podatki_hidro_df.iloc[elektrarna]["Biološki minimum (m3/s)"]
    skupina = podatki_hidro_df.iloc[elektrarna]["Skupina"]
    obstojeca_nova = podatki_hidro_df.iloc[elektrarna]["Obstoječa (O) ali nova (N) proizvodnja"]

    new_row = {"name":name, "type":type, "capital_cost [EUR/MW]":capital_cost, "marginal_cost [EUR/MWh]":marginal_cost, "active":active, "build_year [year]":build_year,
               "lifetime [years]":life_time, "p_nom [MW]":p_nom, "efficiency [p.u.]":eff, 	"ramp_limit_up [p.u./h]":ramp_up_limit,	"ramp_limit_down [p.u./h]":ramp_down_limit,
                   	"ramp_limit_start_up [p.u./h]":ramp_limit_start,	"ramp_limit_shut_down [p.u./h]":ramp_limit_shutdown,	"fuel":fuel,	"co2_emissions [t CO2/MWh]":co2,	"country":country,	"x (coord) [decimal deg]":x,	"y (coord) [decimal deg]":y,	"committable":commitable,
                    "min_up_time [h]":min_up_time,	"min_down_time [h]":min_down_time,	"startup_cost [EUR]":startup_cost,	"shutdown_cost [EUR]":shutdown_cost,	"stand_by_cost [EUR/MW/h]":standby_cost,	"inflow_source":inflow_source,	"H [m]":H,	"v_min [m3]":V_min,	"v_max [m3]":V_max,	"bio_min [m3/s]":bio_min, "skupina":skupina, "Obstoječa/nova":obstojeca_nova}
    rows_hydro.append(new_row)

podatki["Hydro"] = pd.DataFrame(rows_hydro)


###### DODAJANJE TERMO in GAS
podatki_termo_df = elektrarne.loc[(elektrarne["Tehnologija"]== "coal") | (elektrarne["Tehnologija"]== "gas")]

rows_termo = []
for elektrarna in range(len(podatki_termo_df)):
    name = podatki_termo_df.iloc[elektrarna]["Ime"]
    type = podatki_termo_df.iloc[elektrarna]["Tehnologija"]
    capital_cost = podatki_termo_df.iloc[elektrarna]["CAPEX (EUR/MW)"]
    marginal_cost = podatki_termo_df.iloc[elektrarna]["Variabilni obratovani stroški (EUR/MWh)"]
    active = True
    build_year = podatki_termo_df.iloc[elektrarna]["Leto izgradnje"]
    life_time = podatki_termo_df.iloc[elektrarna]["Življenjska doba"]
    p_nom = podatki_termo_df.iloc[elektrarna]["Pmax (MW)"]
    eff = podatki_termo_df.iloc[elektrarna]["Ocenjen CF (0-1)"]
    ramp_up_limit = podatki_termo_df.iloc[elektrarna]["Hitrost spremembe moči navzgor (MW/min)"]/p_nom*60
    ramp_down_limit = podatki_termo_df.iloc[elektrarna]["Hitrost spremembe moči navzdol (MW/min)"]/p_nom*60
    ramp_limit_start = 1
    ramp_limit_shutdown = 1
    fuel = type
    co2 = 999999
    country = "Slovenia"
    x = None
    y = None
    commitable = True
    min_up_time = podatki_termo_df.iloc[elektrarna]["Minimalni čas obratovanja (min)"]
    min_down_time = 0
    startup_cost = podatki_termo_df.iloc[elektrarna]["Zagonski strošek (EUR/MW ali podobno)"]
    shutdown_cost = podatki_termo_df.iloc[elektrarna]["Zaustavitveni strošek (EUR/MW ali podobno)"]
    standby_cost = 0
    skupina = podatki_termo_df.iloc[elektrarna]["Skupina"]
    obstojeca_nova = podatki_termo_df.iloc[elektrarna]["Obstoječa (O) ali nova (N) proizvodnja"]

    new_row = {"name":name, "type":type, "capital_cost [EUR/MW]":capital_cost, "marginal_cost [EUR/MWh]":marginal_cost, "active":active, "build_year [year]":build_year,
               "lifetime [years]":life_time, "p_nom [MW]":p_nom, "efficiency [p.u.]":eff, 	"ramp_limit_up [p.u./h]":ramp_up_limit,	"ramp_limit_down [p.u./h]":ramp_down_limit,
                   	"ramp_limit_start_up [p.u./h]":ramp_limit_start,	"ramp_limit_shut_down [p.u./h]":ramp_limit_shutdown,	"fuel":fuel,	"co2_emissions [t CO2/MWh]":co2,	"country":country,	"x (coord) [decimal deg]":x,	"y (coord) [decimal deg]":y,	"committable":commitable,
                    "min_up_time [h]":min_up_time,	"min_down_time [h]":min_down_time,	"startup_cost [EUR]":startup_cost,	"shutdown_cost [EUR]":shutdown_cost,	"stand_by_cost [EUR/MW/h]":standby_cost, "skupina":skupina, "Obstoječa/nova":obstojeca_nova}
    rows_termo.append(new_row)

podatki["Thermal"] = pd.DataFrame(rows_termo)

##### DODAJANJE NUC
podatki_nuc_df = elektrarne.loc[(elektrarne["Tehnologija"]== "nuc")]

rows_nuc = []
for elektrarna in range(len(podatki_nuc_df)):
    name = podatki_nuc_df.iloc[elektrarna]["Ime"]
    type = podatki_nuc_df.iloc[elektrarna]["Tehnologija"]
    capital_cost = podatki_nuc_df.iloc[elektrarna]["CAPEX (EUR/MW)"]
    marginal_cost = podatki_nuc_df.iloc[elektrarna]["Variabilni obratovani stroški (EUR/MWh)"]
    active = True
    build_year = podatki_nuc_df.iloc[elektrarna]["Leto izgradnje"]
    life_time = podatki_nuc_df.iloc[elektrarna]["Življenjska doba"]
    p_nom = podatki_nuc_df.iloc[elektrarna]["Pmax (MW)"]
    eff = podatki_nuc_df.iloc[elektrarna]["Ocenjen CF (0-1)"]
    ramp_up_limit = podatki_nuc_df.iloc[elektrarna]["Hitrost spremembe moči navzgor (MW/min)"]/p_nom*60
    ramp_down_limit = podatki_nuc_df.iloc[elektrarna]["Hitrost spremembe moči navzdol (MW/min)"]/p_nom*60
    ramp_limit_start = 1
    ramp_limit_shutdown = 1
    fuel = type
    co2 = 999999
    country = "Slovenia"
    x = None
    y = None
    commitable = True
    min_up_time = podatki_nuc_df.iloc[elektrarna]["Minimalni čas obratovanja (min)"]
    min_down_time = 0
    startup_cost = podatki_nuc_df.iloc[elektrarna]["Zagonski strošek (EUR/MW ali podobno)"]
    shutdown_cost = podatki_nuc_df.iloc[elektrarna]["Zaustavitveni strošek (EUR/MW ali podobno)"]
    standby_cost = 0
    skupina = podatki_nuc_df.iloc[elektrarna]["Skupina"]
    obstojeca_nova = podatki_nuc_df.iloc[elektrarna]["Obstoječa (O) ali nova (N) proizvodnja"]

    new_row = {"name":name, "type":type, "capital_cost [EUR/MW]":capital_cost, "marginal_cost [EUR/MWh]":marginal_cost, "active":active, "build_year [year]":build_year,
               "lifetime [years]":life_time, "p_nom [MW]":p_nom, "efficiency [p.u.]":eff, 	"ramp_limit_up [p.u./h]":ramp_up_limit,	"ramp_limit_down [p.u./h]":ramp_down_limit,
                   	"ramp_limit_start_up [p.u./h]":ramp_limit_start,	"ramp_limit_shut_down [p.u./h]":ramp_limit_shutdown,	"fuel":fuel,	"co2_emissions [t CO2/MWh]":co2,	"country":country,	"x (coord) [decimal deg]":x,	"y (coord) [decimal deg]":y,	"committable":commitable,
                    "min_up_time [h]":min_up_time,	"min_down_time [h]":min_down_time,	"startup_cost [EUR]":startup_cost,	"shutdown_cost [EUR]":shutdown_cost,	"stand_by_cost [EUR/MW/h]":standby_cost, "skupina":skupina, "Obstoječa/nova":obstojeca_nova}
    rows_nuc.append(new_row)

podatki["Nuclear"] = pd.DataFrame(rows_nuc)

##### DODAJANJE BHEE
podatki_batt_df = elektrarne.loc[(elektrarne["Tehnologija"]== "stor")]

rows_batt = []
for elektrarna in range(len(podatki_batt_df)):
    name = podatki_batt_df.iloc[elektrarna]["Ime"]
    type = podatki_batt_df.iloc[elektrarna]["Tehnologija"]
    capital_cost = podatki_batt_df.iloc[elektrarna]["CAPEX (EUR/MW)"]
    marginal_cost = podatki_batt_df.iloc[elektrarna]["Variabilni obratovani stroški (EUR/MWh)"]
    active = True
    build_year = podatki_batt_df.iloc[elektrarna]["Leto izgradnje"]
    life_time = podatki_batt_df.iloc[elektrarna]["Življenjska doba"]
    e_nom = podatki_batt_df.iloc[elektrarna]["Pmax (MW)"]*2
    p_nom = podatki_batt_df.iloc[elektrarna]["Pmax (MW)"]
    charging_eff = 0.9
    disscharging_eff = 0.9
    standing_loss = 0.0001
    country = "Slovenia"
    x = None
    y = None
    skupina = podatki_batt_df.iloc[elektrarna]["Skupina"]
    obstojeca_nova = podatki_batt_df.iloc[elektrarna]["Obstoječa (O) ali nova (N) proizvodnja"]

    new_row = {"name":name, "type":type, "capital_cost [EUR/MW]":capital_cost, "marginal_cost [EUR/MWh]":marginal_cost, "active":active, "build_year [year]":build_year,
               "lifetime [years]":life_time, "e_nom [MWh]":e_nom, "p_nom [MW]":p_nom, "charging_efficiency [p.u.]":charging_eff, 	"discharging_efficiency [p.u.]":disscharging_eff, "standing_loss [p.u./h]":standing_loss,
                 "country":country,	"x (coord) [decimal deg]":x,	"y (coord) [decimal deg]":y, "skupina":skupina, "Obstoječa/nova":obstojeca_nova}
    rows_batt.append(new_row)

podatki["Batt"] = pd.DataFrame(rows_batt)


###### DODAJANJE PUMPED HYDRO
podatki_pump_df = elektrarne.loc[(elektrarne["Tehnologija"]== "pump")]

rows_pump = []
for elektrarna in range(len(podatki_pump_df)):
    name = podatki_pump_df.iloc[elektrarna]["Ime"]
    type = podatki_pump_df.iloc[elektrarna]["Tehnologija"]
    capital_cost = podatki_pump_df.iloc[elektrarna]["CAPEX (EUR/MW)"]
    marginal_cost = podatki_pump_df.iloc[elektrarna]["Variabilni obratovani stroški (EUR/MWh)"]
    active = True
    build_year = podatki_pump_df.iloc[elektrarna]["Leto izgradnje"]
    life_time = podatki_pump_df.iloc[elektrarna]["Življenjska doba"]
    p_nom = podatki_pump_df.iloc[elektrarna]["Pmax (MW)"]
    eff = 1
    ramp_up_limit = podatki_pump_df.iloc[elektrarna]["Hitrost spremembe moči navzgor (MW/min)"]/p_nom*60
    ramp_down_limit = podatki_pump_df.iloc[elektrarna]["Hitrost spremembe moči navzdol (MW/min)"]/p_nom*60
    ramp_limit_start = 1
    ramp_limit_shutdown = 1
    fuel = "hydro"
    co2 = 0
    country = "Slovenia"
    x = None
    y = None
    commitable = True
    min_up_time = podatki_pump_df.iloc[elektrarna]["Minimalni čas obratovanja (min)"]
    min_down_time = 0
    startup_cost = podatki_pump_df.iloc[elektrarna]["Zagonski strošek (EUR/MW ali podobno)"]
    shutdown_cost = podatki_pump_df.iloc[elektrarna]["Zaustavitveni strošek (EUR/MW ali podobno)"]
    standby_cost = 0
    inflow_source = podatki_pump_df.iloc[elektrarna]["Porečje"]
    H = podatki_pump_df.iloc[elektrarna]["Neto padec (m)"]
    V_min = podatki_pump_df.iloc[elektrarna]["Minimalni volumen bazena (m3)"]
    V_max = podatki_pump_df.iloc[elektrarna]["Maksimalni volumen bazena (m3)"]
    bio_min = podatki_pump_df.iloc[elektrarna]["Biološki minimum (m3/s)"]
    skupina = podatki_pump_df.iloc[elektrarna]["Skupina"]
    obstojeca_nova = podatki_pump_df.iloc[elektrarna]["Obstoječa (O) ali nova (N) proizvodnja"]

    new_row = {"name":name, "type":type, "capital_cost [EUR/MW]":capital_cost, "marginal_cost [EUR/MWh]":marginal_cost, "active":active, "build_year [year]":build_year,
               "lifetime [years]":life_time, "p_nom [MW]":p_nom, "efficiency [p.u.]":eff, 	"ramp_limit_up [p.u./h]":ramp_up_limit,	"ramp_limit_down [p.u./h]":ramp_down_limit,
                   	"ramp_limit_start_up [p.u./h]":ramp_limit_start,	"ramp_limit_shut_down [p.u./h]":ramp_limit_shutdown,	"fuel":fuel,	"co2_emissions [t CO2/MWh]":co2,	"country":country,	"x (coord) [decimal deg]":x,	"y (coord) [decimal deg]":y,	"committable":commitable,
                    "min_up_time [h]":min_up_time,	"min_down_time [h]":min_down_time,	"startup_cost [EUR]":startup_cost,	"shutdown_cost [EUR]":shutdown_cost,	"stand_by_cost [EUR/MW/h]":standby_cost,	"inflow_source":inflow_source,	"H [m]":H,	"v_min [m3]":V_min,	"v_max [m3]":V_max,	"bio_min [m3/s]":bio_min, "skupina":skupina, "Obstoječa/nova":obstojeca_nova}
    rows_pump.append(new_row)

podatki["Pumped_Hydro"] = pd.DataFrame(rows_pump)

#podatki["HydroTimeSeries"] = podatki["HydroTimeSeries"].iloc[3]

#podatki o  elektrarnah
# datoteka3 = "sava_pred_radovljico_hourly_2025-2050.xlsx"
# sava_pred_radovljico = pd.read_excel(PATH +"\\"+ datoteka3)

# datoteka4 = "sava_okroglo_hourly_2025-2050.xlsx"
# sava_okroglo = pd.read_excel(PATH +"\\"+ datoteka4)

# datoteka5 = "sava_pred_catez_hourly_2025-2050.xlsx"
# sava_pred_catezem = pd.read_excel(PATH +"\\"+ datoteka5)

# datoteka6 = "sava_catez_hourly_2025-2050.xlsx"
# sava_catez = pd.read_excel(PATH +"\\"+ datoteka6)

# datoteka7 = "drava_hourly_2025-2050.xlsx"
# drava = pd.read_excel(PATH +"\\"+ datoteka7)

# datoteka8 = "soca_hourly_2025-2050.xlsx"
# soca = pd.read_excel(PATH +"\\"+ datoteka8)

# # Get maximum required length
# max_len = max(len(df) for df in [
#     drava, soca, sava_pred_radovljico, sava_okroglo, sava_pred_catezem, sava_catez
# ])

# # Expand the dataframe if needed
# rows_needed = 2 + max_len  # 2 header rows + data
# current_rows = len(podatki["HydroTimeSeries"])

# if current_rows < rows_needed:
#     missing_rows = rows_needed - current_rows
#     additional_rows = pd.DataFrame(index=range(missing_rows), columns=podatki["HydroTimeSeries"].columns)
#     podatki["HydroTimeSeries"] = pd.concat([podatki["HydroTimeSeries"], additional_rows], ignore_index=True)

# podatki["HydroTimeSeries"].iloc[2:2 + len(drava), 0] = pd.to_datetime(drava["Časovna značka"].values)

# podatki["HydroTimeSeries"].iloc[2:2 + len(drava), 1] = drava["Pretok"].values
# podatki["HydroTimeSeries"].iloc[2:2 + len(soca), 2] = soca["Pretok"].values
# podatki["HydroTimeSeries"].iloc[2:2 + len(sava_pred_radovljico), 3] = sava_pred_radovljico["Pretok"].values
# podatki["HydroTimeSeries"].iloc[2:2 + len(sava_okroglo), 4] = sava_okroglo["Pretok"].values
# podatki["HydroTimeSeries"].iloc[2:2 + len(sava_pred_catezem), 5] = sava_pred_catezem["Pretok"].values
# podatki["HydroTimeSeries"].iloc[2:2 + len(sava_catez), 6] = sava_catez["Pretok"].values




# with pd.ExcelWriter(PATH +"\\"+ datoteka_out , engine='openpyxl') as writer:
#     for sheet_name, df in podatki.items():
#         df.to_excel(writer, sheet_name=sheet_name, index=False)

