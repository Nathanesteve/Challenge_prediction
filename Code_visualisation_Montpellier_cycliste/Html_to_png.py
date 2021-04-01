from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import time
import os


# Ne fonction qu'avec Firefox possibilite de faire des modifications pour d'autre navigateur voir la doc de webdriver

Times_beg = ['2020-08-01', '2020-08-09', '2020-08-16', '2020-08-23',
             '2020-09-01', '2020-09-09', '2020-09-16', '2020-09-23',
             '2020-10-01', '2020-10-09', '2020-10-16', '2020-10-23',
             '2020-11-01', '2020-11-09', '2020-11-16', '2020-11-23',
             '2020-12-01', '2020-12-09', '2020-12-16', '2020-12-23']


def folium_map_to_png(filename):
    delay = 4
    input_dir = 'file://{path}/{mapfile}'.format(path=os.getcwd(),mapfile=filename)
    #Open a browser window...
    browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())
    # browser = webdriver.Firefox(executable_path=os.path.abspath("chromedriver"))
    #..that displays the map...
    browser.get(input_dir)
    #Give the map tiles some time to load
    time.sleep(delay)
    #Grab the screenshot
    curr_dir = os.getcwd()
    src_folder = curr_dir 
    if not os.path.exists(src_folder):
        os.mkdir(src_folder)
    src_subfolder = src_folder + filename.rpartition("_")[0] + "/"
    if not os.path.exists(src_subfolder):
        os.mkdir(src_subfolder)
    pic = src_subfolder + filename.split(".")[0] + ".png"
    browser.save_screenshot(pic)
    #Close the browser
    browser.quit()

for i in range(len(Times_beg)):
    folium_map_to_png(f'./Code_visualisation_Montpellier_cycliste/map{i}.html')
