import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
from calendar import isleap
from profil_odjem_ELES_fun import profil_odjema
from profil_mhe_fun import profil_mhe
from profil_sonce_fun import profil_sonce
from profil_loss_fun import profil_loss
from profil_STPE_BIOPLIN_fun import profil_STPE_BIOPLIN
from profile_wind_fun import profile_wind
from profil_toplotna_fun import profil_toplotna
from profil_prolnilnic_fun import profil_polnilnic
from profil_ne_OVE_fun import profil_ne_OVE

PATH=os.path.abspath(os.getcwd())


ELES_profil = profil_odjema("OU") # 2 možnosti "OU" ali "DU"




mhe_profil = profil_mhe("DUOVE") # "OU" ali "DUOVE" ali "DUJE"
SE_profil_DO, SE_profil_PO = profil_sonce("DUOVE")
STPE_profil = profil_STPE_BIOPLIN("DUOVE")
veter_profil_si, veter_profil_au = profile_wind("DUOVE")
toplotna_profil = profil_toplotna()# samo DU
polnolnice_profil = profil_polnilnic()# samo DU
NE_OVE_profil = profil_ne_OVE("OU") # "OU" ali "DUOVE" ali "DUJE"



koncni_profil_brez_izgub = ELES_profil + toplotna_profil + polnolnice_profil  - mhe_profil - veter_profil_si - SE_profil_DO - SE_profil_PO - STPE_profil - NE_OVE_profil
profil_losses = profil_loss(koncni_profil_brez_izgub) # se ne razlikuje glede na OU ali DU

koncni_profil = koncni_profil_brez_izgub + profil_losses


# data_to_plot = koncni_profil.iloc[24*(365*23+100):24*(365*23+120)]
# #another_to_plot = veter_profil_au.iloc[24*200:24*230]
# # data_to_plot = polnilnice_profil2['profil'].iloc[:8760]

# plt.figure(figsize=(15,5))
# plt.plot(data_to_plot.index, data_to_plot.values)
# #plt.plot(another_to_plot.index, another_to_plot.values)
# plt.title("Hourly profile")
# plt.xlabel("Time")
# plt.ylabel("Value")
# plt.grid(True)
# plt.show()
