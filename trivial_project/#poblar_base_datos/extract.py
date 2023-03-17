import requests
import random   
import json
from urllib.parse import unquote
import html
import re

from googletrans import Translator, constants


#Tiene que estar en default encoding y en opcion multiple para que solo se pueda de 4 respuestas(no true or false)

a_dict = {
'geografia': 'https://opentdb.com/api.php?amount=50&category=22&type=multiple',
'arte_y_literatura': 'https://opentdb.com/api.php?amount=23&category=25&type=multiple', #Por alguna razon solo dejar llamar con 23
'historia': 'https://opentdb.com/api.php?amount=50&category=23&type=multiple',
'entretenimiento': 'https://opentdb.com/api.php?amount=50&category=23&type=multiple', # SOlo de videojuegos
'ciencias': 'https://opentdb.com/api.php?amount=50&category=17&type=multiple', #Science and nature
'deportes': 'https://opentdb.com/api.php?amount=50&category=21&type=multiple',
}




#Una vez obtenido el json, ir a esta pagina web para pasarlo a sentencias sql: https://www.convertjson.com/json-to-sql.htm

# Instancia para el traductor
translator = Translator()


def traducir(s):
    return translator.translate(s, dest='es',format_='text').text


#Guardamos sin repetir ninguno
def guardar(dict_preguntas,nombreFichero):
    unique_preguntas = {pregunta['enunciado']: pregunta for pregunta in dict_preguntas['preguntas']}
    dict_preguntas["preguntas"] = list(unique_preguntas.values())

    save_file = open(nombreFichero, "w",encoding='utf-8')  
    json.dump(dict_preguntas, save_file, indent = 6,ensure_ascii=False)
    save_file.close()


def todos():
    for key in a_dict:
        
        tematica = key
        url_link = a_dict[key]

        dict_preguntas_en = {
            "preguntas":[]
        }

        dict_preguntas_es = {
            "preguntas":[]
        }
        print(url_link)
        print(tematica)
        for veces in range(1,15):
            print("Iteracion: " + str(veces))
            r = requests.get(url = url_link)  
            data = r.json()
            print(data['response_code'])

            count = len(data['results'])
            for i in range(0,count):
                dict_pregunta = {
                "enunciado":html.unescape(data['results'][i]['question']),
                "r_bien":html.unescape(data['results'][i]['correct_answer']),
                "r_mal1":html.unescape(data['results'][i]['incorrect_answers'][0]),
                "r_mal2":html.unescape(data['results'][i]['incorrect_answers'][1]),
                "r_mal3":html.unescape(data['results'][i]['incorrect_answers'][2]),
                "tema_id":tematica,
                }
                dict_preguntas_en["preguntas"].append(dict_pregunta)

                dict_pregunta = {
                "enunciado":traducir(html.unescape(data['results'][i]['question'])),
                "r_bien":traducir(html.unescape(data['results'][i]['correct_answer'])),
                "r_mal1":traducir(html.unescape(data['results'][i]['incorrect_answers'][0])),
                "r_mal2":traducir(html.unescape(data['results'][i]['incorrect_answers'][1])),
                "r_mal3":traducir(html.unescape(data['results'][i]['incorrect_answers'][2])),
                "tema_id":tematica,
                }
                dict_preguntas_es["preguntas"].append(dict_pregunta)

        #Eliminamos las que son repetidas
        guardar(dict_preguntas_en,"filename_"+ tematica + "_en.json")
        guardar(dict_preguntas_es,"filename_"+ tematica + "_es.json")

def uno():
    tematica = "arte_y_literatura"
    url_link = "https://opentdb.com/api.php?amount=23&category=25&type=multiple"
    iteraciones = 45

    dict_preguntas_en = {
        "preguntas":[]
    }

    dict_preguntas_es = {
        "preguntas":[]
    }
    for veces in range(1,iteraciones):
        print("Iteracion: " + str(veces))
        r = requests.get(url = url_link)  
        data = r.json()
        print(data['response_code'])

        count = len(data['results'])
        for i in range(0,count):
            dict_pregunta = {
            "enunciado":html.unescape(data['results'][i]['question']),
            "r_bien":html.unescape(data['results'][i]['correct_answer']),
            "r_mal1":html.unescape(data['results'][i]['incorrect_answers'][0]),
            "r_mal2":html.unescape(data['results'][i]['incorrect_answers'][1]),
            "r_mal3":html.unescape(data['results'][i]['incorrect_answers'][2]),
            "tema_id":tematica,
            }
            dict_preguntas_en["preguntas"].append(dict_pregunta)

            dict_pregunta = {
            "enunciado":traducir(html.unescape(data['results'][i]['question'])),
            "r_bien":traducir(html.unescape(data['results'][i]['correct_answer'])),
            "r_mal1":traducir(html.unescape(data['results'][i]['incorrect_answers'][0])),
            "r_mal2":traducir(html.unescape(data['results'][i]['incorrect_answers'][1])),
            "r_mal3":traducir(html.unescape(data['results'][i]['incorrect_answers'][2])),
            "tema_id":tematica,
            }
            dict_preguntas_es["preguntas"].append(dict_pregunta)

    #Eliminamos las que son repetidas
    guardar(dict_preguntas_en,"filename_"+ tematica + "_en.json")
    guardar(dict_preguntas_es,"filename_"+ tematica + "_es.json")





#todos()
uno()




