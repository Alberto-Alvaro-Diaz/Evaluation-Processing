# OPEN AND PROCESS DATA
import os
import pandas as pd
import numpy as np

# import functions
from Rutina_eleccion_nombres import *
from Rutina_ordenar_comentarios import *
from pdf_rutine_2 import *

if __name__ == "__main__":

    current_dire = os.getcwd()
    file_name = "Evaluación Humana 2025 (respuestas).xlsx"
    file_path = os.path.join(current_dire, file_name)
    dataset = pd.read_excel(file_path)
    output_path = os.path.join(current_dire,  "evaluaciones")

    for name, sub_dataset in dataset.groupby(['¿En qué quincena has estado?','¿En qué grupo has estado?']):
        list_keys = sub_dataset.keys()

        print(name, sub_dataset['Nombre:'])
        autocritica_comments = sub_dataset[list_keys[5:12]]
        direccion_num_comments = sub_dataset[list_keys[12:19]]
        direccion_open_comments = sub_dataset[list_keys[19:23]]
        coordi_bool = sub_dataset[list_keys[23]]
        coordi_num_comments = sub_dataset[list_keys[24:28]]
        coordi_open_comments = sub_dataset[list_keys[28:32]]
        
        #### MONIS ####
        moni_name = []
        moni_num_comments = []
        moni_open_comments = []
        # se repiten
        for n in range(4):
            step = n * 13
            moni_name.append(sub_dataset[list_keys[32 + step]])
            moni_num_comments.append(sub_dataset[list_keys[33 + step:42 + step]])
            moni_open_comments.append(sub_dataset[list_keys[42 + step:45 + step]])
        
        # remove repeated names
        names = nombres_repetidos(moni_name, umbral = 85)

        # open fields
        dict_names_open = fill_moni_fields(names, moni_name, moni_open_comments)

        # numerical fields
        dict_names_num = fill_moni_fields(names, moni_name, moni_num_comments)

        # iterate dict_name to compute the numerical average
        for name in dict_names_num.keys():
            for question in dict_names_num[name].keys():
                mean = np.mean(dict_names_num[name][question])
                dict_names_num[name][question] = mean

        # call pdf rutine
        for name_moni, dict_num in dict_names_num.items():
            comentario = []
            for open_question in dict_names_open[name_moni]:
                comentario.append(f"{open_question}\n {"\n".join(dict_names_open[name_moni][open_question])}")

            str_comentario = "\n".join(comentario)
            creating_pdf(name_moni, dict_num, str_comentario, output_path)

        print()

