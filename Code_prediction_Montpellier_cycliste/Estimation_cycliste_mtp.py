# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from download import download
import seaborn as sns
import statistics

# %% Téléchargement et nettoyage des données
url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQVtdpXMHB4g9h75a0jw8CsrqSuQmP5eMIB2adpKR5hkRggwMwzFy5kB-AIThodhVHNLxlZYm8fuoWj/pub?gid=2105854808&single=true&output=csv'
download(url=url, path='Bike_raw')
bike_raw = pd.read_csv("bike_raw")
df_bike = bike_raw.drop('Remarque', 1)
df_bike = df_bike.drop('Unnamed: 4', 1)
df_bike = df_bike.dropna(axis=0)

# Conversion en temps international
time_improved = pd.to_datetime(df_bike['Date'] + ' ' + df_bike['Heure / Time'],
                               format='%d/%m/%Y %H:%M:%S')

df_bike['DateTime'] = time_improved
df_bike['Date'] = pd.to_datetime(df_bike['Heure / Time'], format='%H:%M:%S')
df_bike['Heure'] = pd.to_datetime(df_bike['Heure / Time'])


del df_bike['Heure / Time']
del df_bike['Vélos depuis le 1er janvier / Grand total']

# Set index
bike = df_bike.set_index(['DateTime'])
bike = bike.sort_index()

bike['weekday'] = bike.index.weekday

days = ['Lundi', 'Mardi', 'Mercredi',
        'Jeudi', 'Vendredi', 'Samedi', 'Dimanche']

bike_week = bike.groupby(['weekday', bike.index.hour])[
    "Vélos ce jour / Today's total"].mean().unstack(level=0)


# Affichage du nombre moyen de passage en selon le jour de la semaine
plt.figure(figsize=(15, 6))
sns.set_palette("viridis", n_colors=7)
plt.plot(bike_week)
plt.title("Moyenne par heure et selon les jours")
plt.ylabel("Nombre de passages")
plt.xlabel("Heure de la journée")
plt.xticks(np.arange(0, 24))
plt.legend(labels=days, loc='lower left', bbox_to_anchor=(1, 0.1))
plt.savefig("Passage_cycliste_mtp.pdf")
plt.show()

# Supression du samedi et dimanche
bike = bike[bike.weekday != 6]
bike = bike[bike.weekday != 5]

# %% On choisis une date de depart pour l'analyse
start_date = '2021-01-01 00:00:00'
mask = (bike.index > start_date)
filtered_bike = bike.loc[mask]

# On selectionne les durées qui nous interesse
df_time1 = filtered_bike.between_time('08:30:00', '09:30:00')
df_time2 = bike.between_time('08:30:00', '09:30:00')
df = df_time1.drop_duplicates(['Date'], keep='last')
del df['Date']
a, b = df.shape


# Estimation on donne un poids proportionnel au temps ou à etait pris la mesure
# un poids de 2 si la mesure est prise entre 8:55 et 9:05
# un poids de 1 si la mesure est prise entre 8:45 et 8:55 ou 9:05 et 9:15
# un poids de 1/2 si la mesure est prise entre 8:30 et 8:45 ou 9:15 et 9:30

poids = 2
poids1 = 1
poids2 = 1/2

stockage_heure = []
stockage_passage = []
stockage_poids = []

for i in df['Heure']:
    a = str(i)
    z = a[11:]
    if ('08:29:00' < z < '08:45:00' or ('09:14:00' < z < '09:31:00')):
        stockage_poids.append(poids2)
    if ('08:44:00' < z < '08:55:00' or ('09:04:00' < z < '09:15:00')):
        stockage_poids.append(poids1)
    if '08:54:00' < z < '09:05:00':
        stockage_poids.append(poids)

# Valeur de stockage de calcul
z = 0
w = 0

for i in df["Vélos ce jour / Today's total"]:
    stockage_passage.append(i)
    z = z + (i * stockage_poids[w])
    w = w + 1
print(df)
# Prediction
mediane_mtp = statistics.median(stockage_passage)
ma_prediction = round(z/sum(stockage_poids))
print(f"Mediane de notre echantillons: {mediane_mtp}")
print(f"Ma prédiction est: {ma_prediction} passages à 9h pour le vendredi 2 avril")

# %%
