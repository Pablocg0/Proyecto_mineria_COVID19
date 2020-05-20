import json
import pandas as pd


def json_radar(nombre, data):
    f = open(nombre+".json", "w")
    lines = '[ \n'
    for indice_fila, fila in data.iterrows():
        lines += '{\n \"subject\": \"'+fila['terminos']+'\", \"A\":'+str(fila['#Repeticiones'])+'\n },\n'
    lines = lines[:len(lines)-2] + '\n]'
    f.write(lines)
    f.close()


def json_mapa(nombre, data):
    lugar = data[0]
    etiqueta = data[1]
    numero = data[2]
    with open('../data/mapa.json') as file:
        data = json.load(file)
        for xs in data['features']:
            pro = xs['properties']
            for ys in range(len(lugar)-1):
                if pro['name'] == lugar[ys]:
                    et = etiqueta[ys]
                    num = numero[ys]
                    for ds in range(len(et)-1):
                        pro[et[ds]] = num[ds]
        with open(nombre + '.json', 'w') as file:
            json.dump(data, file, indent=4)


def procesar_mapa(nombre, data):
    lugar = data['Estado'].tolist()
    etiqueta = data['Hashtag'].tolist()
    numero = data['Num_Hash'].tolist()
    json_mapa(nombre[0], [lugar, etiqueta, numero])
    lugar = data['Estado'].tolist()
    etiqueta = data['Mencion'].tolist()
    numero = data['Num_mencion'].tolist()
    json_mapa(nombre[1], [lugar, etiqueta, numero])
    lugar = data['Estado'].tolist()
    etiqueta = data['Usuario_Activo'].tolist()
    numero = data['Num_Usr'].tolist()
    json_mapa(nombre[2], [lugar, etiqueta, numero])


def procesar_mapa2(nombre, data):
    lugar = data['Estado'].tolist()
    etiqueta = data['terminos'].tolist()
    numero = data['#Repeticiones'].tolist()
    json_mapa(nombre, [lugar, etiqueta, numero])
