import matplotlib as plt
import numpy as np
import re
import pandas as pd

iterar = ['Ciudad de México', 'Campeche', 'Puebla', 'Estado de México',
          'Veracruz de Ignacio de la Llave', 'Hidalgo', 'Sinaloa',
          'Nuevo León', 'Quintana Roo', 'Jalisco', 'Coahuila de Zaragoza',
          'San Luis Potosí', 'Tamaulipas', 'Querétaro', 'Guanajuato',
          'Yucatán', 'Tabasco', 'Baja California', 'Oaxaca',
          'Sonora', 'Nayarit', 'Morelos', 'Durango',
          'Guerrero', 'Chihuahua', 'Michoacán de Ocampo', 'Chiapas',
          'Aguascalientes', 'Zacatecas', 'Tlaxcala', 'Baja California Sur',
          'Colima', 'Otro']


'''
Funcion para obten de un txt texto y quitar emojis
return una lista de terminos o de textos
'''


def dataImport(filename):
    info = []
    for xs in filename:
        data = open(xs)
        for r in data:
            r = r.replace('\n', '')
            r = re.sub('https\W*t.co/\w*', '', r)
            info.append(r.encode('utf-8', 'ignore').decode('utf-8'))
    return info


'''
Funcion que etiqueta apartir de una lista de terminos
El dataFrame debe contener una columa de nombre texto
1 si el termino aparece 0 en otro caso
return un el dataFrame original con una columna etiqueta
'''


def etiqueta(data, etiqueta):
    data_text = data['texto'].tolist()
    list_et = []
    val = -1
    for xs in data_text:
        val = -1
        for ys in etiqueta:
            if len(re.findall(ys, xs.lower())) > 0:
                val = 1
                break
            else:
                val = 0
        list_et.append(val)
    eti_df = pd.DataFrame(list_et, columns=['etiqueta'])
    return pd.concat([data, eti_df], axis=1)


def etiqueta_txt(data, etiqueta):
    val = -1
    for ys in etiqueta:
        if len(re.findall(ys, data.lower())) > 0:
            val = 1
        break
    else:
        val = 0
    return val


'''
Funcion que apartir de una lista de texto y una lista de terminos
saca el numero de apariciones de los terminos
return dataFrame con los terminos y su pertinente numero de apariciones
'''


def numApariciones(data, terminos):
    texto = data['texto'].tolist()
    numRepeticiones = []
    terminos_fil = []
    it = 0
    for xs in terminos:
        it = 0
        for ys in texto:
            it += len(re.findall(xs, ys.lower()))
        if it > 0:
            numRepeticiones.append(it)
            terminos_fil.append(xs)

    terminos_df = pd.DataFrame(terminos_fil, columns=['terminos'])
    aparaciones_df = pd.DataFrame(numRepeticiones, columns=['#Repeticiones'])
    return pd.concat([terminos_df, aparaciones_df], axis=1)


'''
Funcion que apartir de una lista de texto y una lista de terminos
saca el numero de apariciones de los terminos por estados de la republica
return dataFrame con los terminos y su pertinente numero de apariciones
'''


def numApariciones_eds(data, terminos, estado):
    info = []
    texto = data['texto'].tolist()
    numRepeticiones = []
    terminos_fil = []
    it = 0
    for xs in terminos:
        it = 0
        for ys in texto:
            it += len(re.findall(xs, ys.lower()))
        if it > 0:
            numRepeticiones.append(it)
            terminos_fil.append(xs)

    info.append([estado, terminos_fil, numRepeticiones])
    return pd.DataFrame(info, columns=['Estado', 'terminos', '#Repeticiones'])

    # terminos_df = pd.DataFrame(terminos, columns=['terminos'])
    # aparaciones_df = pd.DataFrame(numRepeticiones, columns=['#Repeticiones'])
    # return pd.concat([terminos_df, aparaciones_df], axis=1)


'''
Funcion para hacer una  grafica de radar
apartir de un dataFrame con dos columna de nombre terminos y #Repeticiones
'''


def grafica_radar(data, termino):
    labels = np.array(data['terminos'])
    stats = data['#Repeticiones'].values

    angles = np.linspace(0, 2*np.pi, len(labels), endpoint=False)

    stats = np.concatenate((stats, [stats[0]]))
    angles = np.concatenate((angles, [angles[0]]))

    fig = plt.figure(figsize=(22.2, 11.4))
    ax = fig.add_subplot(111, polar=True)
    ax.plot(angles, stats, 'o-', linewidth=2)
    ax.fill(angles, stats, alpha=0.25)
    ax.set_thetagrids(angles * 180/np.pi, labels)
    ax.set_title(termino + ' mas mencionados')
    ax.grid(True)
    plt.show()


def change_edo(data, archivo):
    estados = pd.read_csv(archivo, index_col=0)
    # Convertimos el dataset a diccionario donde la llave es el lugar
    estados = estados.drop_duplicates(subset='PlaceJson')
    estados = estados.set_index('PlaceJson').T.to_dict('list')
    ed_replace = []
    ed = data['full_place'].tolist()
    for xs in ed:
        try:
            if estados[xs] != 'nan':
                ed_replace.append(estados[xs][0])
            else:
                ed_replace.append('Otro')
        except:
            ed_replace.append('Otro')
    data = data.drop('full_place', axis=1)
    data['Estado'] = ed_replace
    return data


def repetcions_ed(data, terminos):
    info_df = pd.DataFrame()
    for xs in iterar:
        data_ed = data[data['Estado'] == xs]
        info = numApariciones_eds(data_ed, terminos, xs)
        info_df = pd.concat([info_df, info], axis=0)
    return info_df
