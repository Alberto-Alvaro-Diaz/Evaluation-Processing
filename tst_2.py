# OPEN AND PROCESS DATA
import os
import pandas as pd
import numpy as np

# to compare strings
from thefuzz import fuzz

# import functions
from Rutina_eleccion_nombres import *

print(fuzz.partial_ratio("Paco", "Paco Santamaria"))  

current_dire = os.getcwd()
file_name = "Evaluación Humana 2025 (respuestas).xlsx"
file_path = os.path.join(current_dire, file_name)
dataset = pd.read_excel(file_path)

for name, sub_dataset in dataset.groupby(['¿En qué quincena has estado?','¿En qué grupo has estado?']):
    list_keys = sub_dataset.keys()

    print(name, sub_dataset['Nombre:'])
    autocritica_comments = sub_dataset[list_keys[5:12]]
    direccion_num_comments = sub_dataset[list_keys[12:19]]
    direccion_open_comments = sub_dataset[list_keys[19:23]]
    coordi_bool = sub_dataset[list_keys[23]]
    coordi_num_comments = sub_dataset[list_keys[24:28]]
    coordi_open_comments = sub_dataset[list_keys[28:32]]
    moni_name = []
    moni_num_comments = []
    moni_open_cooments = []
    # se repiten
    for n in range(4):
        step = n*13
        moni_name.append(sub_dataset[list_keys[32 + step]])
        moni_num_comments.append(sub_dataset[list_keys[33 + step:42 + step]])
        moni_open_cooments.append(sub_dataset[list_keys[42 + step:45 + step]])
    
    names = nombres_repetidos(moni_name, umbral = 85)
    # create a dictionary for every name
    dict_names = {}
    for name in names:
        dict_names[name] = {}
        # initialise a list for all the questions
        for key in moni_num_comments[0].keys():
            dict_names[name][key] = []

    # iterate the keys (questions) to fill the dict_name dictiionary
    for idx_1, set in enumerate(moni_num_comments):
        # select the keys from the dictionary
        keys_list = []
        for key in dict_names.keys():
            for name in moni_name[idx_1]:
                if fuzz.partial_ratio(key, name) > 80:
                    keys_list.append(key)
        for idx_2, key in enumerate(keys_list):
            for idx_3, question in enumerate(set.keys()): 
                for key_question in dict_names[key].keys():
                    if fuzz.partial_ratio(key_question, question) > 90:  # las preguntas repetidas no está exactamente igual escritas
                        question = key_question
                        break
                dict_names[key][question].append(set.values.tolist()[idx_2][idx_3])

    # iterate dict_name to compute the numerical average
    for name in dict_names.keys():
        for question in dict_names[name].keys():
            mean = np.mean(dict_names[name][question])
            dict_names[name][question] = mean
    print()

