import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import os

sample_files = os.listdir("messdaten/csv_kalo/")
print(sample_files)

spl_lst = []
for i,file in enumerate(sample_files):
    with open(("messdaten/csv_kalo/" + file), newline='', encoding='utf-8') as path:
        frame = pd.read_csv(path, delimiter=';')
        frame.columns = [col.strip() for col in frame] # stupid whitespaces t(-_-t)
        spl_lst.append(frame)
        del frame

kalib = spl_lst[0]
benzo = spl_lst[1]
kalib_zeit = np.array(kalib["Zeit"] * 60)
kalib_temp = np.array(kalib["Temp"] + 273.15)
benzo_zeit = np.array(benzo["Zeit"] * 60)
benzo_temp = np.array(benzo["Temp"] + 273.15)
print(np.min(kalib_temp))
cm = 1/2.54 # inch to cm, metric like brrr

# Nightowl mode
plt.style.use("default")
plt.style.use("seaborn-paper")

fig1, ax1 = plt.subplots(figsize=(20*cm, 20*(9/16)*cm))

ax1.plot(kalib_zeit, kalib_temp, label="Kalibrierung")
ax1.plot(benzo_zeit, benzo_temp, label="Probe", color="#800000")

ax1.set_title("Temperaturänderung der kalorimetrischen Bestimmung", fontsize=12)
ax1.set_xlabel("Zeit / [s]", fontsize=8)
ax1.set_ylabel("Temperatur / [K]", fontsize=8)
ax1.axhline(np.min(kalib_temp), linestyle="--", lw=.5)
ax1.axhline(np.max(kalib_temp), linestyle="--", lw=.5)
ax1.axhline(np.min(benzo_temp), linestyle="--", lw=.5, color="#800000")
ax1.axhline(np.max(benzo_temp), linestyle="--", lw=.5, color="#800000")
ax1.legend()
ax1.grid(axis='both', alpha=.3)

plt.tight_layout()
# plt.show()
plt.savefig("assets/plots/kalo/kalo.svg")