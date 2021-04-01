import requests
import json
from zipfile import ZipFile
from io import BytesIO
import pandas as pd
import matplotlib.pyplot as plt
import folium
import webbrowser
import os
from selenium import webdriver

# Variables et fonctions
n = 1  # proportion cercle pour la visualisation
Times_beg = ['2020-08-01', '2020-08-09', '2020-08-16', '2020-08-23',
             '2020-09-01', '2020-09-09', '2020-09-16', '2020-09-23',
             '2020-10-01', '2020-10-09', '2020-10-16', '2020-10-23',
             '2020-11-01', '2020-11-09', '2020-11-16', '2020-11-23',
             '2020-12-01', '2020-12-09', '2020-12-16', '2020-12-23']

Times_end = ['2020-08-08', '2020-08-15', '2020-08-22', '2020-08-31',
             '2020-09-08', '2020-09-15', '2020-09-22', '2020-09-30',
             '2020-10-08', '2020-10-15', '2020-10-22', '2020-10-31',
             '2020-11-08', '2020-11-15', '2020-11-22', '2020-12-01',
             '2020-12-08', '2020-12-15', '2020-12-22', '2021-01-01']

Balise = ['Vacances scolaire', 'Vacances scolaire', 'Vacances scolaire',
          'Vacances scolaire',  'Rentrée scolaire', 'Rentrée scolaire',
          'Rentrée scolaire', '', '', '', '', '',
          'Confinement', 'Confinement', 'Confinement', 'Confinement',
          'Confinement', 'Confinement', 'Confinement', 'Vacance de Noël']

Boucle = len(Times_beg)


def form(str):
    ''' This function load json file and change the format
        to as data set with international day time '''

    with open(str) as f:
        data = json.loads("[" + f.read().replace('}\n{', "},\n{") + "]")
    df = pd.DataFrame(data)

    for i in range(df.shape[0]):
        df.loc[i, 'dateObserved'] = df.loc[i, 'dateObserved'][0:10]
    time_improved = pd.to_datetime(df['dateObserved'], format='%Y/%m/%d')
    df['dateObserved'] = time_improved
    return df


def select_date(df, begin, end):
    ''' Select data in function of date in a data frame'''
    mask = ((df['dateObserved'] > begin) & (df['dateObserved'] < end))
    df = df.loc[mask]
    return df


def data_construct(df):
    moy = df["intensity"].mean()
    # std = df["intensity"].std()
    return moy


# Load data

r = requests.get('https://data.montpellier3m.fr/node/12038/download')
z = ZipFile(BytesIO(r.content))
file = z.extractall('./Zip_stockage')

# Main loop

