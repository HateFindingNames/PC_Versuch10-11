import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
import os

sample_files = os.listdir("messdaten/csv_titration/")
print(sample_files)

spl_lst = []
for i,file in enumerate(sample_files):
    with open(("messdaten/csv/" + file), newline='', encoding='utf-8') as path:
        frame = pd.read_csv(path, delimiter=';')
        frame.columns = [col.strip() for col in frame] # stupid whitespaces t(-_-t)
        spl_lst.append(frame)
        del frame

aufschluss = spl_lst[0]
benzo = spl_lst[1]
aufschluss_vol = np.array(aufschluss["Vol. Maßlösung / [mL]"])
aufschluss_leit = np.array(aufschluss["Leitfähigkeit / [mS/cm]"])
benzo_vol = np.array(benzo["Vol. Maßlösung / [mL]"])
benzo_leit = np.array(benzo["Leitfähigkeit / [uS/cm]"])
# aufschluss_links = np.array(aufschluss_vol[0:np.argmin(aufschluss_leit)], aufschluss_leit[0:np.argmin(aufschluss_leit)])
# aufschluss_links[1:] = aufschluss_vol[0:np.argmin(aufschluss_leit)]
# aufschluss_rechts[0:] = aufschluss_leit[np.argmin(aufschluss_leit):-1]
# aufschluss_rechts[1:] = aufschluss_vol[np.argmin(aufschluss_leit):-1]

# print(aufschluss_links)

def func(x, m, b):
    return x*m+b

cm = 1/2.54 # inch to cm, metric like brrr

# Nightowl mode
plt.style.use("default")
plt.style.use("seaborn-paper")

fig1, ax1 = plt.subplots(figsize=(20*cm, 20*(9/16)*cm))

ax1.scatter(aufschluss["Vol. Maßlösung / [mL]"], aufschluss["Leitfähigkeit / [mS/cm]"])
popt, pcov = curve_fit(func, np.array(aufschluss_vol[0:np.argmin(aufschluss_leit)]), np.array(aufschluss_leit[0:np.argmin(aufschluss_leit)]))
ax1.plot(np.array(aufschluss_vol[0:np.argmin(aufschluss_leit)+8]), func(np.array(aufschluss_vol[0:np.argmin(aufschluss_leit)+8]), *popt), color="#800000", linestyle="--")
popt, pcov = curve_fit(func, np.array(aufschluss_vol[np.argmin(aufschluss_leit):-1]), np.array(aufschluss_leit[np.argmin(aufschluss_leit):-1]))
ax1.plot(np.array(aufschluss_vol[np.argmin(aufschluss_leit)-2:-1]), func(np.array(aufschluss_vol[np.argmin(aufschluss_leit)-2:-1]) ,*popt), color="#800000", linestyle="--")

ax1.set_title("Verlauf der Leitfähigkeit - Aufschluss aus V11", fontsize=12)
ax1.set_xticks(np.arange(0,23,2))
ax1.set_xlabel("Vol. Maßlösung / $mL$", fontsize=8)
ax1.set_ylabel("Leitfähigkeit / $\\frac{mS}{cm}$", fontsize=8)
ax1.grid(axis='both', alpha=.3)

plt.tight_layout()
# plt.show()
plt.savefig("assets/plots/titration/aufschluss.svg")
#========================================================
fig2, ax2 = plt.subplots(figsize=(20*cm, 20*(9/16)*cm))

ax2.scatter(benzo["Vol. Maßlösung / [mL]"], benzo["Leitfähigkeit / [uS/cm]"])
popt, pcov = curve_fit(func, np.array(benzo_vol[0:np.argmin(benzo_leit)]), np.array(benzo_leit[0:np.argmin(benzo_leit)]))
ax2.plot(np.array(benzo_vol[0:np.argmin(benzo_leit)+4]), func(np.array(benzo_vol[0:np.argmin(benzo_leit)+4]), *popt), color="#800000", linestyle="--")
popt, pcov = curve_fit(func, np.array(benzo_vol[np.argmin(benzo_leit):-1]), np.array(benzo_leit[np.argmin(benzo_leit):-1]))
ax2.plot(np.array(benzo_vol[np.argmin(benzo_leit)-1:-1]), func(np.array(benzo_vol[np.argmin(benzo_leit)-1:-1]) ,*popt), color="#800000", linestyle="--")

ax2.set_title("Verlauf der Leitfähigkeit - Benzoesäure", fontsize=12)
ax2.set_xticks(np.arange(0,46,5))
ax2.set_xlabel("Vol. Maßlösung / $mL$", fontsize=8)
ax2.set_ylabel("Leitfähigkeit / $\\frac{\\mu S}{cm}$", fontsize=8)
ax2.grid(axis='both', alpha=.3)

plt.tight_layout()
# plt.show()
plt.savefig("assets/plots/titration/benzo.svg")