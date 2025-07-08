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

PATH=os.path.abspath(os.getcwd())


ELES_profil = profil_odjema("DUOVE")




mhe_profil = profil_mhe("DUOVE")
SE_profil, SE_profil2 = profil_sonce("DUOVE")
loss = profil_loss() # se ne razlikuje glede na OU ali DU
STPE_profil = profil_STPE_BIOPLIN("DUOVE")
veter_profil, veter_profil_au = profile_wind("DUOVE")
toplotna_profil = profil_toplotna()# samo DU
polnolnice_profil2 = profil_polnilnic()# samo DU

# print("ELES_profil2:", type(ELES_profil))
# print("mhe_profil:", type(mhe_profil), mhe_profil.shape)
# print("SE_profil:", type(SE_profil), SE_profil.shape)
# print("loss:", type(loss), loss.shape)
# print("STPE_profil:", type(STPE_profil), STPE_profil.shape)
# print("toplotna_profil:", type(toplotna_profil), toplotna_profil.shape)
# print("polnolnice_profil2:", type(polnolnice_profil2), polnolnice_profil2.shape)
# print("veter_profil:", type(veter_profil), veter_profil.shape)


koncni_profil = ELES_profil + mhe_profil + SE_profil2 + loss + STPE_profil + toplotna_profil + polnolnice_profil2 - veter_profil - SE_profil

#print(koncni_profil)



data_to_plot = koncni_profil.iloc[24*151:24*170]
#another_to_plot = veter_profil_au.iloc[24*200:24*230]
# data_to_plot = polnilnice_profil2['profil'].iloc[:8760]

# plt.figure(figsize=(15,5))
# plt.plot(data_to_plot.index, data_to_plot.values)
# #plt.plot(another_to_plot.index, another_to_plot.values)
# plt.title("Hourly profile")
# plt.xlabel("Time")
# plt.ylabel("Value")
# plt.grid(True)
# plt.show()