for j in range(Boucle):
    cpt1 = form('./Zip_stockage/MMM_EcoCompt_X2H19070220_Archive2020.json')
    cpt2 = form('./Zip_stockage/MMM_EcoCompt_X2H20042632_Archive2020.json')
    cpt3 = form('./Zip_stockage/MMM_EcoCompt_X2H20042633_Archive2020.json')
    cpt4 = form('./Zip_stockage/MMM_EcoCompt_X2H20042634_Archive2020.json')
    cpt5 = form('./Zip_stockage/MMM_EcoCompt_X2H20042635_Archive2020.json')
    cpt6 = form('./Zip_stockage/MMM_EcoCompt_X2H20063161_Archive2020.json')
    cpt7 = form('./Zip_stockage/MMM_EcoCompt_X2H20063162_Archive2020.json')
    cpt8 = form('./Zip_stockage/MMM_EcoCompt_X2H20063163_Archive2020.json')
    cpt9 = form('./Zip_stockage/MMM_EcoCompt_XTH19101158_Archive2020.json')

    data_set = [cpt1, cpt2, cpt3, cpt4, cpt5, cpt6, cpt7, cpt8, cpt9]
    data_selected = []

    # Selection des dates puis calcul de la moyenne sur les dates 
    # et pour chaque localisation

    for i in data_set:
        data_selected.append(select_date(i, Times_beg[j], Times_end[j]))
        # print(f'Datebegin:{Times_beg[j]}, TimeEndn:{Times_end[j]}')
    moylist = []

    for i in data_selected:
        moylist.append(round(data_construct(i)))
        # print(data_construct(i))

    collist = []

    # Attribut une couleur en fonction du nombre de passage
    for i in moylist:
        if i > 900:
            collist.append('green')
        if i < 300:
            collist.append('red')
        if 300 < i < 900:
            collist.append('orange')

    # Create a Map instance
    m = folium.Map(titles= 'mtp_bike', location=[43.59666660141285, 3.878532192712331], zoom_start=13)

    # Add marker

    # Sans Nom
    folium.Marker(
        location=[43.60969924926758, 3.896939992904663],
        popup=f'{moylist[0]} passages',
        icon=folium.Icon(color=collist[0], icon='ok-sign'),
    ).add_to(m)

    folium.Circle(
        radius=(moylist[0])/n,
        location=[43.60969924926758, 3.896939992904663],
        color=collist[0],
        fill=True,
    ).add_to(m)

    # Juvignac
    folium.Marker(
        location=[43.5907, 3.81324],
        popup=f'{moylist[1]} passages',
        icon=folium.Icon(color=collist[1], icon='ok-sign'),
    ).add_to(m)

    folium.Circle(
        radius=(moylist[1])/n,
        location=[43.5907, 3.81324],
        color=collist[1],
        fill=True,
    ).add_to(m)

    # Lodeve

    folium.Marker(
        location=[43.61465, 3.8336],
        popup=f'{moylist[2]} passages',
        icon=folium.Icon(color=collist[2], icon='ok-sign'),
    ).add_to(m)

    folium.Circle(
        radius=(moylist[2])/n,
        location=[43.61465, 3.8336],
        color=collist[2],
        fill=True,
    ).add_to(m)

    # Fraiche1
    folium.Marker(
        location=[43.57926, 3.93327],
        popup=f'{moylist[3]} passages',
        icon=folium.Icon(color=collist[3], icon='ok-sign'),
    ).add_to(m)

    folium.Circle(
        radius=(moylist[3])/n,
        location=[43.57926, 3.93327],
        color=collist[3],
        fill=True,
    ).add_to(m)
    # Fraiche2

    folium.Marker(
        location=[43.57883, 3.93324],
        popup=f'{moylist[4]} passages',
        icon=folium.Icon(color=collist[4], icon='ok-sign'),
    ).add_to(m)
    folium.Circle(
        radius=(moylist[4])/n,
        location=[43.57883, 3.93324],
        color=collist[4],
        fill=True,
    ).add_to(m)
    # Poste
    folium.Marker(
        location=[43.6157418, 3.9096322],
        popup=f'{moylist[5]} passages',
        icon=folium.Icon(collist[5], icon='ok-sign'),
    ).add_to(m)
    folium.Circle(
        radius=(moylist[5])/n,
        location=[43.6157418, 3.9096322],
        color=collist[5],
        fill=True,
    ).add_to(m)

    # Gerhardt
    folium.Marker(
        location=[43.6138841, 3.8684671],
        popup=f'{moylist[6]} passages',
        icon=folium.Icon(color=collist[6], icon='ok-sign'),
    ).add_to(m)
    folium.Circle(
        radius=(moylist[6])/n,
        location=[43.6138841, 3.8684671],
        color=collist[6],
        fill=True,
    ).add_to(m)

    # Delmas
    folium.Marker(
        location=[43.6266977, 3.8956288],
        popup=f'{moylist[7]} passages',
        icon=folium.Icon(color=collist[7], icon='ok-sign'),
    ).add_to(m)
    folium.Circle(
        radius=(moylist[7])/n,
        location=[43.6266977, 3.8956288],
        color=collist[7],
        fill=True,
    ).add_to(m)

    # Albert 1er

    folium.Marker(
        location=[43.61620945549243, 3.874408006668091],
        popup=f'{moylist[8]} passages',
        tooltip=f'ester-egg',
        icon=folium.Icon(color=collist[8], icon='ok-sign'),
    ).add_to(m)

    folium.Circle(
        radius=(moylist[8])/n,
        location=[43.61620945549243, 3.874408006668091],
        color=collist[8],
        fill=True,
    ).add_to(m)

    loc0 = f'Github: Nathanesteve Nombre passage en velo du {Times_beg[j]} au {Times_end[j]}    {Balise[j]}'
    title_html = '''
                <h3 align="center" style="font-size:16px"><b>{}</b></h3>
                '''.format(loc0)
    m.get_root().html.add_child(folium.Element(title_html))
    loc1 = 'Rouge : moins de 300 passages journalier'
    title_html = '''
                <p style="color:#DC143C";>Rouge : moins de 300 passages moyen </p>
                '''.format(loc1)
    m.get_root().html.add_child(folium.Element(title_html))
    loc2 = ' Orange: entre 300 et 900 passages journalier'
    title_html = '''
                <p style="color:#FF8C00";>Orange: entre 300 et 900 passages moyen </p>
                '''.format(loc2)
    m.get_root().html.add_child(folium.Element(title_html))
    loc3 = 'Vert : plus de 900 passages journalier'                                      
    title_html = '''
                <p style="color:#008000";>Vert : plus de 900 passages moyen </p>
                '''.format(loc3)
    m.get_root().html.add_child(folium.Element(title_html))

    m.save(f'./Code_visualisation_Montpellier_cycliste/map{j}.html')
    #  webbrowser.open(f'map{j}.html') # Affiche en Pop up la map
