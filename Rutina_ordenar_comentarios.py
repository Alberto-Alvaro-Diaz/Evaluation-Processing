# Rutine to sort all the comments 
# to compare strings
from thefuzz import fuzz

def fill_moni_fields(names: list, moni_name: list, moni_comments: list, n_name: int = 80, n_question: int = 90) -> dict:
    # create a dictionary for every name
    dict_names = {}
    for name in names:
        dict_names[name] = {}
        # initialise a list for all the (numerical and open) questions 
        for key in moni_comments[0].keys():
            dict_names[name][key] = []

    # iterate the keys (questions) to fill the dict_name dictionary
    for idx_1, set in enumerate(moni_comments):
        # select the keys from the dictionary
        keys_list = []
        for name in moni_name[idx_1]:
            for key in dict_names.keys():
                if fuzz.partial_ratio(key, name) > n_name:
                    keys_list.append(key)
        # iterate the keys_list (moni names)
        for idx_2, key in enumerate(keys_list):
            for idx_3, question in enumerate(set.keys()): 
                for key_question in dict_names[key].keys():
                    if fuzz.partial_ratio(key_question, question) > n_question:  # las preguntas repetidas no están exactamente igual escritas
                        question = key_question
                        break
                dict_names[key][question].append(set.values.tolist()[idx_2][idx_3])
    
    return dict_names